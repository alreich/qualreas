#from unittest import TestCase
import unittest
import qualreas as qr
import os

__author__ = 'Alfred J. Reich'


# class MyTestCase(unittest.TestCase):
#    def test_something(self):
#        self.assertEqual(True, False)

class TestRelation(unittest.TestCase):
    def setUp(self):
        self.test_relation = qr.Relation('AAA', 'a', 'b', 'testDomain', 'testRange', is_transitive=True)
        self.test_relation_converse = qr.Relation('BBB', 'b', 'a', 'testRange', 'testDomain', is_transitive=True)
        self.test_EQ_relation = qr.Relation("EEE", 'e', 'e', 'testDomain', 'testDomain', is_reflexive=True,
                                            is_symmetric=True, is_transitive=True)
        self.test_relation.set_converse(self.test_relation_converse)
        self.test_relation_converse.set_converse(self.test_relation)
        self.test_EQ_relation.set_converse(self.test_EQ_relation)

    def test_converse_name(self):
        self.assertEqual(self.test_relation.converse_name, 'b')

    def test_converse(self):
        self.assertEqual(self.test_relation.converse, self.test_relation_converse)
        self.assertEqual(self.test_relation_converse.converse, self.test_relation)

    def test_name(self):
        self.assertEqual(self.test_relation.short_name, 'a')

    def test_fullname(self):
        self.assertEqual(self.test_relation.long_name, 'AAA')

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
        self.assertEqual(self.test_relation_converse.domain, 'testRange')

    def test_range(self):
        self.assertEqual(self.test_relation.range, 'testRange')


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

    # def test_repr(self):
    #     self.assertEqual(self.relsetABC.__repr__(), '<RelationSet([a, b, c])>')

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


class TestAlgebra(unittest.TestCase):

    def setUp(self):
        """
        Load all of the existing algebras
        """
        path = os.path.join(os.getenv('PYPROJ'), 'qualreas/Algebras')
        self.alg0 = qr.Algebra(os.path.join(path, 'IntervalAlgebra.json'))
        self.alg1 = qr.Algebra(os.path.join(path, 'IntervalAndPointAlgebra.json'))
        self.alg2 = qr.Algebra(os.path.join(path, 'LeftBranchingIntervalAndPointAlgebra.json'))
        self.alg3 = qr.Algebra(os.path.join(path, 'RightBranchingIntervalAndPointAlgebra.json'))
        self.alg4 = qr.Algebra(os.path.join(path, 'rcc8Algebra.json'))

    # Interval Algebra
    def test_identity_relset0(self):
        allrelsnames0 = map(lambda x: x.short_name, self.alg0.identity)
        self.assertEqual(set(allrelsnames0),
                         {'B', 'E', 'D', 'OI', 'F', 'MI', 'DI', 'M', 'BI', 'O', 'S', 'FI', 'SI'})

    # Interval and Point Algebra
    def test_identity_relset1(self):
        allrelsnames1 = map(lambda x: x.short_name, self.alg1.identity)
        self.assertEqual(set(allrelsnames1),
                         {'B', 'E', 'D', 'OI', 'F', 'MI', 'DI', 'M', 'BI', 'O', 'S', 'FI', 'SI', 'PE', 'PF', 'PFI',
                          'PS', 'PSI'})

    # Left-Branching Interval and Point Algebra
    def test_identity_relset2(self):
        allrelsnames2 = map(lambda x: x.short_name, self.alg2.identity)
        self.assertEqual(set(allrelsnames2),
                         {'B', 'E', 'D', 'OI', 'F', 'MI', 'DI', 'M', 'BI', 'O', 'S', 'FI', 'SI', 'PE', 'PF', 'PFI',
                          'PS', 'PSI', 'LB', 'LBI', 'LF', 'LO', 'LOI', 'L~'})

    # Right-Branching Interval and Point Algebra
    def test_identity_relset3(self):
        allrelsnames3 = map(lambda x: x.short_name, self.alg3.identity)
        self.assertEqual(set(allrelsnames3),
                         {'B', 'E', 'D', 'OI', 'F', 'MI', 'DI', 'M', 'BI', 'O', 'S', 'FI', 'SI', 'PE', 'PF', 'PFI',
                          'PS', 'PSI', 'RB', 'RBI', 'RO', 'ROI', 'RS', 'R~'})

    # Region Connection Calculus 8
    def test_identity_relset4(self):
        allrelsnames4 = map(lambda x: x.short_name, self.alg4.identity)
        self.assertEqual(set(allrelsnames4),
                         {'DC', 'EC', 'EQ', 'NTPP', 'NTPPI', 'PO', 'TPP', 'TPPI'})

    # def test_mult(self):
    #     self.fail()

    # def test_add(self):
    #     self.fail()

    def test_name(self):
        self.assertEqual(self.alg0.name, 'LinearTimeIntervalAlgebra')

    def test_relations(self):
        self.assertEqual(self.alg0.relations['B'].short_name, 'B')

    def test_equality_relations0(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg0.equality_relations)), {'E'})

    def test_equality_relations1(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg1.equality_relations)), {'E', 'PE'})

    def test_equality_relations2(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg2.equality_relations)), {'E', 'PE'})

    def test_equality_relations3(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg3.equality_relations)), {'E', 'PE'})

    def test_equality_relations4(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg4.equality_relations)), {'EQ'})

    def test_relset0(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg0.relset(['B', 'D', 'O']))), {'B', 'D', 'O'})

    def test_relset1(self):
        self.assertEqual(set(map(lambda x: x.short_name,
                                 self.alg1.relset(['B', 'D', 'O', 'PF']))), {'B', 'D', 'O', 'PF'})

    def test_relset2(self):
        self.assertEqual(set(map(lambda x: x.short_name,
                                 self.alg2.relset(['B', 'D', 'O', 'LB']))), {'B', 'D', 'O', 'LB'})

    def test_relset3(self):
        self.assertEqual(set(map(lambda x: x.short_name,
                                 self.alg3.relset(['B', 'D', 'O', 'RB']))), {'B', 'D', 'O', 'RB'})

    def test_relset4(self):
        self.assertEqual(set(map(lambda x: x.short_name,
                                 self.alg4.relset(['DC', 'NTPP', 'TPPI']))), {'DC', 'NTPP', 'TPPI'})

    def test_trans_table0(self):
        self.assertEqual(len(self.alg0.transitivity_table), 13)

    def test_trans_table1(self):
        self.assertEqual(len(self.alg1.transitivity_table), 18)

    def test_trans_table2(self):
        self.assertEqual(len(self.alg2.transitivity_table), 24)

    def test_trans_table3(self):
        self.assertEqual(len(self.alg3.transitivity_table), 24)

    def test_trans_table4(self):
        self.assertEqual(len(self.alg4.transitivity_table), 8)

    def test_check_mult_identity0(self):
        self.assertEqual(self.alg0.check_multiplication_identity(), True)

    def test_check_mult_identity1(self):
        self.assertEqual(self.alg1.check_multiplication_identity(), True)

    def test_check_mult_identity2(self):
        self.assertEqual(self.alg2.check_multiplication_identity(), True)

    def test_check_mult_identity3(self):
        self.assertEqual(self.alg3.check_multiplication_identity(), True)

    def test_check_mult_identity4(self):
        self.assertEqual(self.alg4.check_multiplication_identity(), True)

    def test_is_associative0(self):
        self.assertEqual(self.alg0.is_associative(), True)

    # def test_is_associative1(self):
    #     self.assertEqual(self.alg1.is_associative(verbose=True), True)

    # def test_is_associative2(self):
    #     self.assertEqual(self.alg2.is_associative(), False)
    #
    # def test_is_associative3(self):
    #     self.assertEqual(self.alg3.is_associative(), False)
    #
    # def test_is_associative4(self):
    #     self.assertEqual(self.alg4.is_associative(), True)


