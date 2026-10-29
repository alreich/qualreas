"""Unit tests for qualreas.

These are the checks that used to follow the ``if __name__ == '__main__'`` statement at the
end of src/qualreas.py, turned into unit tests:

  * every algebra loads, has the expected relations, and passes the composition-identity
    and associativity checks
  * constraint propagation gives the expected results in the interval, point and RCC8 algebras
  * the book example (interval algebra, and its extension to points) is detected as inconsistent
  * the Wikipedia RCC8 example is read from its JSON file and propagated

Run from anywhere, once qualreas is installed (pip install -e .):

    python -m unittest discover -s tests -v        # or just:  pytest tests
"""
import contextlib
import io
import os
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


if __name__ == '__main__':
    unittest.main()
