"""Unit tests for qualreas.

These are the checks that used to follow the ``if __name__ == '__main__'`` statement at the
end of src/qualreas.py, turned into unit tests:

  * every algebra loads, has the expected relations, and passes the composition-identity
    and associativity checks
  * constraint propagation gives the expected results in the interval, point and RCC8 algebras
  * the book example (interval algebra, and its extension to points) is detected as inconsistent
  * the Wikipedia RCC8 example is read from its JSON file and propagated
  * the algebra-derivation pipeline (4-point and 6-point networks, derive_algebra) reproduces
    the interval algebras that ship in data/algebras
  * networks survive a round trip through to_dict / JSON, can be copied (mostly_copy) and
    combined (+), and can be expanded into singleton labelings
  * algebras can be built from dictionaries; relation sets, converse and composition behave as
    they should, including for bad input; add_constraint and propagate handle every kind of
    input and report what they did when asked to
  * the composition-identity and associativity checks notice an algebra that has been damaged
  * the summary and table-printing methods print what they promise to

Run from anywhere, once qualreas is installed (pip install -e .):

    python -m unittest discover -s tests -v        # or just:  pytest tests

Deriving the extended and the two branching-time interval algebras takes from 10 to 45 seconds
each, so those tests are skipped unless the environment variable QUALREAS_SLOW_TESTS is set:

    QUALREAS_SLOW_TESTS=1 python -m unittest discover -s tests -v
"""
import contextlib
import copy
import io
import itertools
import json
import os
import re
import runpy
import sys
import tempfile
import unittest

import qualreas as qr

__author__ = 'Alfred J. Reich'


def quietly(func, *args, **kwargs):
    """Call func, discarding anything it prints (e.g., is_associative prints a test summary)."""
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)