class TestNetwork(unittest.TestCase):

    # def __init__(self, methodName='runTest'):
    #     super().__init__(methodName='runTest')
    #     self.D = None

    def setUp(self):
        """
        Load all of the existing algebras
        """
        path = os.path.join(os.getenv('PYPROJ'), 'qualreas/Algebras')

        self.alg0 = qr.Algebra(os.path.join(path, 'IntervalAlgebra.json'))
        self.alg1 = qr.Algebra(os.path.join(path, 'IntervalAndPointAlgebra.json'))
        self.alg2 = qr.Algebra(os.path.join(path, 'LeftBranchingIntervalAndPointAlgebra.json'))
        self.alg3 = qr.Algebra(os.path.join(path, 'RightBranchingIntervalAndPointAlgebra.json'))
        self.alg4 = qr.Algebra(os.path.join(path, 'rcc8Algebra.json'))

        self.e1 = qr.TemporalObject(["ProperInterval"], "X")
        self.e2 = qr.TemporalObject(["ProperInterval"], "Y")
        self.e3 = qr.TemporalObject(["ProperInterval"], "Z")

        self.int_A = qr.TemporalObject(["ProperInterval"], "Int A")
        self.int_B = qr.TemporalObject(["ProperInterval"], "Int B")
        self.int_C = qr.TemporalObject(["ProperInterval"], "Int C")
        self.int_D = qr.TemporalObject(["ProperInterval"], "Int D")

        self.net0 = qr.Network(self.alg0)
        self.net1 = qr.Network(self.alg0)

    def test_constraint_0(self):
        r12_0 = self.alg0.relations["O"]
        r23_0 = self.alg0.relations["O"]
        self.net0.constraint(self.e1, self.e2, [r12_0])
        self.net0.constraint(self.e2, self.e3, [r23_0])
        self.net0.constraint(self.e1, self.e3)
        print(self.net0.print_constraints())
        self.net0.propagate()
        print(self.net0.print_constraints())

    def test_constraint_1(self):
        # This is the "inconsistent labeling" network from Figure 5 of Allen's original 1983 paper
        rel_D  = self.alg0.relations["D"]
        rel_DI = self.alg0.relations["DI"]
        rel_F  = self.alg0.relations["F"]
        rel_FI = self.alg0.relations["FI"]
        rel_M  = self.alg0.relations["M"]
        rel_O  = self.alg0.relations["O"]
        rel_S  = self.alg0.relations["S"]
        self.net1.constraint(self.int_A, self.int_B, [rel_D, rel_DI])
        self.net1.constraint(self.int_D, self.int_A, [rel_M, rel_S])
        self.net1.constraint(self.int_D, self.int_B, [rel_O])
        self.net1.constraint(self.int_D, self.int_C, [rel_M, rel_S])
        self.net1.constraint(self.int_B, self.int_C, [rel_D, rel_DI])

        self.net1.constraint(self.int_A, self.int_C, [rel_F, rel_FI])
        # self.net1.constraint(self.int_A, self.int_C, [rel_F])
        # self.net1.constraint(self.int_A, self.int_C, [rel_FI])

        print(self.net1.print_constraints())
        self.net1.propagate()
        print(self.net1.print_constraints())

    # def test_propagate(self):
    #     self.net0.propagate()
    #     print(self.net0.print_constraints())


if __name__ == '__main__':
    unittest.main()
