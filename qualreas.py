"""
@author: Alfred J. Reich, Ph.D.

"""

from bitsets import bitset, bases
import json
import networkx as nx
# from copy import deepcopy
from functools import reduce
from collections import abc


__author__ = 'Alfred J. Reich'
__version__ = '0.3.0'

# Map 4-Point Network "Signatures" to Typical Names
key_name_mapping = {
      '<,<,<,<': 'B',       '>,>,>,>': 'BI',
      '>,<,>,<': 'D',       '<,<,>,>': 'DI',
      '=,<,>,=': 'E',       '=,=,=,=': 'PE',
      '>,<,>,=': 'F',       '<,<,>,=': 'FI',
      '<,<,=,<': 'M',       '>,=,>,>': 'MI',
      '<,<,>,<': 'O',       '>,<,>,>': 'OI',
      '=,<,>,<': 'S',       '=,<,>,>': 'SI',
      '>,=,>,=': 'PF',      '<,<,=,=': 'PFI',
      '=,<,=,<': 'PS',      '=,=,>,>': 'PSI',
     '<,<,>,r~': 'RO',    '<,<,r~,r~': 'RB',
     '=,<,>,r~': 'RS',     '>,<,>,r~': 'ROI',
    '>,r~,>,r~': 'RBI', 'r~,r~,r~,r~': 'R~',
     'l~,<,>,<': 'LO',     'l~,<,>,=': 'LF',
     'l~,<,>,>': 'LOI',   'l~,l~,>,>': 'LBI',
    'l~,<,l~,<': 'LB',  'l~,l~,l~,l~': 'L~'
}


class RelSet(bases.BitSet):

    def __str__(self):
        return "|".join(self.members())

    def __add__(self, rs):
        return self.intersection(rs)


# See https://www.w3.org/TR/owl-time/
# classes: "Point", "ProperInterval", "Duration"
class TemporalEntity(object):

    def __init__(self, classes, name=None, start=None, end=None, dur=None):
        self.classes = classes  # Ontological, not OOP; e.g., Point, ProperInterval
        self.name = name
        self.start = start
        self.end = end
        self.duration = dur

    def __repr__(self):
        if self.name:
            return f"<TemporalEntity {self.name} {self.classes}>"
        else:
            return f"<TemporalEntity {self.classes}>"


# Don't have a good source yet for a spatial vocabulary,
# but see https://www.w3.org/2017/sdwig/bp/
class SpatialEntity(object):

    def __init__(self, classes, name=None):
        self.classes = classes  # Ontological, not OOP
        self.name = name

    def __repr__(self):
        if self.name:
            return f"<SpatialObject {self.name} {self.classes}>"
        else:
            return f"<SpatialObject {self.classes}>"


# Abbreviations for Algebra Summary
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

        # self.elements_bitset = bitset(self.name, tuple(self.relations_dict.keys()))  # A class object
        self.elements_bitset = bitset('relset', tuple(self.relations_dict.keys()), base=RelSet)

        # TODO: Rename 'identity' to 'elements'
        self.elements = self.elements_bitset.supremum

        # The equality relations of the algebra
        self.__equality_relations = self.relset([rel for rel in self.elements if self.rel_equality(rel)])

        # Populate a dictionary that allows equality relations to be looked-up based on their domain/range.
        self.equality_relations_dict = dict()
        for eqrel in self.__equality_relations:
            dom = self.rel_domain(eqrel)[0]  # Get the single item out of the eqrel's domain set.
            self.equality_relations_dict[dom] = self.relset([eqrel])

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

    def rel_equality(self, rel):
        """If a relation is reflexive, symmetric, and transitive, then it is an
        equivalence relation, called equality here."""
        return self.rel_reflexive(rel) & self.rel_symmetric(rel) & self.rel_transitive(rel)

    def converse(self, rel_or_relset):
        """Return the converse of a relation (str) or relation set (bitset)."""
        if isinstance(rel_or_relset, str):
            return self.relations_dict[rel_or_relset]["Converse"]
        else:
            return self.elements_bitset((self.converse(r) for r in rel_or_relset.members()))

    def __str__(self):
        """Return a string representation of the Algebra."""
        return f"<{self.name}: {self.description}>"

    @property
    def equality_relations(self):
        """Return all of the algebra's equality relations."""
        return self.__equality_relations

    def equality_relation(self, domain_or_range):
        return self.equality_relations_dict[domain_or_range]

    def relset(self, relations):
        """Return a relation set (bitset) for the given relations."""
        if isinstance(relations, str):  # Assumed to be something like 'B|M|O'
            return self.string_to_relset(relations)
        elif isinstance(relations, abc.Iterable):  # e.g., ['B','M','O'] or ('B',)
            return self.elements_bitset(relations)
        else:
            raise TypeError("Input must be a string, list, tuple, or set.")

    def string_to_relset(self, string, delimiter='|'):
        """Take a string like 'B|M|O' and turn it into a relation set."""
        return self.relset(string.split(delimiter))

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
        print(f" Equality Rels: {self.equality_relations}")
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


