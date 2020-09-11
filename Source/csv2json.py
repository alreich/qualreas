"""
Created on Nov 3, 2012

@author: Alfred J. Reich
"""

import csv, json

class SetEncoder(json.JSONEncoder):
    """
    Custom encoder that turns Python sets into lists. Needed for dumping
    Python sets to JSON, since JSON doesn't contain sets as a datatype.
    """
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        else:
            return json.JSONEncoder.default(self, obj)

#def transTable2JsonString(transitivity_table):
#    return json.dumps(transitivity_table, cls=SetEncoder, indent=4)

def dictDump(d, jsonFile):
    with open(jsonFile, 'wb') as jsonOut:
        json.dump(d, jsonOut, cls=SetEncoder, sort_keys=True, indent=4)

def csvTransTable2Dict(filename):
    """
    Read transitivity table in .csv format and convert it to a dictionary.  Returns the dictionary.
    """
    f = open(filename, "rb")
    reader = csv.reader(f)
    reader.next() # Skip header line
    transTbl = {}
    for rel1, rel2, prod in reader:
        if prod == "-":
            transTbl[rel1][rel2] = []
        else:
            relList = prod.split(' ')
            for rel in relList:
                addToTable(transTbl,rel1,rel2,rel)
    f.close()
    return transTbl

def trueOrFalse(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        print '*** TYPO IN CSV FILE ***'

def csvRelations2Dict(filename):
    """
    Read relations in .csv format and convert it to a dictionary.  Returns the dictionary.
    """
    f = open(filename, "rb")
    reader = csv.reader(f)
    reader.next() # Skip header line
    relations = {}
    for name, rel, conv, dom, rng, ref, sym, trn in reader:
        relations[rel] = {"Name":name,
                          "Converse":conv,
                          "Domain":dom,
                          "Range":rng,
                          "Reflexive":trueOrFalse(ref),
                          "Symmetric":trueOrFalse(sym),
                          "Transitive":trueOrFalse(trn)
                          }
    f.close()
    return relations

def csvAlgebra2Json(algName, algType, algDesc, relations, transitivityTable, jsonFileName):
    alg = {"Name":algName,
           "Type":algType,
           "Description":algDesc,
           "Relations":relations,
           "TransTable":transitivityTable}
    dictDump(alg,jsonFileName)
    print "Created JSON file: %s (%s) - %s." % (algName,algType,algDesc)

def addToTable(transTable, relation1, relation2, product):
    """
    Create a dictionary of dictionaries that stores a transitivity table.
    """
    if relation1 not in transTable:
        transTable[relation1] = {relation2: {product}}
    else:
        if relation2 not in transTable[relation1]:
            transTable[relation1][relation2] = {product}
        else:
            transTable[relation1][relation2].add(product)

if __name__ == '__main__':

    import os

    path = os.path.join( os.getenv('PYPROJ'), 'qualreas' )

    leftBranchingPointRels = csvRelations2Dict(os.path.join(path, 'leftBranchingPointRelations.csv'))
    leftBranchingPointTransTbl = csvTransTable2Dict(os.path.join(path, 'leftBranchingPointTransTable.csv'))
    csvAlgebra2Json("Left-Branching Point Algebra", "Relation System",
        "Left-Branching Point Algebra",
        leftBranchingPointRels, leftBranchingPointTransTbl,
        os.path.join(path, "LeftBranchingPointAlgebra.json"))

    rightBranchingPointRels = csvRelations2Dict(os.path.join(path, 'rightBranchingPointRelations.csv'))
    rightBranchingPointTransTbl = csvTransTable2Dict(os.path.join(path, 'rightBranchingPointTransTable.csv'))
    csvAlgebra2Json("Right-Branching Point Algebra", "Relation System",
        "Right-Branching Point Algebra",
        rightBranchingPointRels, rightBranchingPointTransTbl,
        os.path.join(path, "RightBranchingPointAlgebra.json"))

    linearPointRels = csvRelations2Dict(os.path.join(path, 'linearPointRelations.csv'))
    linearPointTransTbl = csvTransTable2Dict(os.path.join(path, 'linearPointTransTable.csv'))
    csvAlgebra2Json("Linear Point Algebra", "Relation System",
        "Linear Point Algebra",
        linearPointRels, linearPointTransTbl,
        os.path.join(path, "LinearPointAlgebra.json"))

    # rcc8Rels = csvRelations2Dict(os.path.join(path, 'rcc8Relations.csv'))
    # rcc8TransTbl = csvTransTable2Dict(os.path.join(path, 'rcc8TransTable.csv'))
    # csvAlgebra2Json("RCC8", "Relation System",
    #     "Region Connection Calculus 8 Algebra",
    #     rcc8Rels, rcc8TransTbl,
    #     os.path.join(path, "RCC8Algebra.json"))

#    intRels = csvRelations2Dict(os.path.join(path, 'intervalRelations.csv'))
#    intTransTbl = csvTransTable2Dict(os.path.join(path, 'intervalTransTable.csv'))
#    csvAlgebra2Json("Linear Time Interval Algebra", "Relation System",
#        "Allen's algebra of proper time intervals",
#        intRels, intTransTbl,
#        os.path.join(path, "LinearIntervalAlgebra.json"))
#
#    ptRels = csvRelations2Dict(os.path.join(path, 'PointRelations.csv'))
#    intPtRels = intRels.copy() # Make a copy of the interval-only relations
#    intPtRels.update(ptRels)   #    then add the point relations to it.
#    intPtTransTbl = csvTransTable2Dict(os.path.join(path, 'IntervalPointTransTable.csv'))
#    csvAlgebra2Json("Linear Time Interval & Point Algebra", "Relation System",
#        "Reich's point extension to Allen's time interval algebra (see TIME-94 paper)",
#        intPtRels, intPtTransTbl,
#        os.path.join(path, "ExtendedLinearIntervalAlgebra.json"))
#
#    rbRels = csvRelations2Dict(os.path.join(path, 'RightBranchingRelations.csv'))
#    intPtRbRels = intPtRels.copy() # Make a copy of the interval & point relations
#    intPtRbRels.update(rbRels)     #    then add the right-branching relations to it.
#    rbTransTbl = csvTransTable2Dict(os.path.join(path, 'RightBranchingTransTable.csv'))
#    csvAlgebra2Json("Right-Branching Time Interval & Point Algebra", "Relation System",
#        "Reich's right-branching extension to Allen's time interval algebra (see TIME-94 paper)",
#        intPtRbRels, rbTransTbl,
#        os.path.join(path, "RightBranchingIntervalAlgebra.json"))
#
#    lbRels = csvRelations2Dict(os.path.join(path, 'LeftBranchingRelations.csv'))
#    intPtLbRels = intPtRels.copy() # Make a copy of the interval & point relations
#    intPtLbRels.update(lbRels)     #    then add the left-branching relations to it.
#    lbTransTbl = csvTransTable2Dict(os.path.join(path, 'LeftBranchingTransTable.csv'))
#    csvAlgebra2Json("Left-Branching Time Interval & Point Algebra", "Relation System",
#        "Reich's left-branching extension to Allen's time interval algebra (see TIME-94 paper)",
#        intPtLbRels, lbTransTbl,
#        os.path.join(path, "LeftBranchingIntervalAlgebra.json"))

# EOF