def capturing(func, *args, **kwargs):
    """Call func and return (its result, everything it printed)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args, **kwargs)
    return result, buffer.getvalue()


def relations(relset):
    """The relations in a RelSet (or a string such as 'B|D|M') as a set of names."""
    text = str(relset)
    return set(text.split('|')) if text else set()


# (algebra file name (without .json), number of relations in the algebra)
INTERVAL_ALGEBRAS = [("Linear_Interval_Algebra", 13),
                     ("Extended_Linear_Interval_Algebra", 18),
                     ("Left_Branching_Interval_Algebra", 24),
                     ("Right_Branching_Interval_Algebra", 24)]
POINT_ALGEBRAS = [("Linear_Point_Algebra", 3),
                  ("Right_Branching_Point_Algebra", 4),
                  ("Left_Branching_Point_Algebra", 4)]
RCC8_ALGEBRA = [("RCC8_Algebra", 8)]
ALL_ALGEBRAS = INTERVAL_ALGEBRAS + RCC8_ALGEBRA + POINT_ALGEBRAS


def load_algebra(name):
    return qr.Algebra(os.path.join(qr.ALGEBRA_DIR, name + ".json"))


@contextlib.contextmanager
def recursion_limit(limit):
    """Raise Python's recursion limit for a while.  Network.all_singleton_labelings is recursive
    and deriving an algebra needs a lot of depth (the derive_*.ipynb notebooks use 10000)."""
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, limit))
    try:
        yield
    finally:
        sys.setrecursionlimit(old)


def tampered(algebra_name, rel1, rel2, entry):
    """A copy of a shipped algebra in which the composition rel1;rel2 has been replaced by
    entry (a string such as 'B|M', or '' for the empty relation set)."""
    alg_dict = copy.deepcopy(load_algebra(algebra_name).algebra_dict)
    alg_dict["TransTable"][rel1][rel2] = entry
    return qr.Algebra(alg_dict=alg_dict)


def associativity_violations(algebra):
    """Every triple of relations (a, b, c) for which (a;b);c differs from a;(b;c), found with the
    algebra's own compose method.  Only meaningful for algebras with a single ontological class
    (the point algebras, Allen's interval algebra, RCC8); see TestAlgebraChecks."""
    violations = []
    for a, b, c in itertools.product(algebra.elements, repeat=3):
        ra, rb, rc = algebra.relset([a]), algebra.relset([b]), algebra.relset([c])
        if (algebra.compose(algebra.compose(ra, rb), rc)
                != algebra.compose(ra, algebra.compose(rb, rc))):
            violations.append((a, b, c))
    return violations


def intervals(names):
    """A list of proper-interval entities, one for each name in names."""
    return [qr.TemporalEntity(["ProperInterval"], name) for name in names]


def constraints_by_name(net):
    """{(tail name, head name): constraint string} for every edge of a network, so that two
    networks can be compared without caring about their node order or entity objects."""
    return {(tail.name, head.name): str(net.edges[tail, head]['constraint'])
            for tail, head in net.edges}


def make_chain(algebra, name="Chain"):
    """The network X B Y, Y D Z, propagated.  In the interval algebras X to Z is B|D|M|O|S."""
    x, y, z = intervals("XYZ")
    net = qr.Network(algebra, name)
    net.add_constraint(x, y, "B")
    net.add_constraint(y, z, "D")
    assert quietly(net.propagate)
    return net


# (point algebra, "less than" relation, interval algebra that deriving from them should give)
DERIVATIONS = [("Linear_Point_Algebra", "<", "Linear_Interval_Algebra"),
               ("Linear_Point_Algebra", "<|=", "Extended_Linear_Interval_Algebra"),
               ("Right_Branching_Point_Algebra", "<|=", "Right_Branching_Interval_Algebra"),
               ("Left_Branching_Point_Algebra", "<|=", "Left_Branching_Interval_Algebra")]

SLOW = os.environ.get("QUALREAS_SLOW_TESTS", "") not in ("", "0")
skip_unless_slow = unittest.skipUnless(
    SLOW, "slow (10-45 seconds); set QUALREAS_SLOW_TESTS=1 to run")


class TestDataLocations(unittest.TestCase):
    """The package finds its data files, wherever the tests are run from."""

    def test_data_directories_exist(self):
        for d in (qr.DATA_DIR, qr.ALGEBRA_DIR, qr.NETWORK_DIR):
            self.assertTrue(os.path.isdir(d), d)

    def test_data_files_exist(self):
        for name, _ in ALL_ALGEBRAS:
            path = os.path.join(qr.ALGEBRA_DIR, name + ".json")
            self.assertTrue(os.path.isfile(path), path)
        self.assertTrue(os.path.isfile(os.path.join(qr.NETWORK_DIR, "rcc8_example.json")))


class TestAlgebras(unittest.TestCase):
    """Properties that every algebra must have."""

    @classmethod
    def setUpClass(cls):
        cls.algebras = {name: load_algebra(name) for name, _ in ALL_ALGEBRAS}

    def test_name_and_number_of_relations(self):
        for name, size in ALL_ALGEBRAS:
            with self.subTest(algebra=name):
                alg = self.algebras[name]
                self.assertEqual(alg.name, name)
                self.assertEqual(len(relations(alg.elements)), size)

    def test_composition_identity(self):
        for name, _ in ALL_ALGEBRAS:
            with self.subTest(algebra=name):
                self.assertTrue(quietly(self.algebras[name].check_composition_identity))

    def test_associativity(self):
        for name, _ in ALL_ALGEBRAS:
            with self.subTest(algebra=name):
                self.assertTrue(quietly(self.algebras[name].is_associative))


class TestIntervalNetworks(unittest.TestCase):
    """X B Y and Y D Z, propagated, in each of the interval algebras."""

    # Expected constraint from X to Z.  The left-branching algebra adds LB and LO.
    EXPECTED = {"Linear_Interval_Algebra": {"B", "D", "M", "O", "S"},
                "Extended_Linear_Interval_Algebra": {"B", "D", "M", "O", "S"},
                "Left_Branching_Interval_Algebra": {"B", "D", "LB", "LO", "M", "O", "S"},
                "Right_Branching_Interval_Algebra": {"B", "D", "M", "O", "S"}}

    def test_propagation(self):
        for name, _ in INTERVAL_ALGEBRAS:
            with self.subTest(algebra=name):
                alg = load_algebra(name)
                x = qr.TemporalEntity(["ProperInterval"], "X")
                y = qr.TemporalEntity(["ProperInterval"], "Y")
                z = qr.TemporalEntity(["ProperInterval"], "Z")
                net = qr.Network(alg, f"Network-{name}")
                net.add_constraint(x, y, "B")
                net.add_constraint(y, z, "D")
                self.assertTrue(quietly(net.propagate))
                self.assertEqual(relations(net.get_constraint("X", "Y")), {"B"})
                self.assertEqual(relations(net.get_constraint("Y", "Z")), {"D"})
                self.assertEqual(relations(net.get_constraint("X", "Z")), self.EXPECTED[name])


class TestPointNetworks(unittest.TestCase):
    """X < Y and Y < Z, propagated, in each of the point algebras, implies X < Z."""

    def test_propagation(self):
        for name, _ in POINT_ALGEBRAS:
            with self.subTest(algebra=name):
                alg = load_algebra(name)
                x = qr.TemporalEntity(["Point"], "X")
                y = qr.TemporalEntity(["Point"], "Y")
                z = qr.TemporalEntity(["Point"], "Z")
                net = qr.Network(alg, f"Network-{name}")
                net.add_constraint(x, y, "<")
                net.add_constraint(y, z, "<")
                self.assertTrue(quietly(net.propagate))
                self.assertEqual(relations(net.get_constraint("X", "Z")), {"<"})


class TestRCC8Networks(unittest.TestCase):

    def test_ntpp_is_transitive(self):
        alg = load_algebra("RCC8_Algebra")
        x = qr.SpatialEntity(["Region"], "X")
        y = qr.SpatialEntity(["Region"], "Y")
        z = qr.SpatialEntity(["Region"], "Z")
        net = qr.Network(alg, "Network-RCC8_Algebra")
        net.add_constraint(x, y, "NTPP")
        net.add_constraint(y, z, "NTPP")
        self.assertTrue(quietly(net.propagate))
        self.assertEqual(relations(net.get_constraint("X", "Z")), {"NTPP"})

    def test_wikipedia_example(self):
        """Example from http://en.wikipedia.org/wiki/RCC8, read from a JSON file."""
        net = qr.Network(algebra_path=qr.ALGEBRA_DIR,
                         json_file_name=os.path.join(qr.NETWORK_DIR, "rcc8_example.json"))
        self.assertEqual(len(net.nodes), 5)
        # Before propagation, the constraints between the road and the properties are unknown
        self.assertEqual(len(relations(net.get_constraint("Property1", "Road"))), 8)
        self.assertEqual(len(relations(net.get_constraint("Property2", "Road"))), 8)

        self.assertTrue(quietly(net.propagate))

        # Constraints that were given are unchanged, or were narrowed
        self.assertEqual(relations(net.get_constraint("House1", "House2")), {"DC"})
        self.assertEqual(relations(net.get_constraint("House1", "Property1")), {"NTPP", "TPP"})
        self.assertEqual(relations(net.get_constraint("House1", "Road")), {"EC"})
        self.assertEqual(relations(net.get_constraint("House2", "Property1")), {"DC"})
        self.assertEqual(relations(net.get_constraint("House2", "Property2")), {"NTPP"})
        # Constraints inferred by propagation.  The Wikipedia article gives
        #   road property1: EC|PO      road property2: PO|TPP
        self.assertEqual(relations(net.get_constraint("Property1", "Road")), {"EC", "PO"})
        self.assertEqual(relations(net.get_constraint("Property2", "Road")), {"PO", "TPPI"})
        self.assertEqual(relations(net.get_constraint("Road", "Property1")), {"EC", "PO"})
        self.assertEqual(relations(net.get_constraint("Road", "Property2")), {"PO", "TPP"})


class TestBookExample(unittest.TestCase):
    """Example from the book on constraint processing for temporal reasoning.
    The constraints are inconsistent, and propagation detects that."""

    CONSTRAINTS = [("I", "J", "F|FI"), ("I", "L", "S|M"), ("L", "J", "S|M"),
                   ("K", "I", "D|DI"), ("K", "J", "D|DI"), ("L", "K", "O")]

    def make_network(self, algebra_name, classes):
        ents = {n: qr.TemporalEntity(list(classes), n) for n in "IJKL"}
        net = qr.Network(load_algebra(algebra_name), "Book Example")
        for tail, head, rels in self.CONSTRAINTS:
            net.add_constraint(ents[tail], ents[head], rels)
        return net

    def test_constraints_before_propagation(self):
        net = self.make_network("Linear_Interval_Algebra", ["ProperInterval"])
        self.assertEqual(len(net.nodes), 4)
        self.assertEqual(relations(net.get_constraint("I", "J")), {"F", "FI"})
        self.assertEqual(relations(net.get_constraint("I", "L")), {"S", "M"})
        self.assertEqual(relations(net.get_constraint("L", "K")), {"O"})

    def test_interval_algebra_is_inconsistent(self):
        net = self.make_network("Linear_Interval_Algebra", ["ProperInterval"])
        self.assertFalse(quietly(net.propagate))

    def test_extended_algebra_is_inconsistent(self):
        net = self.make_network("Extended_Linear_Interval_Algebra", ["Point", "ProperInterval"])
        self.assertFalse(quietly(net.propagate))


class TestSignatureTables(unittest.TestCase):
    """The tables that connect 4-point network signatures to relation names."""

    def test_name_signature_mapping_is_the_inverse(self):
        self.assertEqual(len(qr.signature_name_mapping), len(qr.name_signature_mapping))
        for name, signature in qr.name_signature_mapping.items():
            with self.subTest(relation=name):
                self.assertEqual(len(signature), 4)
                self.assertEqual(qr.signature_name_mapping[",".join(signature)], name)

    def test_every_relation_has_a_long_name(self):
        self.assertEqual(set(qr.signature_name_mapping.values()), set(qr.relation_long_names))

    def test_long_names_agree_with_the_shipped_algebras(self):
        for name, _ in INTERVAL_ALGEBRAS:
            alg = load_algebra(name)
            for rel in alg.elements:
                with self.subTest(algebra=name, relation=rel):
                    self.assertEqual(alg.rel_name(rel), qr.relation_long_names[rel])


class TestFourAndSixPointNets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pt = load_algebra("Linear_Point_Algebra")

    def test_four_point_net(self):
        net = qr.FourPointNet(self.pt, "FP", "<")
        self.assertEqual(net.name_list, ["StartPt1", "EndPt1", "StartPt2", "EndPt2"])
        points = net.get_points()
        self.assertEqual([p.name for p in points], net.name_list)
        self.assertTrue(all(p.classes == ["Point"] for p in points))
        # Each interval's start is before its end ...
        self.assertEqual(net.get_constraint("StartPt1", "EndPt1"), "<")
        self.assertEqual(net.get_constraint("EndPt1", "StartPt1"), ">")
        self.assertEqual(net.get_constraint("StartPt2", "EndPt2"), "<")
        # ... and nothing is said, yet, about how the two intervals relate
        self.assertFalse(net.has_edge(points[0], points[2]))
        self.assertFalse(net.has_edge(points[1], points[3]))

    def test_six_point_net(self):
        net = qr.SixPointNet(self.pt, "<", "B", "D")
        self.assertEqual(net.name_list, ["StartPt1", "EndPt1", "StartPt2", "EndPt2",
                                         "StartPt3", "EndPt3"])
        self.assertEqual([p.name for p in net.get_points()], net.name_list)
        self.assertEqual(net.name, "B;D")
        for i in (1, 2, 3):
            self.assertEqual(net.get_constraint(f"StartPt{i}", f"EndPt{i}"), "<")
        # Interval 1 is before interval 2:  B is signature <,<,<,<
        for start_or_end_1 in ("StartPt1", "EndPt1"):
            for start_or_end_2 in ("StartPt2", "EndPt2"):
                self.assertEqual(net.get_constraint(start_or_end_1, start_or_end_2), "<")
        # Interval 2 is during interval 3:  D is signature >,<,>,<
        self.assertEqual(net.get_constraint("StartPt2", "StartPt3"), ">")
        self.assertEqual(net.get_constraint("StartPt2", "EndPt3"), "<")
        self.assertEqual(net.get_constraint("EndPt2", "StartPt3"), ">")
        self.assertEqual(net.get_constraint("EndPt2", "EndPt3"), "<")
        # How interval 1 relates to interval 3 is what is to be derived, so it starts out open
        self.assertEqual(relations(net.get_constraint("StartPt1", "StartPt3")), {"<", "=", ">"})


class TestGenerateConsistentNetworks(unittest.TestCase):

    def check(self, point_alg_name, less_than, interval_alg_name):
        pt = load_algebra(point_alg_name)
        target = load_algebra(interval_alg_name)
        nets = quietly(qr.generate_consistent_networks, pt, lessthan=less_than)
        # One consistent network for each relation of the interval algebra
        self.assertEqual(set(nets), relations(target.elements))
        for rel, net in nets.items():
            with self.subTest(relation=rel):
                self.assertIsInstance(net, qr.FourPointNet)
                domain, range_ = net.domain_and_range()
                self.assertEqual(set(domain), set(target.rel_domain(rel)))
                self.assertEqual(set(range_), set(target.rel_range(rel)))
        return nets

    def test_linear_points_give_allens_13(self):
        nets = self.check("Linear_Point_Algebra", "<", "Linear_Interval_Algebra")
        self.assertEqual(len(nets), 13)

    def test_linear_points_with_less_than_or_equal_give_18(self):
        nets = self.check("Linear_Point_Algebra", "<|=", "Extended_Linear_Interval_Algebra")
        self.assertEqual(len(nets), 18)
        # The extra relations are the ones that involve points
        self.assertEqual(nets["PE"].domain_and_range(), (["Point"], ["Point"]))
        self.assertEqual(nets["PS"].domain_and_range(), (["Point"], ["ProperInterval"]))
        self.assertEqual(nets["PFI"].domain_and_range(), (["ProperInterval"], ["Point"]))

    def test_branching_points_give_24(self):
        for point_alg, interval_alg in [("Right_Branching_Point_Algebra",
                                         "Right_Branching_Interval_Algebra"),
                                        ("Left_Branching_Point_Algebra",
                                         "Left_Branching_Interval_Algebra")]:
            with self.subTest(algebra=point_alg):
                self.assertEqual(len(self.check(point_alg, "<|=", interval_alg)), 24)

    def test_signatures_match_the_mapping(self):
        """The top-right 2x2 block of a 4-point network, read as text, is the relation's
        signature."""
        pt = load_algebra("Linear_Point_Algebra")
        nets = quietly(qr.generate_consistent_networks, pt)
        for rel, net in nets.items():
            with self.subTest(relation=rel):
                self.assertEqual(net.get_2x2_partition_constraints(0, 2, net.name_list),
                                 ",".join(qr.name_signature_mapping[rel]))


class TestDeriveComposition(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pt = load_algebra("Linear_Point_Algebra")

    def test_known_compositions(self):
        # (relation 1, relation 2, their composition)
        for r1, r2, expected in [("B", "B", "B"),
                                 ("B", "D", "B|D|M|O|S"),
                                 ("M", "M", "B"),
                                 ("O", "O", "B|M|O"),
                                 ("E", "D", "D"),
                                 ("D", "E", "D"),
                                 ("B", "BI", "B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI")]:
            with self.subTest(composition=f"{r1};{r2}"):
                with recursion_limit(10000):
                    result = qr.derive_composition(self.pt, "<", r1, r2)
                self.assertEqual(relations(result), relations(expected))

    def test_composition_table(self):
        with recursion_limit(10000):
            table = qr.derive_composition_table(self.pt, "<", ["B", "E"])
        self.assertEqual(table, {"B": {"B": "B", "E": "B"},
                                 "E": {"B": "B", "E": "E"}})


class TestDeriveAlgebra(unittest.TestCase):
    """Deriving Allen's algebra from the linear point algebra gives the algebra in
    data/algebras/Linear_Interval_Algebra.json, relation for relation and table entry for
    table entry."""

    @classmethod
    def setUpClass(cls):
        cls.pt = load_algebra("Linear_Point_Algebra")
        cls.allen = load_algebra("Linear_Interval_Algebra")
        with recursion_limit(10000):
            cls.derived = quietly(qr.derive_algebra, cls.pt, "<",
                                  name="Derived", description="Derived for a test")
            cls.nets = quietly(qr.generate_consistent_networks, cls.pt)
        cls.table = cls.derived["TransTable"]

    def test_algebra_dict_contents(self):
        self.assertEqual(set(self.derived), {"Name", "Description", "Relations", "TransTable"})
        self.assertEqual(self.derived["Name"], "Derived")
        self.assertEqual(self.derived["Description"], "Derived for a test")
        self.assertEqual(len(self.derived["Relations"]), 13)
        self.assertEqual(len(self.derived["TransTable"]), 13)

    def test_matches_the_shipped_algebra(self):
        self.assertEqual(self.derived["Relations"], self.allen.algebra_dict["Relations"])
        self.assertEqual(self.derived["TransTable"], self.allen.algebra_dict["TransTable"])
        self.assertTrue(qr.Algebra(alg_dict=self.derived).equivalent_algebra(self.allen))

    def test_derived_algebra_is_sound(self):
        alg = qr.Algebra(alg_dict=self.derived)
        self.assertEqual(alg.name, "Derived")
        self.assertTrue(quietly(alg.check_composition_identity))
        self.assertTrue(quietly(alg.is_associative))

    def test_relation_info(self):
        for rel in ("B", "E", "O", "D"):
            with self.subTest(relation=rel):
                info = qr.derive_relation_info(rel, self.nets[rel], self.nets, self.table)
                self.assertEqual(info, self.allen.algebra_dict["Relations"][rel])

    def test_relation_dict(self):
        rel_dict = qr.derive_relation_dict(self.nets, self.table)
        self.assertEqual(rel_dict, self.allen.algebra_dict["Relations"])

    def test_reflexive_symmetric_transitive(self):
        names = sorted(self.nets)
        self.assertEqual({r for r in names if qr.is_reflexive(r, self.nets)}, {"E"})
        self.assertEqual({r for r in names if qr.is_symmetric(r, self.nets)}, {"E"})
        self.assertEqual({r for r in names if qr.is_transitive(r, self.table)},
                         {"B", "BI", "D", "DI", "E", "F", "FI", "S", "SI"})

    def test_json_file_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "derived.json")
            qr.algebra_to_json_file(self.derived, path)
            with open(path) as f:
                self.assertEqual(json.load(f), self.derived)
            self.assertTrue(qr.Algebra(path).equivalent_algebra(self.allen))

    @skip_unless_slow
    def test_other_derivations_match_the_shipped_algebras(self):
        """Extended Linear (18 relations), then Right and Left Branching (24 relations each)."""
        for point_alg, less_than, interval_alg in DERIVATIONS[1:]:
            with self.subTest(derive=interval_alg):
                with recursion_limit(10000):
                    derived = quietly(qr.derive_algebra, load_algebra(point_alg), less_than,
                                      name=interval_alg, description="test")
                self.assertTrue(qr.Algebra(alg_dict=derived)
                                .equivalent_algebra(load_algebra(interval_alg)))


class TestNetworkRoundTrip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.alg = load_algebra("Linear_Interval_Algebra")

    def test_to_dict(self):
        net = make_chain(self.alg, "Chain")
        d = net.to_dict()
        self.assertEqual(d["name"], "Chain")
        self.assertEqual(d["algebra"], "Linear_Interval_Algebra")
        self.assertEqual({name: classes for name, classes in d["nodes"]},
                         {"X": ["ProperInterval"], "Y": ["ProperInterval"],
                          "Z": ["ProperInterval"]})
        # One edge for each pair of nodes: no self edges and no converse edges
        self.assertEqual(len(d["edges"]), 3)
        self.assertEqual({frozenset(edge[:2]) for edge in d["edges"]},
                         {frozenset("XY"), frozenset("YZ"), frozenset("XZ")})
        for tail, head, constraint in d["edges"]:
            self.assertEqual(net.get_constraint(tail, head), constraint)

    def test_round_trip_with_algebra_object(self):
        net = make_chain(self.alg)
        copy = qr.Network(algebra=self.alg, network_dict=net.to_dict())
        self.assertEqual(copy.name, net.name)
        self.assertEqual(constraints_by_name(copy), constraints_by_name(net))

    def test_round_trip_finding_the_algebra_by_name(self):
        net = make_chain(self.alg)
        copy = qr.Network(algebra_path=qr.ALGEBRA_DIR, network_dict=net.to_dict())
        self.assertEqual(copy.algebra.name, "Linear_Interval_Algebra")
        self.assertEqual(constraints_by_name(copy), constraints_by_name(net))

    def test_round_trip_through_a_json_file(self):
        net = make_chain(self.alg)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "chain.json")
            with open(path, "w") as f:
                json.dump(net.to_dict(), f)
            copy = qr.Network(algebra_path=qr.ALGEBRA_DIR, json_file_name=path)
        self.assertEqual(constraints_by_name(copy), constraints_by_name(net))

    def test_round_trip_of_the_rcc8_example(self):
        net = qr.Network(algebra_path=qr.ALGEBRA_DIR,
                         json_file_name=os.path.join(qr.NETWORK_DIR, "rcc8_example.json"))
        self.assertTrue(quietly(net.propagate))
        copy = qr.Network(algebra_path=qr.ALGEBRA_DIR, network_dict=net.to_dict())
        self.assertEqual(len(copy.nodes), 5)
        self.assertTrue(all(isinstance(node, qr.SpatialEntity) for node in copy.nodes))
        self.assertEqual(constraints_by_name(copy), constraints_by_name(net))

    def test_network_dict_with_abbreviations_and_an_unconstrained_edge(self):
        net_dict = {"name": "FromDict",
                    "description": "Built from a dictionary",
                    "algebra": "Linear_Interval_Algebra",
                    "nodes": [["A", ["ProperInterval"]], ["B", ["ProperInterval"]],
                              ["C", ["ProperInterval"]]],
                    "abbreviations": {"bm": "B|M"},
                    "edges": [["A", "B", "bm"], ["B", "C", "D"], ["A", "C"]]}
        net = qr.Network(algebra=self.alg, network_dict=net_dict)
        self.assertEqual(net.name, "FromDict")
        self.assertEqual(net.description, "Built from a dictionary")
        self.assertEqual(relations(net.get_constraint("A", "B")), {"B", "M"})
        self.assertEqual(relations(net.get_constraint("B", "C")), {"D"})
        # An edge without a constraint allows every relation
        self.assertEqual(relations(net.get_constraint("A", "C")), relations(self.alg.elements))

    def test_network_dict_entity_types(self):
        net_dict = {"name": "Types", "algebra": "Linear_Point_Algebra",
                    "nodes": [["P", ["Point"]], ["Q", ["Point"]]],
                    "edges": [["P", "Q", "<"]]}
        net = qr.Network(algebra_path=qr.ALGEBRA_DIR, network_dict=net_dict)
        self.assertTrue(all(isinstance(node, qr.TemporalEntity) for node in net.nodes))
        self.assertEqual(net.get_constraint("P", "Q"), "<")
        self.assertEqual(net.get_constraint("Q", "P"), ">")


