"""
@author: Alfred J. Reich, Ph.D.

"""

import json
from bitsets import bitset
import networkx as nx
import uuid
from itertools import combinations, chain

__author__ = 'Alfred J. Reich'
__version__ = '0.2.0'


# Some utilities:

def flatten(list_of_lists):
    """Flatten one level of nesting"""
    return chain.from_iterable(list_of_lists)


# TODO: Make the function list_of_combinations produce an iterator, rather than a list
def list_of_combinations(items, make_sequence):
    """Given a list of items, return a list of all possible combinations of the items.
    Each combination is expressed in the form of whatever sequence building function
    is passed in for make_sequence (e.g., list, set, tuple).  The empty combination is not
    included in the returned result.  If there are n items in the input list, then
    the number of combinations in the result will be 2^n - 1, so becareful not too include
    too many items in the input list of items.

    Example:
    > n = 4
    > items = list(range(4))
    > list_of_combinations(items, set)
     [{0}, {1}, {2}, {3}, {0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}, {0, 1, 2},
      {0, 1, 3}, {0, 2, 3}, {1, 2, 3}, {0, 1, 2, 3}]

    """
    x = []
    for i in items[1:]:
        c = combinations(items, i)
        x.append(list(c))
    combos = list(map(make_sequence, list(flatten(x))))
    combos.append(make_sequence(items))
    return combos


def add(relset1, relset2):
    """Addition for relation sets is equivalent to set intersection."""
    return relset1.intersection(relset2)


# TODO: Don't embed the abbreviation dictionary in code; create a file for it
def abbrev(term_list):
    abbrev_dict = {"Point": "Pt",
                   "ProperInterval": "PInt",
                   "Interval": "Int"}
    return '|'.join([abbrev_dict[term] for term in term_list])


