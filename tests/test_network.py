import unittest
import os
import qualreas as qr

__author__ = 'Alfred J. Reich'


class TestNetwork(unittest.TestCase):

    def setUp(self):
        """
        Load all of the existing algebras
        """
        path = os.path.join( os.getenv('PYPROJ'), 'qualreas' )

        self.alg0 = qr.Algebra(os.path.join(path, 'LinearIntervalAlgebra.json'))
        self.alg1 = qr.Algebra(os.path.join(path, 'ExtendedLinearIntervalAlgebra.json'))
        self.alg2 = qr.Algebra(os.path.join(path, 'LeftBranchingIntervalAlgebra.json'))
        self.alg3 = qr.Algebra(os.path.join(path, 'RightBranchingIntervalAlgebra.json'))
        self.alg4 = qr.Algebra(os.path.join(path, 'RCC8Algebra.json'))

        self.e1 = qr.TemporalObject(["ProperInterval"], "X")
        self.e2 = qr.TemporalObject(["ProperInterval"], "Y")
        self.e3 = qr.TemporalObject(["ProperInterval"], "Z")

        self.net0 = qr.Network(self.alg0)
        self.net1 = qr.Network(self.alg1)
        self.net2 = qr.Network(self.alg2)
        self.net3 = qr.Network(self.alg3)
        self.net4 = qr.Network(self.alg4)

    def test_constraint_0(self):
        r12_0 = self.alg0.relations["O"]
        r23_0 = self.alg0.relations["O"]
        self.net0.constraint(self.e1, self.e2, [r12_0])
        self.net0.constraint(self.e2, self.e3, [r23_0])
        self.net0.constraint(self.e1, self.e3)

    def test_propagate(self):
        self.net0.propagate()
        print(self.net0.print_constraints())

#    def test_printConstraints(self):
#        self.fail()

if __name__ == '__main__':
    unittest.main()