class TestNetworkCopyAndCombine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.alg = load_algebra("Linear_Interval_Algebra")

    def test_mostly_copy(self):
        net = make_chain(self.alg)
        copy = net.mostly_copy()
        self.assertIsNot(copy, net)
        self.assertIs(copy.algebra, net.algebra)        # the algebra is shared ...
        self.assertEqual(constraints_by_name(copy), constraints_by_name(net))
        for node in copy.nodes:                          # ... but the entities are not
            self.assertTrue(all(node is not original for original in net.nodes))

    def test_changing_a_copy_leaves_the_original_alone(self):
        net = make_chain(self.alg)
        before = constraints_by_name(net)
        copy = net.mostly_copy()
        x, z = copy.get_entity("X"), copy.get_entity("Z")
        copy.set_constraint(x, z, self.alg.relset("B"))
        self.assertEqual(copy.get_constraint("X", "Z"), "B")
        self.assertEqual(constraints_by_name(net), before)

    def test_adding_disjoint_networks(self):
        a, b = qr.Network(self.alg, "A"), qr.Network(self.alg, "B")
        p, q = intervals("pq")
        r, s = intervals("rs")
        a.add_constraint(p, q, "B")
        b.add_constraint(r, s, "D")
        combined = a + b
        self.assertEqual(combined.name, "A+B")
        self.assertIs(combined.algebra, self.alg)
        self.assertEqual({n.name for n in combined.nodes}, {"p", "q", "r", "s"})
        self.assertEqual(len(combined.edges), 8)         # 4 self edges + 2 edges each way
        self.assertEqual(combined.get_constraint("p", "q"), "B")
        self.assertEqual(combined.get_constraint("s", "r"), "DI")
        # The networks that were added are not changed
        self.assertEqual({n.name for n in a.nodes}, {"p", "q"})
        self.assertEqual({n.name for n in b.nodes}, {"r", "s"})

    def test_adding_networks_that_share_an_entity(self):
        a, b = qr.Network(self.alg, "A"), qr.Network(self.alg, "B")
        p, q, r = intervals("pqr")
        a.add_constraint(p, q, "B")
        b.add_constraint(q, r, "D")
        combined = a + b
        self.assertEqual({n.name for n in combined.nodes}, {"p", "q", "r"})
        self.assertEqual(len(combined.edges), 7)         # 3 self edges + 2 edges each way
        # Nothing is known about p and r until the combined network is propagated
        self.assertFalse(combined.has_edge(p, r))
        self.assertTrue(quietly(combined.propagate))
        self.assertEqual(relations(combined.get_constraint("p", "r")), {"B", "D", "M", "O", "S"})