class Algebra(object):

    def __init__(self, filename):
        """An algebra is created from a JSON file containing the algebra's
        relation and transitivity table definitions.
        """
        with open(filename, 'r') as f:
            self.algebra_dict = json.load(f)

        self.name = self.algebra_dict["Name"]

        self.description = self.algebra_dict["Description"]

        # TODO: For consistency, rename relations_dict to rel_dict
        self.relations_dict = self.algebra_dict["Relations"]

        self.elements_bitset = bitset(self.name, tuple(self.relations_dict.keys()))  # A class object

        # TODO: Rename 'identity' to 'elements'
        self.elements = self.elements_bitset.supremum

        # Setup the transitivity table used by Relation Set multiplication
        self.transitivity_table = dict()
        tabledefs = self.algebra_dict["TransTable"]
        for rel1 in tabledefs:
            self.transitivity_table[rel1] = dict()
            for rel2 in tabledefs[rel1]:
                self.transitivity_table[rel1][rel2] = self.elements_bitset(tuple(tabledefs[rel1][rel2]))

    # Accessors for information about a given relation.

    def rel_name(self, rel):
        return self.relations_dict[rel]["Name"]

    def rel_domain(self, rel):
        return self.relations_dict[rel]["Domain"]

    def rel_range(self, rel):
        return self.relations_dict[rel]["Range"]

    def rel_reflexive(self, rel):
        return self.relations_dict[rel]["Reflexive"]

    def rel_symmetric(self, rel):
        return self.relations_dict[rel]["Symmetric"]

    def rel_transitive(self, rel):
        return self.relations_dict[rel]["Transitive"]

    def converse(self, rel_or_relset):
        """Return the converse of a relation (str) or relation set (bitset)."""
        if isinstance(rel_or_relset, str):
            return self.relations_dict[rel_or_relset]["Converse"]
        else:
            return self.elements_bitset((self.converse(r) for r in rel_or_relset.members()))

    def __str__(self):
        """Return a string representation of the Algebra."""
        return f"<{self.name}: {self.description}>"

    def relset(self, relations):
        """Return a relation set (bitset) for the given relations."""
        return self.elements_bitset(relations)

    def mult(self, relset1, relset2):
        """Multiplication is done, element-by-element, on the cross-product
        of the two sets using the algebra's transitivity table, and
        then reducing those results to a single relation set using set
        union.
        """
        result = self.elements_bitset.infimum  # the empty relation set
        for r1 in relset1:
            for r2 in relset2:
                result = result.union(self.transitivity_table[r1][r2])
        return result

    def check_multiplication_identity(self, verbose=False):
        """Check the validity of the multiplicative identity for every
        combination of singleton relset.  :param verbose: Print out
        the details of each test :return: True or False

        """
        count = 0
        result = True
        rels = self.elements
        for r in rels:
            r_rs = self.relset((r,))
            for s in rels:
                count += 1
                s_rs = self.relset((s,))
                prod1 = self.mult(r_rs, s_rs)
                prod2 = self.converse(self.mult(self.converse(s_rs), self.converse(r_rs)))
                if prod1 != prod2:
                    if verbose:
                        print("FAIL:")
                        print(f"      r    = {r_rs}")
                        print(f"      s    = {s_rs}")
                        print(f"( r *  s)  = {prod1}")
                        print(f"(si * ri)i = {prod2}")
                        print(f"{prod1} != {prod2}")
                    result = False
        if verbose:
            print(f"\n{self.name} -- Multiplication Identity Check:")
        if result:
            if verbose:
                print(f"PASSED . {count} products tested.")
        else:
            if verbose:
                print("FAILED. See FAILURE output above.")
        return result

    def summary(self):
        """Print out a summary of this algebra and its elements."""
        print(f"  Algebra Name: {self.name}")
        print(f"   Description: {self.description}")
        # print(f" Equality Rels: {self.equality_relations}")
        print("     Relations:")
        print("{:>25s} {:>25s} {:>10s} {:>10s} {:>10s} {:>8s} {:>12s}".format("NAME (ABBREV)", "CONVERSE (ABBREV)",
                                                                              "REFLEXIVE", "SYMMETRIC", "TRANSITIVE",
                                                                              "DOMAIN", "RANGE"))
        # TODO: Vary spacing between columns based on max word lengths
        # For syntax used below see https://docs.python.org/3/library/string.html#format-string-syntax
        for r in self.elements:
            print(f"{self.rel_name(r):>19s} ({r:>3s}) "
                  f"{self.rel_name(self.converse(r)):>19s} ({self.converse(r):>3s}) "
                  f"{self.rel_reflexive(r)!s:>8} {self.rel_symmetric(r)!s:>10} {self.rel_transitive(r)!s:>10}"
                  f"{abbrev(self.rel_domain(r))!s:>11} {abbrev(self.rel_range(r))!s:>13}")
        # TODO: Don't hardcode the legend below; make it depend on an abbreviations file (JSON)
        print("\nDomain & Range Abbreviations:")
        print("   Pt = Point")
        print(" PInt = Proper Interval")

    def is_associative(self, verbose=False):
        result = True
        countskipped = 0
        countok = 0
        countfailed = 0
        counttotal = 0
        rels = self.elements
        for _a in rels:
            for _b in rels:
                for _c in rels:
                    if verbose:
                        print(f"{_a} x {_b} x {_c} :")
                    a_rs = self.relset((_a,))
                    b_rs = self.relset((_b,))
                    c_rs = self.relset((_c,))
                    if set(self.rel_range(_a)) & set(self.rel_domain(_b)):
                        prod_ab = a_rs * b_rs
                        prod_ab_c = prod_ab * c_rs
                        if set(self.rel_range(_b)) & set(self.rel_domain(_c)):
                            prod_bc = b_rs * c_rs
                            prod_a_bc = a_rs * prod_bc
                            if not (prod_ab_c == prod_a_bc):
                                if verbose:
                                    print(f"  Associativity fails for a = {a_rs}, b = {b_rs}, c = {c_rs}")
                                    print(
                                        f"    associativity check: {self.rel_range(_a)}::{self.rel_domain(_b)} \
                                        {self.rel_range(_b)}::{self.rel_domain(_c)}")
                                    print(f"    (a * b) * c = {prod_ab_c}")
                                    print(f"    a * (b * c) = {prod_a_bc}")
                                countfailed += 1
                                counttotal += 1
                                result = False
                            else:
                                if verbose:
                                    print("  Associativity OK")
                                countok += 1
                                counttotal += 1
                        else:
                            if verbose:
                                print(
                                    f"  Skipping check due to b x c: {self.rel_range(_b)}::{self.rel_domain(_c)}")
                            countskipped += 1
                            counttotal += 1
                    else:
                        if verbose:
                            print(f"  Skipping check due to a x b: {self.rel_range(_a)}::{self.rel_domain(_b)}")
                        countskipped += 1
                        counttotal += 1
        print(f"\nTEST SUMMARY: {countok} OK, {countskipped} Skipped, {countfailed} Failed ({counttotal} Total)")
        numrels = len(rels)
        totaltests = numrels * numrels * numrels
        if counttotal != totaltests:
            print(f"Test counts do not add up; Total should be {totaltests}")
        return result


