"""
DOC TESTS:
To run the tests type the following command in a terminal window: "python -m doctest -v qualreas_doctests.py"

>>> import os

The environment variable, PYPROJ, should be set to the directory where the 'qualreas' project
resides:

>>> path = os.path.join( os.getenv('PYPROJ'), 'qualreas' )

-----------------
Interval Algebra:
-----------------

Algebras are created by reading their definition from a JSON file:

>>> alg0 = Algebra(os.path.join(path, "IntervalAlgebra.json"))

Use the 'relations' property to obtain the full set of relations in the algebra:

>>> rels0 = alg0.relations

Only relation sets can be 'multiplied', so create a couple of one-element sets, {Before} & {Met-By}:

>>> b0 = RelationSet([rels0["B"]], alg0)

>>> mi0 = RelationSet([rels0["MI"]], alg0)

Now 'multiply' them together:

Before * Met-By:
>>> sorted(b0 * mi0, key=lambda rel: rel.short_name)
[B, D, M, O, S]

The following computations illustrate an identity involving relation set multiplication, that is,
if X & Y are two relation sets and 'inv()' inverts a relation set, then:  X * Y = inv(inv(Y) * inv(X))

inv( inv(Met-By) * inv(Before) ):
>>> sorted( (mi0.inverse * b0.inverse).inverse , key=lambda rel: rel.short_name)
[B, D, M, O, S]

Met-By * Before:
>>> sorted(mi0 * b0, key=lambda rel: rel.short_name)
[B, DI, FI, M, O]

inv( inv(Before) * inv(Met-By) ):
>>> sorted( (b0.inverse * mi0.inverse).inverse , key=lambda rel: rel.short_name)
[B, DI, FI, M, O]

Relation sets can also be 'added' together. 'Addition' here is actually set intersection:

(Before * Met-By) + (Met-By * Before):
>>> sorted( (b0 * mi0) + (mi0 * b0), key=lambda rel: rel.short_name)
[B, M, O]

>>> alg0.equality_relations
[E]

The examples shown, above, are repeated for three more relation algebras in the next three sections.  In each example,
note how different relation sets (from those obtained, above) result from multiplications of what looks like the same
relation sets (i.e., point, left-branching, and right-branching relations get pulled in to play):

-------------------------
Interval & Point Algebra:
-------------------------

>>> alg1 = Algebra(os.path.join(path, "IntervalAndPointAlgebra.json"))

>>> rels1 = alg1.relations

>>> b1 = RelationSet([rels1["B"]], alg1)

>>> mi1 = RelationSet([rels1["MI"]], alg1)

Before * Met-By:
>>> sorted(b1 * mi1, key=lambda rel: rel.short_name)
[B, D, M, O, PS, S]

inv( inv(Met-By) * inv(Before) ):
>>> sorted( (mi1.inverse * b1.inverse).inverse , key=lambda rel: rel.short_name)
[B, D, M, O, PS, S]

Met-By * Before:
>>> sorted(mi1 * b1, key=lambda rel: rel.short_name)
[B, DI, FI, M, O, PFI]

inv( inv(Before) * inv(Met-By) ):
>>> sorted( (b1.inverse * mi1.inverse).inverse , key=lambda rel: rel.short_name)
[B, DI, FI, M, O, PFI]

(Before * Met-By) + (Met-By * Before):
>>> sorted( (b1 * mi1) + (mi1 * b1), key=lambda rel: rel.short_name)
[B, M, O]

>>> sorted(alg1.equality_relations, key=lambda rel: rel.short_name)
[E, PE]

----------------------------------------
Left-Branching Interval & Point Algebra:
----------------------------------------

>>> alg2 = Algebra(os.path.join(path, "LeftBranchingIntervalAndPointAlgebra.json"))

>>> rels2 = alg2.relations

>>> b2 = RelationSet([rels2["B"]], alg2)

>>> mi2 = RelationSet([rels2["MI"]], alg2)

Before * Met-By:
>>> sorted(b2 * mi2, key=lambda rel: rel.short_name)
[B, D, LB, LO, M, O, PS, S]

inv( inv(Met-By) * inv(Before) ):
>>> sorted( (mi2.inverse * b2.inverse).inverse , key=lambda rel: rel.short_name)
[B, D, LB, LO, M, O, PS, S]

Met-By * Before:
>>> sorted(mi2 * b2, key=lambda rel: rel.short_name)
[B, DI, FI, M, O, PFI]

inv( inv(Before) * inv(Met-By) ):
>>> sorted( (b2.inverse * mi2.inverse).inverse , key=lambda rel: rel.short_name)
[B, DI, FI, M, O, PFI]

(Before * Met-By) + (Met-By * Before):
>>> sorted( (b2 * mi2) + (mi2 * b2), key=lambda rel: rel.short_name)
[B, M, O]

>>> sorted(alg2.equality_relations, key=lambda rel: rel.short_name)
[E, PE]

-----------------------------------------
Right-Branching Interval & Point Algebra:
-----------------------------------------

>>> alg3 = Algebra(os.path.join(path, "RightBranchingIntervalAndPointAlgebra.json"))

>>> rels3 = alg3.relations

>>> b3 = RelationSet([rels3["B"]], alg3)

>>> mi3 = RelationSet([rels3["MI"]], alg3)

Before * Met-By:
>>> sorted(b3 * mi3, key=lambda rel: rel.short_name)
[B, D, M, O, PS, S]

inv( inv(Met-By) * inv(Before) ):
>>> sorted( (mi3.inverse * b3.inverse).inverse , key=lambda rel: rel.short_name)
[B, D, M, O, PS, S]

Met-By * Before:
>>> sorted(mi3 * b3, key=lambda rel: rel.short_name)
[B, DI, FI, M, O, PFI, RB, RO]

inv( inv(Before) * inv(Met-By) ):
>>> sorted( (b3.inverse * mi3.inverse).inverse , key=lambda rel: rel.short_name)
[B, DI, FI, M, O, PFI, RB, RO]

(Before * Met-By) + (Met-By * Before):
>>> sorted( (b3 * mi3) + (mi3 * b3), key=lambda rel: rel.short_name)
[B, M, O]

>>> sorted(alg3.equality_relations, key=lambda rel: rel.short_name)
[E, PE]

-----------------------------
Region Connection Calculus 8:
-----------------------------

>>> alg4 = Algebra(os.path.join(path, "rcc8Algebra.json"))

>>> rels4 = alg4.relations

>>> DC = rels4['DC']

>>> EC = rels4['EC']

>>> PO = rels4['PO']

>>> TPP = rels4['TPP']

>>> NTPP = rels4['NTPP']

>>> TPPI = rels4['TPPI']

>>> NTPPI = rels4['NTPPI']

>>> EQ = rels4['EQ']

>>> house1 = SpatialObject(['Region'], 'house1')

>>> house2 = SpatialObject(['Region'], 'house2')

>>> property1 = SpatialObject(['Region'], 'property1')

>>> property2 = SpatialObject(['Region'], 'property2')

>>> road = SpatialObject(['Region'], 'road')

>>> net4 = Network(alg4, "Wikipedia RCC8 Example")

house1 {DC} house2:
>>> net4.constraint(house1,house2,[DC])

house1 {TPP,NTPP} property1:
>>> net4.constraint(house1,property1,[TPP,NTPP])

house1 {DC,EC} property2:
>>> net4.constraint(house1,property2,[DC,EC])

house1 {EC} road:
>>> net4.constraint(house1,road,[EC])

house2 {DC,EC} property1:
>>> net4.constraint(house2,property1,[DC,EC])

house2 {NTPP} property2:
>>> net4.constraint(house2,property2,[NTPP])

house2 {EC} road:
>>> net4.constraint(house2,road,[EC])

property1 {DC,EC} property2:
>>> net4.constraint(property1,property2,[DC,EC])

road { DC, EC, TPP, TPPi, PO, EQ, NTPP, NTPPi } property1
>>> net4.constraint(road,property1,[DC,EC,TPP,TPPI,PO,EQ,NTPP,NTPPI])

road { DC, EC, TPP, TPPi, PO, EQ, NTPP, NTPPi } property2
>>> net4.constraint(road,property2,[DC,EC,TPP,TPPI,PO,EQ,NTPP,NTPPI])

>>> net4.print_constraints()
<BLANKLINE>
<Network: Wikipedia RCC8 Example, 5 entities>
Constraints: (Source, Target, RelationSet)
  house1, house1, [EQ]
  house1, house2, [DC]
  house1, property1, [NTPP, TPP]
  house1, property2, [DC, EC]
  house1, road, [EC]
  house2, house1, [DC]
  house2, house2, [EQ]
  house2, property1, [DC, EC]
  house2, property2, [NTPP]
  house2, road, [EC]
  property1, house1, [NTPPI, TPPI]
  property1, house2, [DC, EC]
  property1, property1, [EQ]
  property1, property2, [DC, EC]
  property1, road, [NTPPI, NTPP, DC, EC, TPPI, TPP, EQ, PO]
  property2, house1, [DC, EC]
  property2, house2, [NTPPI]
  property2, property1, [DC, EC]
  property2, property2, [EQ]
  property2, road, [NTPPI, NTPP, DC, EC, TPPI, TPP, EQ, PO]
  road, house1, [EC]
  road, house2, [EC]
  road, property1, [NTPPI, NTPP, DC, EC, TPPI, TPP, EQ, PO]
  road, property2, [NTPPI, NTPP, DC, EC, TPPI, TPP, EQ, PO]
  road, road, [EQ]

>>> net4.propagate()

>>> net4.print_constraints()
<BLANKLINE>
<Network: Wikipedia RCC8 Example, 5 entities>
Constraints: (Source, Target, RelationSet)
  house1, house1, [EQ]
  house1, house2, [DC]
  house1, property1, [NTPP, TPP]
  house1, property2, [DC, EC]
  house1, road, [EC]
  house2, house1, [DC]
  house2, house2, [EQ]
  house2, property1, [DC]
  house2, property2, [NTPP]
  house2, road, [EC]
  property1, house1, [NTPPI, TPPI]
  property1, house2, [DC]
  property1, property1, [EQ]
  property1, property2, [DC, EC]
  property1, road, [EC, PO]
  property2, house1, [DC, EC]
  property2, house2, [NTPPI]
  property2, property1, [DC, EC]
  property2, property2, [EQ]
  property2, road, [TPPI, PO]
  road, house1, [EC]
  road, house2, [EC]
  road, property1, [EC, PO]
  road, property2, [TPP, PO]
  road, road, [EQ]

"""

from qualreas import *