class TestNetworkEditing(unittest.TestCase):
    """The small methods that read and change a network's constraints."""

    @classmethod
    def setUpClass(cls):
        cls.alg = load_algebra("Linear_Interval_Algebra")

    def test_set_constraint_sets_the_converse_too(self):
        net = make_chain(self.alg)
        x, z = net.get_entity("X"), net.get_entity("Z")
        net.set_constraint(x, z, self.alg.relset("B|M"))
        self.assertEqual(relations(net.get_constraint("X", "Z")), {"B", "M"})
        self.assertEqual(relations(net.get_constraint("Z", "X")), {"BI", "MI"})

    def test_set_constraint_on_an_equality_edge(self):
        net = make_chain(self.alg)
        x = net.get_entity("X")
        net.set_constraint(x, x, self.alg.relset("E"))
        self.assertEqual(net.get_constraint("X", "X"), "E")

    def test_remove_constraint_removes_both_directions(self):
        net = make_chain(self.alg)
        x, y = net.get_entity("X"), net.get_entity("Y")
        net.remove_constraint(x, y)
        self.assertFalse(net.has_edge(x, y))
        self.assertFalse(net.has_edge(y, x))
        self.assertEqual(len(net.nodes), 3)              # the entities are still there
        self.assertEqual(relations(net.get_constraint("Y", "Z")), {"D"})
        net.remove_constraint(x, y)                      # nothing left to remove; no error

    def test_get_entities_keeps_the_order_asked_for(self):
        net = make_chain(self.alg)
        self.assertEqual([e.name for e in net.get_entities(["Z", "X", "Y"])], ["Z", "X", "Y"])
        self.assertIsNone(net.get_entity("No such entity"))

    def test_get_edge(self):
        net = make_chain(self.alg)
        self.assertEqual(net.get_edge("X", "Y"), ("X", "Y", "B"))
        source, target, constraint = net.get_edge("Y", "Z", return_names=False)
        self.assertIs(source, net.get_entity("Y"))
        self.assertIs(target, net.get_entity("Z"))
        self.assertEqual(constraint, "D")

    def test_to_list(self):
        net = make_chain(self.alg)
        as_sets = lambda rows: [[relations(cell) for cell in row] for row in rows]
        after = {"BI", "DI", "MI", "OI", "SI"}
        self.assertEqual(as_sets(net.to_list()),
                         [[{"E"}, {"B"}, {"B", "D", "M", "O", "S"}],
                          [{"BI"}, {"E"}, {"D"}],
                          [after, {"DI"}, {"E"}]])
        # The rows and columns can be put in any order
        z, x = net.get_entity("Z"), net.get_entity("X")
        self.assertEqual(as_sets(net.to_list([z, x])),
                         [[{"E"}, after],
                          [{"B", "D", "M", "O", "S"}, {"E"}]])