class Network(nx.DiGraph):

    def __init__(self, algebra, name=None):
        self.algebra = algebra
        super().__init__(name=name)

    def __str__(self):
        return f"<Network--{self.name}--{self.algebra.name}>"

    def add_constraint(self, entity1, entity2, relation_set=None):
        """Same as add_edge, except that two edges are added with converse constraints."""
        if relation_set:
            self.add_edge(entity1, entity2, constraint=relation_set)
            self.add_edge(entity2, entity1, constraint=self.algebra.converse(relation_set))
        else:
            self.add_edge(entity1, entity2, constraint=self.algebra.elements)
            self.add_edge(entity2, entity1, constraint=self.algebra.elements)

    @property
    def constraints(self):
        return self.edges

    @property
    def entities(self):
        return self.nodes

    def __set_unconstrained_values(self):
        ident = self.algebra.elements
        for ent1 in self.nodes:
            for ent2 in self.nodes:
                if ent1 in self.__constraints:
                    if ent2 in self.__constraints[ent1]:
                        pass
                    else:
                        self.constraint(ent1, ent2, ident)
                else:
                    if ent2 in self.__constraints:
                        if ent1 in self.__constraints[ent2]:
                            pass
                        else:
                            self.constraint(ent1, ent2, ident)
                    else:
                        self.constraint(ent1, ent2, ident)

    def propagate(self, verbose=False):
        """Propagate constraints in the network.
        @param verbose: Print number of loops as constraints are propagated.

        """
        loop_count = 0
        self.__set_unconstrained_values()
        something_changed = True  # Start off with this True so we'll loop at least once
        while something_changed:
            something_changed = False  # Immediately set to False; if nothing changes, we'll only loop once
            loop_count += 1
            for ent1 in self.__entities:
                for ent2 in self.__entities:
                    prod = self.__algebra.identity_relset
                    c12 = self.__constraints[ent1][ent2]
                    for ent3 in self.__entities:
                        c13 = self.__constraints[ent1][ent3]
                        c32 = self.__constraints[ent3][ent2]
                        prod = prod + (c13 * c32)
                    if prod != c12:
                        something_changed = True  # Need to continue top-level propagation loop
                    self.__constraints[ent1][ent2] = prod
        if verbose:
            print("Number of propagation loops: %d".format(loop_count))

    def summary(self):
        """Print out a summary of this network and its nodes, edges, and constraints."""
        print(f"{self.name}: {len(self.nodes)} nodes, {len(self.edges)} edges")
        # print("  Head")
        # print("    Tail: (Constraints)")
        for head in self.nodes:
            print(f"  {head.name}:")
            for tail in self.neighbors(head):
                print(f"    => {tail.name}: {list(self.edges[head, tail]['constraint'].members())}")


# See https://www.w3.org/TR/owl-time/
class TemporalEntity(object):
    types = ["Point", "ProperInterval", "Duration"]

    def __init__(self, types, name=None, start=None, end=None, dur=None):
        self.__type = types
        self.__name = name
        self.__start = start
        self.__end = end
        self.__duration = dur

    @property
    def name(self):
        return self.__name

    def gettype(self):
        return self.__type

    def settype(self, typ):
        self.__type = typ

    def __repr__(self):
        if self.__name:
            return f"<TemporalEntity {self.__name} {self.__type}>"
        else:
            return f"<TemporalEntity {self.__type}>"


# Don't have a good source yet for a spatial vocabulary,
# but see https://www.w3.org/2017/sdwig/bp/
class SpatialEntity(object):

    def __init__(self, types, name=None):
        self.__type = types
        self.__name = name

    @property
    def name(self):
        return self.__name

    def gettype(self):
        return self.__type

    def settype(self, typ):
        self.__type = typ

    def __repr__(self):
        if self.__name:
            return f"<SpatialObject {self.__name} {self.__type}>"
        else:
            return f"<SpatialObject {self.__type}>"


