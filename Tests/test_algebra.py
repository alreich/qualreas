import unittest
import os
import qualreas as qr

__author__ = 'Alfred J. Reich'

class TestAlgebra(unittest.TestCase):

    def setUp(self):
        """
        Load all of the existing algebras
        """
        path = os.path.join( os.getenv('PYPROJ'), 'qualreas/Algebras' )
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
        self.assertEqual(set(map(lambda x: x.short_name, self.alg1.relset(['B', 'D', 'O', 'PF']))), {'B', 'D', 'O', 'PF'})

    def test_relset2(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg2.relset(['B', 'D', 'O', 'LB']))), {'B', 'D', 'O', 'LB'})

    def test_relset3(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg3.relset(['B', 'D', 'O', 'RB']))), {'B', 'D', 'O', 'RB'})

    def test_relset4(self):
        self.assertEqual(set(map(lambda x: x.short_name, self.alg4.relset(['DC', 'NTPP', 'TPPI']))), {'DC', 'NTPP', 'TPPI'})

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

if __name__ == '__main__':
    unittest.main()

# EOF