class TestSingletonLabelings(unittest.TestCase):
    """Expanding a network's disjunctive constraints into networks that have one relation on
    every edge."""

    @classmethod
    def setUpClass(cls):
        cls.alg = load_algebra("Linear_Interval_Algebra")

    def open_edge_network(self):
        net = qr.Network(self.alg, "Open")
        a, b = intervals("ab")
        net.add_constraint(a, b, "B|M|O")
        return net

    def test_has_only_singleton_constraints(self):
        net = qr.Network(self.alg, "Singletons")
        a, b = intervals("ab")
        net.add_constraint(a, b, "B")
        self.assertTrue(net.has_only_singleton_constraints())
        self.assertFalse(self.open_edge_network().has_only_singleton_constraints())

    def test_next_singleton_labelings(self):
        net = self.open_edge_network()
        expansion = net.next_singleton_labelings()
        self.assertEqual(len(expansion), 3)
        self.assertEqual(sorted(str(n.get_constraint("a", "b")) for n in expansion),
                         ["B", "M", "O"])
        self.assertEqual(sorted(str(n.get_constraint("b", "a")) for n in expansion),
                         ["BI", "MI", "OI"])
        for labeled in expansion:
            self.assertTrue(labeled.has_only_singleton_constraints())
            self.assertIs(labeled.algebra, net.algebra)
        # The network itself is not changed
        self.assertEqual(relations(net.get_constraint("a", "b")), {"B", "M", "O"})
        self.assertFalse(net.has_only_singleton_constraints())

    def test_nothing_to_expand_when_every_constraint_is_a_singleton(self):
        net = qr.Network(self.alg, "Singletons")
        a, b = intervals("ab")
        net.add_constraint(a, b, "B")
        self.assertEqual(net.next_singleton_labelings(), [])
        labelings = net.all_singleton_labelings()
        self.assertEqual(len(labelings), 1)
        self.assertEqual(constraints_by_name(labelings[0]), constraints_by_name(net))

    def test_all_singleton_labelings_of_one_open_edge(self):
        net = self.open_edge_network()
        labelings = net.all_singleton_labelings()
        self.assertEqual(len(labelings), 3)
        self.assertTrue(all(n.has_only_singleton_constraints() for n in labelings))
        self.assertEqual(sorted(str(n.get_constraint("a", "b")) for n in labelings),
                         ["B", "M", "O"])

    def test_all_singleton_labelings_of_several_open_edges(self):
        net = qr.Network(self.alg, "Triangle")
        a, b, c = intervals("abc")
        for tail, head in [(a, b), (b, c), (a, c)]:
            net.add_constraint(tail, head, "B|M")
        labelings = net.all_singleton_labelings()
        self.assertEqual(len(labelings), 8)              # 2 x 2 x 2
        self.assertEqual(len({tuple(sorted(constraints_by_name(n).items())) for n in labelings}), 8)

    def test_consistent_singleton_labelings(self):
        """a B|M b, b B|M c and a B|M c.  Whichever of B or M is chosen for a-b and for b-c,
        a is before c, so only 4 of the 8 labelings are consistent."""
        net = qr.Network(self.alg, "Triangle")
        a, b, c = intervals("abc")
        for tail, head in [(a, b), (b, c), (a, c)]:
            net.add_constraint(tail, head, "B|M")
        consistent = net.consistent_singleton_labelings()
        self.assertEqual(len(consistent), 4)
        for labeled in consistent:
            self.assertEqual(relations(labeled.get_constraint("a", "c")), {"B"})

    def test_inconsistent_labeling_is_dropped(self):
        net = qr.Network(self.alg, "Chain")
        x, y, z = intervals("xyz")
        net.add_constraint(x, y, "B")
        net.add_constraint(y, z, "B")
        net.add_constraint(x, z, "B|BI")
        self.assertEqual(len(net.all_singleton_labelings()), 2)
        consistent = net.consistent_singleton_labelings()
        self.assertEqual(len(consistent), 1)
        self.assertEqual(consistent[0].get_constraint("x", "z"), "B")

    def test_get_submatrix_constraints(self):
        net = make_chain(self.alg)
        names = ["X", "Y", "Z"]
        result = net.get_submatrix_constraints([0, 1], [1, 2], names)
        self.assertEqual([relations(r) for r in result],
                         [{"B"}, {"B", "D", "M", "O", "S"}, {"E"}, {"D"}])
        # Rows and columns need not be next to each other, or in order
        result = net.get_submatrix_constraints([2, 0], [0], names)
        self.assertEqual([relations(r) for r in result],
                         [{"BI", "DI", "MI", "OI", "SI"}, {"E"}])

    def test_get_2x2_partition_constraints(self):
        net = make_chain(self.alg)
        result = net.get_2x2_partition_constraints(0, 1, ["X", "Y", "Z"])
        self.assertEqual([relations(r) for r in result.split(",")],
                         [{"B"}, {"B", "D", "M", "O", "S"}, {"E"}, {"D"}])


class TestAlgebraConstruction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.allen = load_algebra("Linear_Interval_Algebra")
        cls.points = load_algebra("Linear_Point_Algebra")

    def test_name_and_description_come_from_the_file(self):
        self.assertEqual(self.allen.name, "Linear_Interval_Algebra")
        self.assertTrue(self.allen.description)
        self.assertEqual(str(self.allen), f"<{self.allen.name}: {self.allen.description}>")

    def test_from_a_dictionary_without_name_or_description(self):
        alg_dict = {"Relations": self.allen.algebra_dict["Relations"],
                    "TransTable": self.allen.algebra_dict["TransTable"]}
        alg = qr.Algebra(alg_dict=alg_dict)
        self.assertTrue(alg.name.startswith("Algebra:"))
        self.assertEqual(alg.description, "No description provided.")
        self.assertEqual(relations(alg.elements), relations(self.allen.elements))
        self.assertTrue(alg.equivalent_algebra(self.allen))

    def test_table_entries_can_be_lists(self):
        """The original transitivity table format used lists; the compact one uses strings."""
        table = {r1: {r2: str(self.points.transitivity_table[r1][r2]).split("|")
                         if str(self.points.transitivity_table[r1][r2]) else []
                      for r2 in self.points.elements}
                 for r1 in self.points.elements}
        alg = qr.Algebra(alg_dict={"Name": "ListTable",
                                   "Relations": self.points.algebra_dict["Relations"],
                                   "TransTable": table})
        for r1, r2 in itertools.product(alg.elements, repeat=2):
            self.assertEqual(alg.transitivity_table[r1][r2], self.points.transitivity_table[r1][r2])

    def test_a_bad_table_entry_is_rejected(self):
        with self.assertRaisesRegex(Exception, "Bad entry in transitivity table"):
            qr.Algebra(alg_dict={"Relations": self.points.algebra_dict["Relations"],
                                 "TransTable": {"<": {"<": 5}}})

    def test_an_empty_string_in_the_table_is_the_empty_relation_set(self):
        alg = tampered("Linear_Point_Algebra", "<", "<", "")
        self.assertEqual(str(alg.transitivity_table["<"]["<"]), "")
        self.assertEqual(str(alg.compose(alg.relset("<"), alg.relset("<"))), "")

    def test_equivalent_algebra(self):
        self.assertTrue(self.allen.equivalent_algebra(load_algebra("Linear_Interval_Algebra")))
        self.assertFalse(self.allen.equivalent_algebra(load_algebra("Extended_Linear_Interval_Algebra")))
        # A change to one composition, or to one relation, makes algebras differ
        self.assertFalse(self.allen.equivalent_algebra(
            tampered("Linear_Interval_Algebra", "B", "B", "M")))
        alg_dict = copy.deepcopy(self.allen.algebra_dict)
        alg_dict["Relations"]["B"]["Name"] = "Earlier"
        self.assertFalse(self.allen.equivalent_algebra(qr.Algebra(alg_dict=alg_dict)))


