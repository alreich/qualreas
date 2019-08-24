import unittest
import qualreas as qr

__author__ = 'Alfred J. Reich'


class TestRelation(unittest.TestCase):

    def setUp(self):
        self.test_relation = qr.Relation('AAA', 'a', 'b', 'testDomain', 'testRange', is_transitive=True)
        self.test_relation_inverse = qr.Relation('BBB', 'b', 'a', 'testRange', 'testDomain', is_transitive=True)
        self.test_EQ_relation = qr.Relation("EEE", 'e', 'e', 'testDomain', 'testDomain', is_reflexive=True,
                                            is_symmetric=True, is_transitive=True)
        self.test_relation.set_inverse(self.test_relation_inverse)
        self.test_relation_inverse.set_inverse(self.test_relation)
        self.test_EQ_relation.set_inverse(self.test_EQ_relation)

    def test_inverse_name(self):
        self.assertEqual(self.test_relation.inverse_name, 'b')

    def test_inverse(self):
        self.assertEqual(self.test_relation.inverse, self.test_relation_inverse)
        self.assertEqual(self.test_relation_inverse.inverse, self.test_relation)

    def test_short_name(self):
        self.assertEqual(self.test_relation.short_name, 'a')

    def test_fullname(self):
        self.assertEqual(self.test_relation.full_name, 'AAA')

    def test_is_reflexive(self):
        self.assertEqual(self.test_relation.is_reflexive, False)

    def test_is_symmetric(self):
        self.assertEqual(self.test_relation.is_symmetric, False)

    def test_is_transitive(self):
        self.assertEqual(self.test_relation.is_transitive, True)

    def test_is_equality(self):
        self.assertEqual(self.test_relation.is_equality, False)
        self.assertEqual(self.test_EQ_relation.is_equality, True)

    def test_domain(self):
        self.assertEqual(self.test_relation.domain, 'testDomain')
        self.assertEqual(self.test_relation_inverse.domain, 'testRange')

    def test_range(self):
        self.assertEqual(self.test_relation.range, 'testRange')

    def test_less_than(self):
        self.assertEqual(self.test_relation < self.test_EQ_relation, True)

if __name__ == '__main__':
    unittest.main()

# EOF
