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

Run from anywhere, once qualreas is installed (pip install -e .):

    python -m unittest discover -s tests -v        # or just:  pytest tests

Deriving the extended and the two branching-time interval algebras takes from 10 to 45 seconds
each, so those tests are skipped unless the environment variable QUALREAS_SLOW_TESTS is set:

    QUALREAS_SLOW_TESTS=1 python -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

import qualreas as qr

__author__ = 'Alfred J. Reich'


def quietly(func, *args, **kwargs):
    """Call func, discarding anything it prints (e.g., is_associative prints a test summary)."""
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)


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


if __name__ == '__main__':
    unittest.main()