class TestAlgebraAccessors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.allen = load_algebra("Linear_Interval_Algebra")
        cls.extended = load_algebra("Extended_Linear_Interval_Algebra")

    def test_relation_information(self):
        self.assertEqual(self.allen.rel_name("B"), "Before")
        self.assertEqual(self.allen.rel_converse_name("B"), "After")
        self.assertEqual(self.allen.rel_domain("B"), ["ProperInterval"])
        self.assertEqual(self.allen.rel_range("B"), ["ProperInterval"])
        self.assertEqual(self.extended.rel_domain("PS"), ["Point"])
        self.assertEqual(self.extended.rel_range("PS"), ["ProperInterval"])

    def test_equality_is_reflexive_symmetric_and_transitive(self):
        self.assertTrue(self.allen.rel_reflexive("E"))
        self.assertTrue(self.allen.rel_symmetric("E"))
        self.assertTrue(self.allen.rel_transitive("E"))
        self.assertTrue(self.allen.rel_equality("E"))
        self.assertFalse(self.allen.rel_equality("B"))      # transitive only
        self.assertTrue(self.allen.rel_transitive("B"))

    def test_equality_relations_of_each_algebra(self):
        expected = {"Linear_Interval_Algebra": {"E"},
                    "Extended_Linear_Interval_Algebra": {"E", "PE"},
                    "RCC8_Algebra": {"EQ"},
                    "Linear_Point_Algebra": {"="}}
        for name, equalities in expected.items():
            with self.subTest(algebra=name):
                self.assertEqual(relations(load_algebra(name).all_equality_relations), equalities)

    def test_equality_relation_of_each_class(self):
        self.assertEqual(relations(self.allen.get_domain_or_range_equality_rel("ProperInterval")),
                         {"E"})
        self.assertEqual(relations(self.extended.get_domain_or_range_equality_rel("Point")),
                         {"PE"})
        self.assertEqual(relations(self.extended.get_domain_or_range_equality_rel("ProperInterval")),
                         {"E"})
        with self.assertRaises(KeyError):
            self.allen.get_domain_or_range_equality_rel("Point")

    def test_domain_and_range_classes_of_a_relation_set(self):
        # (relation set, domain classes, range classes)
        for relset, domain, range_ in [("PE", {"Point"}, {"Point"}),
                                       ("E", {"ProperInterval"}, {"ProperInterval"}),
                                       ("PE|E", {"Point", "ProperInterval"},
                                        {"Point", "ProperInterval"}),
                                       ("PS", {"Point"}, {"ProperInterval"}),
                                       ("PFI", {"ProperInterval"}, {"Point"})]:
            with self.subTest(relset=relset):
                self.assertEqual(self.extended.get_domain_classes(relset), domain)
                self.assertEqual(self.extended.get_range_classes(relset), range_)


class TestRelSetOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.allen = load_algebra("Linear_Interval_Algebra")
        cls.algebras = {name: load_algebra(name) for name, _ in ALL_ALGEBRAS}

    def test_relset_from_every_kind_of_input(self):
        for given, expected in [("B|M", {"B", "M"}), (["B", "M"], {"B", "M"}), (("B",), {"B"}),
                                ({"B", "M"}, {"B", "M"}), ("", set()), ([], set())]:
            with self.subTest(given=given):
                self.assertEqual(relations(self.allen.relset(given)), expected)

    def test_relset_rejects_bad_input(self):
        for bad in (5, 3.5, None):
            with self.subTest(given=bad):
                with self.assertRaises(TypeError):
                    self.allen.relset(bad)
        with self.assertRaises(KeyError):
            self.allen.relset("ZZ")

    def test_string_to_relset_with_another_delimiter(self):
        self.assertEqual(relations(self.allen.string_to_relset("B,M", delimiter=",")), {"B", "M"})

    def test_relset_text_and_intersection(self):
        self.assertEqual(str(self.allen.relset("B|M")), "B|M")
        self.assertEqual(str(self.allen.relset([])), "")
        # + is intersection
        self.assertEqual(relations(self.allen.relset("B|M") + self.allen.relset("M|O")), {"M"})
        self.assertEqual(str(self.allen.relset("B") + self.allen.relset("M")), "")

    def test_converse_of_a_relation_and_of_a_relation_set(self):
        self.assertEqual(self.allen.converse("B"), "BI")
        self.assertEqual(self.allen.converse("E"), "E")
        converse = self.allen.converse(self.allen.relset("B|M"))
        self.assertIsInstance(converse, qr.RelSet)
        self.assertEqual(relations(converse), {"BI", "MI"})
        self.assertEqual(str(self.allen.converse(self.allen.relset([]))), "")

    def test_converse_of_converse_is_the_relation_itself(self):
        for name, alg in self.algebras.items():
            with self.subTest(algebra=name):
                for rel in alg.elements:
                    self.assertEqual(alg.converse(alg.converse(rel)), rel)

    def test_compose(self):
        self.assertEqual(relations(self.allen.compose(self.allen.relset("B"),
                                                      self.allen.relset("D"))),
                         {"B", "D", "M", "O", "S"})
        # Composing with the empty relation set gives the empty relation set
        self.assertEqual(str(self.allen.compose(self.allen.relset([]), self.allen.relset("B"))), "")
        self.assertEqual(str(self.allen.compose(self.allen.relset("B"), self.allen.relset([]))), "")

    def test_compose_distributes_over_union(self):
        both = self.allen.compose(self.allen.relset("B|M"), self.allen.relset("D"))
        separately = (self.allen.compose(self.allen.relset("B"), self.allen.relset("D"))
                      .union(self.allen.compose(self.allen.relset("M"), self.allen.relset("D"))))
        self.assertEqual(both, separately)

    def test_equality_is_the_identity_for_composition(self):
        for rel in self.allen.elements:
            with self.subTest(relation=rel):
                relset = self.allen.relset([rel])
                self.assertEqual(self.allen.compose(self.allen.relset("E"), relset), relset)
                self.assertEqual(self.allen.compose(relset, self.allen.relset("E")), relset)


class TestAddConstraint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.alg = load_algebra("Linear_Interval_Algebra")

    def setUp(self):
        self.net = qr.Network(self.alg, "Net")
        self.x, self.y = intervals("xy")

    def test_constraint_as_a_string(self):
        self.net.add_constraint(self.x, self.y, "B|M")
        self.assertEqual(relations(self.net.get_constraint("x", "y")), {"B", "M"})
        self.assertEqual(relations(self.net.get_constraint("y", "x")), {"BI", "MI"})

    def test_constraint_as_a_relset(self):
        self.net.add_constraint(self.x, self.y, self.alg.relset("B|M"))
        self.assertEqual(relations(self.net.get_constraint("x", "y")), {"B", "M"})
        self.assertEqual(relations(self.net.get_constraint("y", "x")), {"BI", "MI"})

    def test_no_constraint_allows_every_relation(self):
        self.net.add_constraint(self.x, self.y)
        self.assertEqual(relations(self.net.get_constraint("x", "y")), relations(self.alg.elements))
        self.assertEqual(relations(self.net.get_constraint("y", "x")), relations(self.alg.elements))

    def test_constraint_of_the_wrong_type(self):
        for bad in (42, ["B", "M"], 3.5):
            with self.subTest(given=bad):
                with self.assertRaisesRegex(TypeError, "relation_set must be"):
                    self.net.add_constraint(self.x, self.y, bad)

    def test_a_new_constraint_replaces_the_old_one(self):
        self.net.add_constraint(self.x, self.y, "B")
        self.net.add_constraint(self.x, self.y, "D")
        self.assertEqual(self.net.get_constraint("x", "y"), "D")
        self.assertEqual(self.net.get_constraint("y", "x"), "DI")
        self.assertEqual(len(self.net.edges), 4)       # two self edges and one edge each way

    def test_every_entity_is_equal_to_itself(self):
        self.net.add_constraint(self.x, self.y, "B")
        self.assertEqual(self.net.get_constraint("x", "x"), "E")
        self.assertEqual(self.net.get_constraint("y", "y"), "E")

    def test_equality_of_an_entity_depends_on_its_classes(self):
        extended = load_algebra("Extended_Linear_Interval_Algebra")
        net = qr.Network(extended, "Classes")
        either = qr.TemporalEntity(["Point", "ProperInterval"], "either")
        point = qr.TemporalEntity(["Point"], "point")
        interval = qr.TemporalEntity(["ProperInterval"], "interval")
        net.add_constraint(either, point, "PE|PS")
        net.add_constraint(point, interval, "PS")
        self.assertEqual(relations(net.get_constraint("either", "either")), {"E", "PE"})
        self.assertEqual(relations(net.get_constraint("point", "point")), {"PE"})
        self.assertEqual(relations(net.get_constraint("interval", "interval")), {"E"})

    def test_entity_with_an_unknown_class(self):
        with self.assertRaises(KeyError):
            self.net.add_constraint(qr.TemporalEntity(["Region"], "r"), self.y, "B")

    def test_verbose_output(self):
        _, text = capturing(self.net.add_constraint, self.x, self.y, "B|M", True)
        self.assertEqual(text.splitlines(),
                         ["Equality Constraint Added: x ['E']",
                          "Equality Constraint Added: y ['E']",
                          "Constraint Added: x y ['B', 'M']",
                          "Constraint Added: y x ['BI', 'MI']"])
        # The equality constraints exist now, so they are not announced a second time
        _, text = capturing(self.net.add_constraint, self.x, self.y, "B", True)
        self.assertEqual(text.splitlines(), ["Constraint Added: x y ['B']",
                                             "Constraint Added: y x ['BI']"])

    def test_quiet_by_default(self):
        _, text = capturing(self.net.add_constraint, self.x, self.y, "B")
        self.assertEqual(text, "")