# Used to break out of Network propagation if it is found to be inconsistent
class InconsistentNetwork(Exception):
    pass


class Network(nx.DiGraph):

    def __init__(self, algebra, name=None):
        self.algebra = algebra
        super().__init__(name=name)

    def __str__(self):
        return f"<Network--{self.name}--{self.algebra.name}>"

    def remove_constraint(self, entity1, entity2):
        # Remove edges in both directions
        if self.has_edge(entity1, entity2):
            self.remove_edge(entity1, entity2)
        if self.has_edge(entity2, entity1):
            self.remove_edge(entity2, entity1)

    def __set_equality_constraint(self, entity, equality_rels, verbose):
        if not self.has_edge(entity, entity):
            self.add_edge(entity, entity, constraint=equality_rels)
            if verbose:
                print(f"Equality Constraint Added: {entity.name} {list(equality_rels.members())}")

    def __set_unconstrained_values(self, verbose):
        """Find all pairs of nodes (not the same) that don't have a constraint set
        between them, and set the constraint to be all algebra elements.  Meaning that,
        any constraint between them is possible."""
        for ent1 in self.nodes():
            for ent2 in self.nodes():
                if (ent1 != ent2) and not self.has_edge(ent1, ent2):
                    self.add_constraint(ent1, ent2, self.algebra.elements, verbose)

    def add_constraint(self, entity1, entity2, relation_set=None, verbose=False):
        """Same as add_edge, except that two edges are added with converse constraints."""

        # Get the proper equality relation(s) for each of the two entities
        eq_rels1 = reduce(lambda r1, s1: r1.union(s1),
                          (map(lambda t1: self.algebra.equality_relation(t1),
                               entity1.classes)))
        eq_rels2 = reduce(lambda r2, s2: r2.union(s2),
                          (map(lambda t2: self.algebra.equality_relation(t2),
                               entity2.classes)))

        # Each entity must equal itself
        self.__set_equality_constraint(entity1, eq_rels1, verbose)
        self.__set_equality_constraint(entity2, eq_rels2, verbose)

        # Override any previously set constraint on this pair of entities
        self.remove_constraint(entity1, entity2)

        # Handle different expressions for a relation set:
        # If None, then use all relations (elements) as constraint
        if not relation_set:
            rel_set = self.algebra.elements
        # If it's a string, assume it's in the form 'a' or 'a|b|c'
        elif isinstance(relation_set, str):
            rel_set = self.algebra.string_to_relset(relation_set)
        # Or maybe it's actually a RelSet
        elif isinstance(relation_set, RelSet):
            rel_set = relation_set
        # Otherwise, throw an exception
        else:
            raise TypeError("relation_set must be None, a String, or a RelSet")

        # Add the constraint and it's converse
        rel_set_converse = self.algebra.converse(rel_set)
        self.add_edge(entity1, entity2, constraint=rel_set)
        self.add_edge(entity2, entity1, constraint=rel_set_converse)

        if verbose:
            print(f"Constraint Added: {entity1.name} {entity2.name} {list(rel_set.members())}")
            print(f"Constraint Added: {entity2.name} {entity1.name} {list(rel_set_converse.members())}")

    # TODO: Write transpose method for networks
    # def transpose(self, other):
    #     """Viewing this network as a matrix, return a copy that is its transpose."""
    #     pass

    # TODO: Write converse method for networks
    # def converse(self):
    #     """Return a copy of this network where all of the elements are converses of the original."""
    #     net_copy = deepcopy(self)
    #     for node1 in net_copy:
    #         for node2 in net_copy:
    #             constraint12 = net_copy.edges(node1, node2)['constraint']
    #             net_copy.edges(node1, node2)['constraint'] = self.algebra.converse(constraint12)
    #     return net_copy

    # def copy(self):
    #     """Return a deep copy of this network."""
    #     return deepcopy(self)

    @property
    def constraints(self):
        return self.edges

    @property
    def entities(self):
        return self.nodes

    def get_entity_by_name(self, name):
        """Return the node (entity) with the input name. If more than one have the same name,
        then the first one found is returned.  So, try to give entities different names."""
        result = None
        for node in self.nodes:
            if node.name == name:
                result = node
                break
        return result

    def to_list(self, entities=None):
        """Return a list of lists of constraints, where the lists in the list represent
        rows of a matrix of constraints, ordered by the ordering in the list of entities."""
        if not entities:
            entities = self.nodes
        result = []
        for row_ent in entities:
            row = []
            for col_ent in entities:
                row.append(str(self.edges[row_ent, col_ent]['constraint']))
            result.append(row)
        return result

    # def print_as_matrix(self, node_names=None):
    #     """Print the Network constraints in matrix form using the ordering of entities
    #     as given by their names in node_names or, if that's None, then by the ordering
    #     returned by the method self.nodes."""
    #     if not node_names:
    #         nodes_list = list(self.nodes)
    #         node_names = list(map(lambda x: x.name, nodes_list))
    #     else:
    #         nodes_list = list(map(lambda nm: self.get_entity_by_name(nm), node_names))
    #     print(node_names)
    #     for row_node in nodes_list:
    #         row = ""
    #         for col_node in nodes_list:
    #             row += "  " + str(self.edges[row_node, col_node]['constraint'])
    #         print(row)

    def propagate(self, verbose=False):
        """Propagate constraints in the network. Constraint propagation is a fixed-point iteration of a square
        constraint matrix.  Or, in plain English, we treat the network as if it's a matrix, multiplying it by
        itself, repeatedly, until it stops changing.
        @param verbose: Print number of iterations required to propagate constraints.
        """
        loop_count = 0
        self.__set_unconstrained_values(verbose)
        something_changed = True  # We'll iterate at least once
        try:
            while something_changed:
                something_changed = False  # If nothing changes, we'll only iterate once
                loop_count += 1
                for ent1 in self.nodes():
                    for ent2 in self.nodes():
                        prod = self.algebra.elements
                        c12 = self.edges[ent1, ent2]['constraint']
                        for ent3 in self.nodes():
                            c13 = self.edges[ent1, ent3]['constraint']
                            c32 = self.edges[ent3, ent2]['constraint']
                            prod += self.algebra.mult(c13, c32)
                        if prod != c12:
                            something_changed = True  # Continue iterating
                        self.edges[ent1, ent2]['constraint'] = prod
                        # If any product is empty then the Network is inconsistent
                        if not prod.any():
                            raise InconsistentNetwork
            if verbose:
                print(f"Number of iterations: {loop_count}")
            return True
        except InconsistentNetwork:
            if verbose:
                print(f"Propagation suspended; the network is inconsistent.")
            return False

    def summary(self):
        """Print out a summary of this network and its nodes, edges, and constraints."""
        print(f"\n{self.name}: {len(self.nodes)} nodes, {len(self.edges)} edges")
        print(f"  Algebra: {self.algebra.name}")
        for head in self.nodes:
            print(f"  {head.name}:")
            for tail in self.neighbors(head):
                print(f"    => {tail.name}: {str(self.edges[head, tail]['constraint'])}")


