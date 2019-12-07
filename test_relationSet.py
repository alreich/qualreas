import unittest
import qualreas as qr

__author__ = 'Alfred J. Reich'


class TestRelationSet(unittest.TestCase):

    def setUp(self):

        self.AAA = qr.Relation('AAA', 'A', 'a', 'testDomain', 'testRange', is_transitive=True)
        self.BBB = qr.Relation('BBB', 'B', 'b', 'testRange', 'testDomain', is_transitive=True)
        self.aaa = qr.Relation('aaa', 'a', 'A', 'testDomain', 'testRange')
        self.bbb = qr.Relation('bbb', 'b', 'B', 'testRange', 'testDomain')

        self.AAA.set_converse(self.aaa)  # AAA & aaa are each others' converses
        self.BBB.set_converse(self.bbb)  # BBB & bbb are each others' converses
        self.aaa.set_converse(self.AAA)
        self.bbb.set_converse(self.BBB)

        self.relset_ABa = qr.RelationSet([self.BBB, self.AAA, self.aaa])
        self.relset_Bab = qr.RelationSet([self.aaa, self.bbb, self.BBB])

    def test_addition(self):
        # 'Addition' is the same as set intersection
        self.assertEqual(self.relset_ABa + self.relset_Bab, qr.RelationSet([self.BBB, self.aaa]))

    def test_contains_1(self):
        self.assertEqual(self.AAA in self.relset_ABa, True)

    def test_contains_2(self):
        self.assertEqual(self.bbb in self.relset_ABa, False)

    def test_eq_1(self):
        self.assertEqual(self.relset_ABa == qr.RelationSet([self.aaa, self.BBB, self.AAA]), True)

    def test_eq_2(self):
        self.assertEqual(self.relset_ABa == qr.RelationSet([self.bbb, self.BBB, self.AAA]), False)

    def test_iter(self):
        names = set()
        for elem in self.relset_ABa:
            names.add(elem.short_name)
        self.assertEqual(names, {'A', 'B', 'a'})

    def test_len(self):
        self.assertEqual(len(self.relset_ABa), 3)

#    def test_mul(self):
#        '''N/A: The relations have to be part of an algebra to test multiplication'''

    def test_ne_1(self):
        self.assertEqual(self.relset_ABa != qr.RelationSet([self.aaa, self.BBB, self.AAA]), False)

    def test_ne_2(self):
        self.assertEqual(self.relset_ABa != qr.RelationSet([self.bbb, self.BBB, self.AAA]), True)

#    def test_repr(self):
#

    def test_union(self):
        self.assertEqual(self.relset_ABa.union(self.relset_Bab),
                         qr.RelationSet([self.AAA, self.BBB, self.aaa, self.bbb]))

    # def test_printSorted(self):
    #     self.fail()

    def test_elements(self):
        self.assertEqual(self.relset_ABa.elements, frozenset([self.AAA, self.BBB, self.aaa]))

    # def test_algebra(self):
    #     self.fail()

    def test_converse(self):
        self.assertEqual(self.relset_ABa.converse, qr.RelationSet([self.aaa, self.bbb, self.AAA]))

    def test_names(self):
        self.assertEqual(self.relset_ABa.short_names, ['A', 'B', 'a'])

    def test_fullnames(self):
        self.assertEqual(self.relset_ABa.long_names, ['AAA', 'BBB', 'aaa'])

if __name__ == '__main__':
    unittest.main()

# EOF