class TestNetworkConstruction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.alg = load_algebra("Linear_Interval_Algebra")

    def test_empty_network(self):
        net = qr.Network(self.alg)
        self.assertEqual(len(net.nodes), 0)
        self.assertTrue(net.name.startswith("Network:"))
        self.assertIs(net.algebra, self.alg)
        self.assertEqual(str(net), f"<Network--{net.name}--Linear_Interval_Algebra>")
        self.assertTrue(quietly(net.propagate))         # nothing to be inconsistent about

    def test_name_given_to_the_constructor(self):
        self.assertEqual(qr.Network(self.alg, "Mine").name, "Mine")

    def test_dictionary_without_name_or_description(self):
        net_dict = {"nodes": [["A", ["ProperInterval"]]], "edges": []}
        net = qr.Network(algebra=self.alg, network_dict=net_dict, name="Given")
        self.assertEqual(net.name, "Given")
        self.assertEqual(net.description, "None provided")
        unnamed = qr.Network(algebra=self.alg, network_dict=net_dict)
        self.assertTrue(unnamed.name.startswith("Network:"))

    def test_the_dictionary_names_the_network(self):
        net_dict = {"name": "FromDict", "nodes": [], "edges": []}
        net = qr.Network(algebra=self.alg, network_dict=net_dict, name="Ignored")
        self.assertEqual(net.name, "FromDict")


class TestPropagate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.alg = load_algebra("Linear_Interval_Algebra")
        cls.extended = load_algebra("Extended_Linear_Interval_Algebra")

    def chain(self):
        x, y, z = intervals("XYZ")
        net = qr.Network(self.alg, "Chain")
        net.add_constraint(x, y, "B")
        net.add_constraint(y, z, "D")
        return net

    def test_quiet_unless_verbose(self):
        result, text = capturing(self.chain().propagate)
        self.assertTrue(result)
        self.assertEqual(text, "")

    def test_verbose_reports_the_number_of_iterations(self):
        result, text = capturing(self.chain().propagate, True)
        self.assertTrue(result)
        self.assertRegex(text, r"Number of iterations: \d+")
        # X and Z were not constrained, so propagate announces that it relates them
        self.assertIn("Constraint Added: X Z", text)

    def test_verbose_reports_an_inconsistency(self):
        net = qr.Network(self.alg, "Inconsistent")
        i, j, k = intervals("ijk")
        net.add_constraint(i, j, "B")
        net.add_constraint(j, k, "B")
        net.add_constraint(i, k, "BI")                  # i before j before k, yet i after k
        result, text = capturing(net.propagate, True)
        self.assertFalse(result)
        self.assertIn("the network is inconsistent", text)
        self.assertNotIn("Number of iterations", text)

    def test_propagating_again_changes_nothing(self):
        net = self.chain()
        self.assertTrue(quietly(net.propagate))
        before = constraints_by_name(net)
        self.assertTrue(quietly(net.propagate))
        self.assertEqual(constraints_by_name(net), before)

    def test_unconstrained_pairs_are_filled_in(self):
        net = self.chain()
        self.assertFalse(net.has_edge(net.get_entity("X"), net.get_entity("Z")))
        self.assertTrue(quietly(net.propagate))
        self.assertEqual(relations(net.get_constraint("X", "Z")), {"B", "D", "M", "O", "S"})
        self.assertEqual(relations(net.get_constraint("Z", "X")), {"BI", "DI", "MI", "OI", "SI"})

    def test_entity_classes_are_narrowed(self):
        """Entities that start out as either a point or a proper interval become whatever the
        constraints they are in allow."""
        both = ["Point", "ProperInterval"]
        # (constraint, classes of the first entity, classes of the second)
        for constraint, first, second in [("E", ["ProperInterval"], ["ProperInterval"]),
                                          ("PE", ["Point"], ["Point"]),
                                          ("PS", ["Point"], ["ProperInterval"])]:
            with self.subTest(constraint=constraint):
                a = qr.TemporalEntity(list(both), "a")
                b = qr.TemporalEntity(list(both), "b")
                net = qr.Network(self.extended, "Narrowing")
                net.add_constraint(a, b, constraint)
                self.assertTrue(quietly(net.propagate))
                self.assertEqual(sorted(a.classes), first)
                self.assertEqual(sorted(b.classes), second)