class FourPoint(Network):
    """Create four Temporal Entities that represent time points and use them
    to express two independent intervals. For example, (s1,e1) and (s2,e2),
    where s1 < e1 and s2 < e2, represents two proper intervals.  Using '<|='
    instead of '<', would represent two intervals where one or both might
    be points.  Return the network and the four temporal entities."""

    def __init__(self, algebra, name, lessthanstr, startname="StartPt", endname="EndPt"):
        self.algebra = algebra
        self.lessthan = algebra.relset(lessthanstr)
        # Start & End Points of Interval 1
        self.start1 = TemporalEntity(["Point"], name=startname + "1")
        self.end1 = TemporalEntity(["Point"], name=endname + "1")
        # Start & End Points of Interval 2
        self.start2 = TemporalEntity(["Point"], name=startname + "2")
        self.end2 = TemporalEntity(["Point"], name=endname + "2")
        super().__init__(algebra, name)
        self.add_constraint(self.start1, self.end1, self.lessthan, verbose=False)
        self.add_constraint(self.start2, self.end2, self.lessthan, verbose=False)

    def get_points(self):
        return [self.start1, self.end1, self.start2, self.end2]


if __name__ == '__main__':

    print("\n=======================================================================")

    import os

    path = os.path.join(os.getenv('PYPROJ'), 'qualreas')

    alg = [Algebra(os.path.join(path, "Algebras/LinearIntervalAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/ExtendedLinearIntervalAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/LeftBranchingIntervalAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/RightBranchingIntervalAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/RCC8Algebra.json")),
           Algebra(os.path.join(path, "Algebras/LinearPointAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/RightBranchingPointAlgebra.json")),
           Algebra(os.path.join(path, "Algebras/LeftBranchingPointAlgebra.json"))
           ]

    print("\n-------------------------------------")
    print("Check algebra multiplication identity")
    print("-------------------------------------")

    verbosity = False

    for a in alg:
        print(f"\n{a.name}:")
        print(f"Relations: {a.elements}")
        if a.check_multiplication_identity():
            print("Multiplication Identity OK")
        else:
            print("Multiplication Identity Failed")

    print("\n-----------------------------------------------")
    print("Check network propagation for interval algebras")
    print("-----------------------------------------------")

    # Interval Algebras

    entity_x = TemporalEntity(["ProperInterval"], "X")
    entity_y = TemporalEntity(["ProperInterval"], "Y")
    entity_z = TemporalEntity(["ProperInterval"], "Z")

    for a in alg[0:4]:
        print("\n--------------------------------------------------")
        print(f"Algebra: {a.name}")
        net = Network(a, f"Network-{a.name}")
        net.add_constraint(entity_x, entity_y, "B", verbosity)
        net.add_constraint(entity_y, entity_z, "D", verbosity)
        net.summary()
        net.propagate(True)
        net.summary()

    # Point Algebras

    entity_x = TemporalEntity(["Point"], "X")
    entity_y = TemporalEntity(["Point"], "Y")
    entity_z = TemporalEntity(["Point"], "Z")

    for a in alg[5:]:
        print("\n--------------------------------------------------")
        print(f"Algebra: {a.name}")
        net = Network(a, f"Network-{a.name}")
        net.add_constraint(entity_x, entity_y, "<", verbosity)
        net.add_constraint(entity_y, entity_z, "<", verbosity)
        net.summary()
        net.propagate()
        net.summary()

    # RCC8 Algebra

    entity_x = SpatialEntity(["Region"], "X")
    entity_y = SpatialEntity(["Region"], "Y")
    entity_z = SpatialEntity(["Region"], "Z")

    a = alg[4]
    print("\n--------------------------------------------------")
    print(f"Algebra: {a.name}")
    net = Network(a, f"Network-{a.name}")
    net.add_constraint(entity_x, entity_y, "NTPP", verbosity)
    net.add_constraint(entity_y, entity_z, "NTPP", verbosity)
    net.summary()
    net.propagate()
    net.summary()

    print("\n---------------------------------------------------------------")
    print("Example in book on constraint processing for temporal reasoning")
    print("---------------------------------------------------------------")
    pint_I = TemporalEntity(["ProperInterval"], "I")
    pint_J = TemporalEntity(["ProperInterval"], "J")
    pint_K = TemporalEntity(["ProperInterval"], "K")
    pint_L = TemporalEntity(["ProperInterval"], "L")
    net2 = Network(alg[0], "Book Example")
    net2.add_constraint(pint_I, pint_J, "F|FI", verbosity)
    net2.add_constraint(pint_I, pint_L, "S|M", verbosity)
    net2.add_constraint(pint_L, pint_J, "S|M", verbosity)
    net2.add_constraint(pint_K, pint_I, "D|DI", verbosity)
    net2.add_constraint(pint_K, pint_J, "D|DI", verbosity)
    net2.add_constraint(pint_L, pint_K, "O", verbosity)
    net2.summary()
    net2.propagate()
    net2.summary()

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

    print("\n----------------------------------------------")
    print("Region Connection Calculus 8")
    print("Example from http://en.wikipedia.org/wiki/RCC8")
    print("----------------------------------------------")

    alg4 = Algebra(os.path.join(path, "Algebras/RCC8Algebra.json"))

    house1 = SpatialEntity(["Region"], "house1")
    house2 = SpatialEntity(["Region"], "house2")
    property1 = SpatialEntity(["Region"], "property1")
    property2 = SpatialEntity(["Region"], "property2")
    road = SpatialEntity(["Region"], "road")

    net4 = Network(alg4, "Wikipedia RCC8 Example")

    net4.add_constraint(house1, house2, "DC", verbosity)
    net4.add_constraint(house1, property1, "TPP|NTPP", verbosity)
    net4.add_constraint(house1, property2, "DC|EC", verbosity)
    net4.add_constraint(house1, road, "EC", verbosity)
    net4.add_constraint(house2, property1, "DC|EC", verbosity)
    net4.add_constraint(house2, property2, "NTPP", verbosity)
    net4.add_constraint(house2, road, "EC", verbosity)
    net4.add_constraint(property1, property2, "DC|EC", verbosity)

    net4.summary()
    net4.propagate()
    net4.summary()

    # Note: According to Wikipedia, the correct constraints
    # between 'road' and 'property1', and
    # between 'road' and 'property2' are:
    #   road property1 EC|PO
    #   road property2 PO|TPP

    # End of File