if __name__ == '__main__':

    import os

    path = os.path.join(os.getenv('PYPROJ'), 'qualreas')

    alg = [Algebra(os.path.join(path, "Algebras/IntervalAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/IntervalAndPointAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/LeftBranchingIntervalAndPointAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/RightBranchingIntervalAndPointAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/rcc8Algebra.json")),
           Algebra(os.path.join(path, "Algebras/linearPointAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/rightBranchingPointAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/leftBranchingPointAlgebra.json"))
           ]

    for a in alg:
        print("\n{}:".format(a.name))
        print("Relations {}: ".format(a.elements))
        if a.check_multiplication_identity():
            print("Multiplication Identity OK for {}.".format(a.name))
        else:
            print("Multiplication Identity Failed for {}.".format(a.name))

    print("{}:".format(alg[0].name))
    entity_x = TemporalEntity(["ProperInterval"], "X")
    entity_y = TemporalEntity(["ProperInterval"], "Y")
    entity_z = TemporalEntity(["ProperInterval"], "Z")
    r12 = alg[0].relset(["B"])
    r23 = alg[0].relset(["D"])
    print("\n")
    print(f"Constraint: {entity_x.name} {list(r12.members())} {entity_y.name}")
    print(f"Constraint: {entity_y.name} {list(r23.members())} {entity_z.name}")
    net0 = Network(alg[0], "Test0")
    net0.add_constraint(entity_x, entity_y, r12)
    net0.add_constraint(entity_y, entity_z, r23)
    net0.summary()
    #net0.propagate(verbose=True)
    #net0.print_constraints()
    print("\n")

    # print("{}:".format(alg[1].name))
    # entity_x1 = TemporalObject(["Point", "ProperInterval"], "X1")
    # entity_y1 = TemporalObject(["Point", "ProperInterval"], "Y1")
    # entity_z1 = TemporalObject(["Point", "ProperInterval"], "Z1")
    # s12 = alg[1].relations["B"]
    # s23 = alg[1].relations["D"]
    # print("\n")
    # print("Constraint: {} {} {}".format(entity_x1, s12.long_name, entity_y1))
    # print("Constraint: {} {} {}".format(entity_y1, s23.long_name, entity_z1))
    # net1 = Network(alg[1], "Test1")
    # net1.constraint(entity_x1, entity_y1, [s12])
    # net1.constraint(entity_y1, entity_z1, [s23])
    # # net1.constraint(entity_x1, entity_z1)
    # net1.print_constraints()
    # net1.propagate(verbose=True)
    # net1.print_constraints()
    # print("\n")
    #
    # # Example in book on constraint processing for temporal reasoning
    # pint_I = TemporalObject(["ProperInterval"], "I")
    # pint_J = TemporalObject(["ProperInterval"], "J")
    # pint_K = TemporalObject(["ProperInterval"], "K")
    # pint_L = TemporalObject(["ProperInterval"], "L")
    # D0 = alg[0].relations["D"]
    # DI0 = alg[0].relations["DI"]
    # F0 = alg[0].relations["F"]
    # FI0 = alg[0].relations["FI"]
    # M0 = alg[0].relations["M"]
    # O0 = alg[0].relations["O"]
    # S0 = alg[0].relations["S"]
    # net2 = Network(alg[0], "Book Example")
    # net2.constraint(pint_I, pint_J, [F0, FI0])
    # net2.constraint(pint_I, pint_L, [S0, M0])
    # net2.constraint(pint_L, pint_J, [S0, M0])
    # net2.constraint(pint_K, pint_I, [D0, DI0])
    # net2.constraint(pint_K, pint_J, [D0, DI0])
    # net2.constraint(pint_L, pint_K, [O0])
    # net2.print_constraints()
    # net2.propagate(verbose=True)
    # net2.print_constraints()
    #
    # # Example in book on constraint processing for temporal reasoning
    # # (extended to intervals & points)
    # pint_I = TemporalObject(["Point", "ProperInterval"], "I")
    # pint_J = TemporalObject(["Point", "ProperInterval"], "J")
    # pint_K = TemporalObject(["Point", "ProperInterval"], "K")
    # pint_L = TemporalObject(["Point", "ProperInterval"], "L")
    # D1 = alg[1].relations["D"]
    # DI1 = alg[1].relations["DI"]
    # F1 = alg[1].relations["F"]
    # FI1 = alg[1].relations["FI"]
    # M1 = alg[1].relations["M"]
    # O1 = alg[1].relations["O"]
    # S1 = alg[1].relations["S"]
    # net2x = Network(alg[1], "Book Example Extended")
    # net2x.constraint(pint_I, pint_J, [F1, FI1])
    # net2x.constraint(pint_I, pint_L, [S1, M1])
    # net2x.constraint(pint_L, pint_J, [S1, M1])
    # net2x.constraint(pint_K, pint_I, [D1, DI1])
    # net2x.constraint(pint_K, pint_J, [D1, DI1])
    # net2x.constraint(pint_L, pint_K, [O1])
    # net2x.print_constraints()
    # net2x.propagate(verbose=True)
    # net2x.print_constraints()
    #
    # # Associativity example done as a network instead
    # x1 = TemporalObject(["Point", "ProperInterval"], "X")
    # y1 = TemporalObject(["Point", "ProperInterval"], "Y")
    # z1 = TemporalObject(["Point", "ProperInterval"], "Z")
    # u1 = TemporalObject(["Point", "ProperInterval"], "U")
    # ps1 = alg[1].relations["PS"]
    # b1 = alg[1].relations["B"]
    # d1 = alg[1].relations["D"]
    # net3 = Network(alg[1], "Associativity Test")
    # net3.constraint(x1, y1, [ps1])
    # net3.constraint(y1, z1, [b1])
    # net3.constraint(z1, u1, [d1])
    # net3.print_constraints()
    # net3.propagate(verbose=True)
    # net3.print_constraints()
    #
    # print("\n{} is associative? {}\n".format(alg[0].name, str(alg[0].is_associative())))
    # #    print "\n{} is associative? {}\n" % (alg[1].short_name, str(alg[1].is_associative(verbose=True)))
    # #    print "\n{} is associative? {}" % (alg2.short_name, str(alg2.is_associative()))
    # #    print "\n{} is associative? {}" % (alg3.short_name, str(alg3.is_associative()))
    # #    print "\n{} is associative? {}" % (alg4.short_name, str(alg4.is_associative()))
    #
    # # Region Connection Calculus 8:
    #
    # # Example from http://en.wikipedia.org/wiki/RCC8
    # alg4 = Algebra(os.path.join(path, "Algebras/rcc8Algebra.json"))
    #
    # DC = alg4.relations['DC']
    # EC = alg4.relations['EC']
    # PO = alg4.relations['PO']
    # TPP = alg4.relations['TPP']
    # NTPP = alg4.relations['NTPP']
    # TPPI = alg4.relations['TPPI']
    # NTPPI = alg4.relations['NTPPI']
    # EQ = alg4.relations['EQ']
    #
    # house1 = SpatialObject(["Region"], "house1")
    # house2 = SpatialObject(["Region"], "house2")
    # property1 = SpatialObject(["Region"], "property1")
    # property2 = SpatialObject(["Region"], "property2")
    # road = SpatialObject(["Region"], "road")
    # net4 = Network(alg4, "Wikipedia RCC8 Example")
    #
    # net4.constraint(house1, house2, [DC])
    # net4.constraint(house1, property1, [TPP, NTPP])
    # net4.constraint(house1, property2, [DC, EC])
    # net4.constraint(house1, road, [EC])
    # net4.constraint(house2, property1, [DC, EC])
    # net4.constraint(house2, property2, [NTPP])
    # net4.constraint(house2, road, [EC])
    # net4.constraint(property1, property2, [DC, EC])
    # net4.constraint(road, property1, [DC, EC, TPP, TPPI, PO, EQ, NTPP, NTPPI])
    # net4.constraint(road, property2, [DC, EC, TPP, TPPI, PO, EQ, NTPP, NTPPI])
    #
    # net4.print_constraints()
    # net4.propagate(verbose=True)
    # net4.print_constraints()

    # Note: According to Wikipedia, the correct constraints
    # between 'road' and 'property1', and
    # between 'road' and 'property2' are:
    #   road { PO, EC } property1
    #   road { PO, TPP } property2

    # End of File