class TestAlgebraChecks(unittest.TestCase):
    """check_composition_identity and is_associative, on sound and on damaged algebras."""

    @classmethod
    def setUpClass(cls):
        cls.allen = load_algebra("Linear_Interval_Algebra")
        cls.extended = load_algebra("Extended_Linear_Interval_Algebra")

    def test_composition_identity_is_quiet_unless_verbose(self):
        result, text = capturing(self.allen.check_composition_identity)
        self.assertTrue(result)
        self.assertEqual(text, "")

    def test_composition_identity_verbose_report(self):
        result, text = capturing(self.allen.check_composition_identity, True)
        self.assertTrue(result)
        self.assertIn("Linear_Interval_Algebra -- Composition Identity Check:", text)
        self.assertIn("PASSED . 169 compositions tested.", text)    # 13 x 13
        self.assertNotIn("FAIL", text)

    def test_composition_identity_notices_a_damaged_table(self):
        damaged = tampered("Linear_Interval_Algebra", "B", "B", "M")    # B;B should be B
        self.assertFalse(quietly(damaged.check_composition_identity))
        result, text = capturing(damaged.check_composition_identity, True)
        self.assertFalse(result)
        self.assertIn("FAIL:", text)
        self.assertIn("( r ;  s)  = M", text)
        self.assertIn("FAILED. See FAILURE output above.", text)
        self.assertNotIn("PASSED", text)

    def test_composition_identity_notices_an_emptied_entry(self):
        damaged = tampered("Linear_Point_Algebra", "<", "<", "")
        self.assertFalse(quietly(damaged.check_composition_identity))

    def test_is_associative_prints_a_summary(self):
        result, text = capturing(self.allen.is_associative)
        self.assertTrue(result)
        self.assertEqual(text.strip(), "TEST SUMMARY: 2197 OK, 0 Skipped, 0 Failed (2197 Total)")

    def test_is_associative_skips_relations_whose_classes_do_not_meet(self):
        """In the extended algebra a relation between points cannot be composed with one between
        proper intervals, so many of the 18 x 18 x 18 triples are skipped."""
        _, text = capturing(self.extended.is_associative)
        match = re.search(r"TEST SUMMARY: (\d+) OK, (\d+) Skipped, (\d+) Failed \((\d+) Total\)", text)
        self.assertIsNotNone(match, text)
        ok, skipped, failed, total = (int(n) for n in match.groups())
        self.assertEqual(total, 18 ** 3)
        self.assertEqual(ok + skipped + failed, total)
        self.assertGreater(skipped, 0)
        self.assertGreater(ok, 0)
        self.assertNotIn("do not add up", text)

    def test_is_associative_verbose_output(self):
        _, text = capturing(self.extended.is_associative, True)
        self.assertIn("B x B x B :", text)
        self.assertIn("Associativity OK", text)
        self.assertIn("Skipping check due to a x b", text)
        self.assertIn("Skipping check due to b x c", text)

    def test_composition_is_associative_in_the_untyped_algebras(self):
        """Allen's algebra, RCC8 and the point algebras have a single ontological class, so
        every triple of relations can be composed.  This checks that with compose itself."""
        for name in ("Linear_Interval_Algebra", "RCC8_Algebra", "Linear_Point_Algebra",
                     "Right_Branching_Point_Algebra", "Left_Branching_Point_Algebra"):
            with self.subTest(algebra=name):
                self.assertEqual(associativity_violations(load_algebra(name)), [])

    def test_associativity_violations_finds_a_damaged_algebra(self):
        """Makes sure that the helper above can fail.  Damaging the entry for =;= in the linear
        point algebra leaves the composition identity intact but breaks associativity:
        (=;=);< is everything, but =;(=;<) is just <."""
        damaged = tampered("Linear_Point_Algebra", "=", "=", "<|>")
        self.assertTrue(quietly(damaged.check_composition_identity))
        self.assertTrue(associativity_violations(damaged))

    # KNOWN PROBLEM, in src/qualreas.py: is_associative multiplies the two relation sets with
    # '*' (prod_ab = a_rs * b_rs).  A RelSet is an int, so that is integer multiplication of the
    # bit masks, and not composition, and integer multiplication is always associative.  The
    # check can therefore never fail, which also means that TestAlgebras.test_associativity,
    # above, cannot fail.  The fix is to use self.compose(a_rs, b_rs) and so on.  Done with the
    # same skipping logic, that gives no failures for Allen's algebra, RCC8 and the point
    # algebras, but 924 for the extended algebra and 1798 for each branching algebra, so
    # test_associativity needs to be reconsidered at the same time.  When it is fixed, this test
    # will start to "pass unexpectedly": delete the decorator.
    @unittest.expectedFailure
    def test_is_associative_notices_a_damaged_algebra(self):
        damaged = tampered("Linear_Point_Algebra", "=", "=", "<|>")
        self.assertFalse(quietly(damaged.is_associative))


class TestPrintedReports(unittest.TestCase):
    """The methods and functions that print an algebra, a network, or a table."""

    @classmethod
    def setUpClass(cls):
        cls.algebras = {name: load_algebra(name) for name, _ in ALL_ALGEBRAS}
        cls.allen = cls.algebras["Linear_Interval_Algebra"]

    def test_entity_text(self):
        self.assertEqual(repr(qr.TemporalEntity(["Point"], "p")), "TemporalEntity(['Point'] 'p')")
        self.assertEqual(repr(qr.SpatialEntity(["Region"], "r")), "SpatialEntity(['Region'] 'r')")
        self.assertTrue(qr.TemporalEntity(["Point"]).name.startswith("TE:"))
        self.assertTrue(qr.SpatialEntity(["Region"]).name.startswith("SE:"))
        self.assertEqual(qr.make_name("given"), "given")

    def test_abbrev(self):
        self.assertEqual(qr.abbrev(["Point", "ProperInterval"]), "Pt|PInt")
        self.assertEqual(qr.abbrev(["Region"]), "Reg")
        self.assertEqual(qr.abbrev(["2DPoint"]), "2DPt")
        self.assertEqual(qr.abbrev([]), "")
        with self.assertRaises(KeyError):
            qr.abbrev(["Duration"])

    def test_algebra_summary(self):
        for name, alg in self.algebras.items():
            with self.subTest(algebra=name):
                _, text = capturing(alg.summary)
                self.assertIn(f"Algebra Name: {name}", text)
                self.assertIn(f"Description: {alg.description}", text)
                self.assertIn("Equality Rels:", text)
                self.assertIn("Domain & Range Abbreviations:", text)
                for rel in alg.elements:                 # a row for each relation
                    self.assertIn(alg.rel_name(rel), text)

    def test_element_summary(self):
        _, text = capturing(self.allen.element_summary, "B")
        shown = dict(line.split(":", 1) for line in text.splitlines())
        shown = {key.strip(): value.strip() for key, value in shown.items()}
        self.assertEqual(shown, {"Symbol": "B", "Name": "Before",
                                 "Domain": "['ProperInterval']", "Range": "['ProperInterval']",
                                 "Converse": "After", "Is Reflexive?": "False",
                                 "Is Symmetric?": "False", "Is Transitive?": "True",
                                 "Is an Equality Relation?": "False"})

    def test_compact_transitivity_table_is_valid_json_for_the_same_table(self):
        for name, alg in self.algebras.items():
            with self.subTest(algebra=name):
                _, text = capturing(alg.print_compact_transitivity_table)
                table = json.loads("{" + text + "}")["TransTable"]
                again = qr.Algebra(alg_dict={"Relations": alg.algebra_dict["Relations"],
                                             "TransTable": table})
                for r1, r2 in itertools.product(alg.elements, repeat=2):
                    self.assertEqual(again.transitivity_table[r1][r2], alg.transitivity_table[r1][r2])

    def test_network_summary(self):
        net = make_chain(self.allen, "Chain")
        _, text = capturing(net.summary)
        self.assertIn("Chain: 3 nodes, 9 edges", text)
        self.assertIn("Algebra: Linear_Interval_Algebra", text)
        for node in ("X", "Y", "Z"):
            self.assertIn(f"  {node}:['ProperInterval']", text)
        # A constraint is shown once, not once in each direction ...
        self.assertEqual([line.strip() for line in text.splitlines() if "=>" in line],
                         ["=> X: E", "=> Y: B", "=> Z: B|D|M|O|S", "=> Y: E", "=> Z: D", "=> Z: E"])
        # ... unless every edge is asked for
        _, text = capturing(net.summary, True)
        self.assertEqual(text.count("=>"), 9)
        self.assertIn("=> X: BI", text)

    def test_point_algebra_composition_table(self):
        for name, _ in POINT_ALGEBRAS:
            with self.subTest(algebra=name):
                alg = self.algebras[name]
                _, text = capturing(qr.print_point_algebra_composition_table, alg)
                lines = text.splitlines()
                self.assertEqual(lines[0], name)
                self.assertEqual(lines[1], "Elements: " + ", ".join(alg.elements))
                # The rows of the table are the lines with three words: rel1, rel2, composition
                printed = {}
                for line in lines:
                    words = line.split()
                    if len(words) == 3:
                        printed[(words[0], words[1])] = words[2]
                self.assertEqual(len(printed), len(alg.elements) ** 2)
                for (rel1, rel2), composition in printed.items():
                    self.assertEqual(composition, str(alg.transitivity_table[rel1][rel2]))

    def test_generate_consistent_networks_reports_how_many(self):
        pt = load_algebra("Linear_Point_Algebra")
        _, text = capturing(qr.generate_consistent_networks, pt)
        self.assertEqual(text.strip(), "13 consistent networks")

    def test_generate_consistent_networks_verbose(self):
        pt = load_algebra("Linear_Point_Algebra")
        _, text = capturing(qr.generate_consistent_networks, pt, verbose=True)
        self.assertEqual(text.count("=" * 26), 13)       # one block for each network
        self.assertNotIn("UNKNOWN", text)
        self.assertIn("<,<,<,<", text)                    # the signature of B
        self.assertIn("13 consistent networks", text)

    def test_running_the_module_as_a_script_runs_the_smoke_test(self):
        _, text = capturing(runpy.run_path, qr.__file__, run_name="__main__")
        self.assertEqual(text.splitlines(),
                         ["Smoke Test:",
                          f"qualreas {qr.__version__}: loaded Linear_Interval_Algebra with 13 relations"])


if __name__ == '__main__':
    unittest.main()
