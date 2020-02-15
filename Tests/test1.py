'''
Created on Sep 6, 2010

@author: Alfred J. Reich
'''

from qualreas import *

if __name__ == '__main__':

    import os
    path = os.path.join( os.getenv('PYPROJ'), 'qualreas' )
    rcc8_alg = Algebra(os.path.join(path, "RCC8Algebra.json"))
    rcc8 = rcc8_alg.relations
    #rcc8.check_multiplication_identity()

    house1 = Region()
    house2 = Region()
    property1 = Region()
    property2 = Region()
    road = Region()

    dc = rcc8["DC"]
    ec = rcc8["EC"]
    tpp = rcc8["TPP"]
    ntpp = rcc8["NTPP"]

    # EXAMPLE: Region Connection Calculus 8
    problem = Network(rcc8, entities = [house1, house2, property1, property2, road])
    problem.constraint(house1, house2, [dc])
    problem.constraint(house1, property1, [tpp, ntpp])
    problem.constraint(house1,  property2, [dc, ec])
    problem.constraint(house1, road, [ec])
    problem.constraint(house2, property1, [dc, ec])
    problem.constraint(house2, property2, [ntpp])
    problem.constraint(house2, road, [ec])
    problem.constraint(property1, property2, [dc, ec])

