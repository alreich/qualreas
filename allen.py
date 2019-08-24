'''
Created on Sep 5, 2010

@author: Alfred J. Reich, Ph.D.
'''

from qualreas.QR import Relation, RelationSet, Algebra

# Allen's TranSitivity Table for Proper Intervals

B = Relation("Before", "B", isTransitive = True)
Bi = Relation("After", "Bi", isTransitive = True)
D = Relation("During", "D", isTransitive = True)
Di = Relation("Contains", "Di", isTransitive = True)
E = Relation("Equals", "E", isReflexive = True, isSymmetric = True, isTransitive = True)
F = Relation("Finishes", "F", isTransitive = True)
Fi = Relation("FinishedBy", "Fi", isTransitive = True)
M = Relation("Meets", "M")
Mi = Relation("MetBy", "Mi")
O = Relation("Overlaps", "O")
Oi = Relation("OverlappedBy", "Oi")
S = Relation("Starts", "S", isTransitive = True)
Si = Relation("StartedBy", "Si", isTransitive = True)

B.setInv(Bi); Bi.setInv(B)
D.setInv(Di); Di.setInv(D)
E.setInv(E)
F.setInv(Fi); Fi.setInv(F)
M.setInv(Mi); Mi.setInv(M)
O.setInv(Oi); Oi.setInv(O)
S.setInv(Si); Si.setInv(S)

allRelations = RelationSet([B, Bi, D, Di, E, F, Fi, M, Mi, O, Oi, S, Si])

__rs1 = RelationSet([B])
__rs2 = RelationSet([B, Bi, D, Di, E, F, Fi, M, Mi, O, Oi, S, Si])
__rs3 = RelationSet([B, D, M, O, S])
__rs4 = RelationSet([B, Di, Fi, M, O])
__rs5 = RelationSet([B, M, O])
__rs6 = RelationSet([Bi])
__rs7 = RelationSet([Bi, D, F, Mi, Oi])
__rs8 = RelationSet([Bi, Di, Mi, Oi, Si])
__rs9 = RelationSet([Bi, Mi, Oi])
__rs10 = RelationSet([D])
__rs11 = RelationSet([D, Di, E, F, Fi, O, Oi, S, Si])
__rs12 = RelationSet([D, F, Oi])
__rs13 = RelationSet([D, O, S])
__rs14 = RelationSet([Di])
__rs15 = RelationSet([Di, Fi, O])
__rs16 = RelationSet([Di, Oi, Si])
__rs17 = RelationSet([E])
__rs18 = RelationSet([E, F, Fi])
__rs19 = RelationSet([F])
__rs20 = RelationSet([Fi])
__rs21 = RelationSet([M])
__rs22 = RelationSet([Mi])
__rs23 = RelationSet([O])
__rs24 = RelationSet([Oi])
__rs25 = RelationSet([S])
__rs26 = RelationSet([Si])
__rs27 = RelationSet([E, S, Si])

table = {(B, B): __rs1,
         (B, Bi): __rs2,
         (B, D): __rs3,
         (B, Di): __rs1,
         (B, E): __rs1,
         (B, F): __rs3,
         (B, Fi): __rs1,
         (B, M): __rs1,
         (B, Mi): __rs3,
         (B, O): __rs1,
         (B, Oi): __rs3,
         (B, S): __rs1,
         (B, Si): __rs1,
         (Bi, B): __rs2,
         (Bi, Bi): __rs6,
         (Bi, D): __rs7,
         (Bi, Di): __rs6,
         (Bi, E): __rs6,
         (Bi, F): __rs6,
         (Bi, Fi): __rs6,
         (Bi, M): __rs7,
         (Bi, Mi): __rs6,
         (Bi, O): __rs7,
         (Bi, Oi): __rs6,
         (Bi, S): __rs7,
         (Bi, Si): __rs6,
         (D, B): __rs1,
         (D, Bi): __rs6,
         (D, D): __rs10,
         (D, Di): __rs2,
         (D, E): __rs10,
         (D, F): __rs10,
         (D, Fi): __rs3,
         (D, M): __rs1,
         (D, Mi): __rs6,
         (D, O): __rs3,
         (D, Oi): __rs7,
         (D, S): __rs10,
         (D, Si): __rs7,
         (Di, B): __rs4,
         (Di, Bi): __rs8,
         (Di, D): __rs11,
         (Di, Di): __rs14,
         (Di, E): __rs14,
         (Di, F): __rs16,
         (Di, Fi): __rs14,
         (Di, M): __rs15,
         (Di, Mi): __rs16,
         (Di, O): __rs15,
         (Di, Oi): __rs16,
         (Di, S): __rs15,
         (Di, Si): __rs14,
         (E, B): __rs1,
         (E, Bi): __rs6,
         (E, D): __rs10,
         (E, Di): __rs14,
         (E, E): __rs17,
         (E, F): __rs19,
         (E, Fi): __rs20,
         (E, M): __rs21,
         (E, Mi): __rs22,
         (E, O): __rs23,
         (E, Oi): __rs24,
         (E, S): __rs25,
         (E, Si): __rs26,
         (F, B): __rs1,
         (F, Bi): __rs6,
         (F, D): __rs10,
         (F, Di): __rs8,
         (F, E): __rs19,
         (F, F): __rs19,
         (F, Fi): __rs18,
         (F, M): __rs21,
         (F, Mi): __rs6,
         (F, O): __rs13,
         (F, Oi): __rs9,
         (F, S): __rs10,
         (F, Si): __rs9,
         (Fi, B): __rs1,
         (Fi, Bi): __rs8,
         (Fi, D): __rs13,
         (Fi, Di): __rs14,
         (Fi, E): __rs20,
         (Fi, F): __rs18,
         (Fi, Fi): __rs20,
         (Fi, M): __rs21,
         (Fi, Mi): __rs16,
         (Fi, O): __rs23,
         (Fi, Oi): __rs16,
         (Fi, S): __rs23,
         (Fi, Si): __rs14,
         (M, B): __rs1,
         (M, Bi): __rs8,
         (M, D): __rs13,
         (M, Di): __rs1,
         (M, E): __rs21,
         (M, F): __rs13,
         (M, Fi): __rs1,
         (M, M): __rs1,
         (M, Mi): __rs18,
         (M, O): __rs1,
         (M, Oi): __rs13,
         (M, S): __rs21,
         (M, Si): __rs21,
         (Mi, B): __rs4,
         (Mi, Bi): __rs6,
         (Mi, D): __rs12,
         (Mi, Di): __rs6,
         (Mi, E): __rs22,
         (Mi, F): __rs22,
         (Mi, Fi): __rs22,
         (Mi, M): __rs27,
         (Mi, Mi): __rs6,
         (Mi, O): __rs12,
         (Mi, Oi): __rs6,
         (Mi, S): __rs12,
         (Mi, Si): __rs6,
         (O, B): __rs1,
         (O, Bi): __rs8,
         (O, D): __rs13,
         (O, Di): __rs4,
         (O, E): __rs23,
         (O, F): __rs13,
         (O, Fi): __rs5,
         (O, M): __rs1,
         (O, Mi): __rs16,
         (O, O): __rs5,
         (O, Oi): __rs11,
         (O, S): __rs23,
         (O, Si): __rs15,
         (Oi, B): __rs4,
         (Oi, Bi): __rs6,
         (Oi, D): __rs12,
         (Oi, Di): __rs8,
         (Oi, E): __rs24,
         (Oi, F): __rs24,
         (Oi, Fi): __rs16,
         (Oi, M): __rs15,
         (Oi, Mi): __rs6,
         (Oi, O): __rs11,
         (Oi, Oi): __rs9,
         (Oi, S): __rs12,
         (Oi, Si): __rs9,
         (S, B): __rs1,
         (S, Bi): __rs6,
         (S, D): __rs10,
         (S, Di): __rs4,
         (S, E): __rs25,
         (S, F): __rs10,
         (S, Fi): __rs5,
         (S, M): __rs1,
         (S, Mi): __rs22,
         (S, O): __rs5,
         (S, Oi): __rs12,
         (S, S): __rs25,
         (S, Si): __rs27,
         (Si, B): __rs4,
         (Si, Bi): __rs6,
         (Si, D): __rs12,
         (Si, Di): __rs14,
         (Si, E): __rs26,
         (Si, F): __rs24,
         (Si, Fi): __rs14,
         (Si, M): __rs15,
         (Si, Mi): __rs22,
         (Si, O): __rs15,
         (Si, Oi): __rs24,
         (Si, S): __rs27,
         (Si, Si): __rs26
         }

algebraAllen = Algebra("Allen's Algebra of Proper Intervals", allRelations, table)

#class AlgebraAllen(Algebra):
#    def __init__(self):
#        Algebra.__init__("Allen's Algebra of Proper Intervals", allRelations, table)
