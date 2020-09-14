"""
@author: Alfred J. Reich

"""
# https://bitsets.readthedocs.io/en/stable/
from bitsets import bitset, bases
import json
import random
import string
import networkx as nx
# from copy import deepcopy
from functools import reduce
from collections import abc
import numpy as np

__author__ = 'Alfred J. Reich'
__version__ = '0.4.0'


def make_name(name=None, prefix="Network:", size=8):
    """If no name, then return a random name; otherwise return name."""
    if not name:
        chars = string.ascii_letters + string.digits + '!@#$%&*'
        name = prefix + "".join([random.choice(chars) for _ in range(size)])
    return name


# The fundamental algebraic elements here are SETS of relations, not individual relations.
# An individual relation, r, relates two temporal entities (te), e.g, teA r teB.  Sets
# of relations denote disjunctions, e.g., teA {r,s} teB <==> (teA r teB) or (teA s teB).
# Here, we use '|' to denote 'or' and we abbreviate sets like {r,s} with 'r|s'.  All of
# the relation sets (referred to here as "relsets") are finite and come from a finite
# population of relations. The functionality needed to implement such finite sets of relations
# is provided for by the BitSet module and all we really need to do is extend it a bit (no pun
# intended) to allow for the abbreviation mentioned, above, and an addition (+) operation,
# which is really just set intersection.  We would include the compose operation also, using
# the multiply operator (*), however, that operation is dependent on Algebra being used,
# so it can only be defined within the context of an Algebra, as a method (see farther below).

class RelSet(bases.BitSet):

    def __str__(self):
        return "|".join(self.members())

    def __add__(self, rs):
        return self.intersection(rs)


# Spatial and Temporal Entities:
#
# Since the focus here is on relations between spatial & temporal entities, the reification
# of those entities, as actual classes, would seem to be unnecessary.  However, all relations
# have both a DOMAIN and a RANGE, which denote the ontological classes of the entities being
# related.  In Allen's original algebra of time intervals, the only ontological
# class supported is the proper time interval; not points, nor improper time intervals.
# And, since Allen's algebra only supported one class, domains and ranges could, and were,
# essentially ignored in his paper and much subsequent work. (Some consideration was given to
# whether time intervals included their end points or not, but nothing was put into a rigorous
# mathematical context in early papers.)  The algebras defined and developed in this module,
# however, support multiple ontological classes, e.g., time points (or instants) and proper
# time intervals.  Hence, it is necessary to store information about domains and ranges
# somewhere.  Temporal and Spatial Entities are convenient for doing that.  They may also be
# used for storing metric information by some potential, future add-on to this module.
# Additionally, they can also be used as nodes in a network of spatio-temporal constraints.

# Also, a note on domains and ranges in the context of relation composition:
# All relations have a domain and a range.  If D1, R1, D2, and R2 are the domains and ranges
# of relations r1 & r2, resp., then the composition of r1 and r2 (written r1;r2 in algebraic
# logic literature) requires that the intersection of R1 and D2 be non-empty.  To see why,
# consider what the composition means wrt the associated Temporal Entities, teA, teB, and
# teC, where (teA r1 teB) and (teB r2 teC).  The ontological classes that teB belongs to
# must include the range of r1 (R1) and the domain of r2 (D2) for r1;r2 to make sense.
#
#                r1         r2
#          teA -----> teB -----> teC
#           D1       R1,D2        R2
#            |                    ^
#            |                    |
#            +--------------------+
#                     r1;r2
#
# Matrix multiplication, M x N, provides an analogy: the number of columns of M must
# match the number of rows of N.

# NOTE: Ontological classes can be organized hierarchically, and so can object-oriented
# programming (OOP) classes, so it might be tempting to use OOP to represent the ontology
# of spatio-temporal "objects" (entities), however, ontological classes are different,
# and so the classes to which a particular Temporal Entity belongs are stored, instead, as a
# list of ontological class name strings, in a field within the Temporal Entity
# object, using names that conform to those found in the W3.org's time ontology ("Point",
# "ProperInterval", "Duration").  See https://www.w3.org/TR/owl-time/.


class TemporalEntity:
    """A temporal entity, such as Time Instant/Point or Time Interval."""

    def __init__(self, classes, name=None):
        self.classes = classes  # Ontological Classes, e.g., Point, ProperInterval
        self.name = make_name(name=name, prefix="TE:", size=8)

    def __repr__(self):
        return f"TemporalEntity({self.classes} \'{self.name}\')"


# Don't have a good source yet for a spatial vocabulary,
# but see https://www.w3.org/2017/sdwig/bp/
class SpatialEntity:
    """A spatial entity, such as a spatial feature or thing (e.g., Point, Area)."""

    def __init__(self, classes, name=None):
        self.classes = classes  # Ontological, not OOP
        self.name = make_name(name=name, prefix="SE:", size=8)

    def __repr__(self):
        return f"SpatialObject({self.classes} \'{self.name}\')"


# The following dictionary is used when loading a JSON specification
# for a network so that entity classes can be resolved into class (type)
# constructors.
class_type_dict = {"ProperInterval": TemporalEntity,
                   "Point": TemporalEntity,
                   "Region": SpatialEntity}


# Abbreviations used by the Algebra Summary method:
# TODO: Create a separate file for this; or perhaps don't abbreviate at all
def abbrev(term_list):
    abbrev_dict = {"Point": "Pt",
                   "ProperInterval": "PInt",
                   "Interval": "Int",
                   "Region": "Reg"}
    return '|'.join([abbrev_dict[term] for term in term_list])


class Algebra:

    def __init__(self, filename):
        """An algebra is created from a JSON file containing the algebra's
        relation and transitivity table definitions.
        """
        with open(filename, 'r') as f:
            self.algebra_dict = json.load(f)

        self.name = self.algebra_dict["Name"]

        self.description = self.algebra_dict["Description"]

        self.rel_info_dict = self.algebra_dict["Relations"]

        self.elements_bitset = bitset('relset', tuple(self.rel_info_dict.keys()), base=RelSet)

        self.elements = self.elements_bitset.supremum

        # The equality relations of the algebra
        self.__equality_relations = self.relset([rel for rel in self.elements if self.rel_equality(rel)])

        # Create a dict to return equality relations, keyed on their domain or range name
        self.equality_relations_dict = dict()
        for eqrel in self.__equality_relations:
            dom = self.rel_domain(eqrel)[0]  # Get the single item out of the eqrel's domain set.
            self.equality_relations_dict[dom] = self.relset([eqrel])

        # Setup the transitivity (or composition) table to be used by Relation Set composition
        self.transitivity_table = dict()
        tabledefs = self.algebra_dict["TransTable"]
        for rel1 in tabledefs:
            self.transitivity_table[rel1] = dict()
            for rel2 in tabledefs[rel1]:
                self.transitivity_table[rel1][rel2] = self.elements_bitset(tuple(tabledefs[rel1][rel2]))

    # Accessors for information about a given relation:

    def rel_name(self, rel):
        return self.rel_info_dict[rel]["Name"]

    def rel_converse_name(self, rel):
        return self.rel_name(self.rel_info_dict[rel]["Converse"])

    def rel_domain(self, rel):
        return self.rel_info_dict[rel]["Domain"]

    def rel_range(self, rel):
        return self.rel_info_dict[rel]["Range"]

    def rel_reflexive(self, rel):
        return self.rel_info_dict[rel]["Reflexive"]

    def rel_symmetric(self, rel):
        return self.rel_info_dict[rel]["Symmetric"]

    def rel_transitive(self, rel):
        return self.rel_info_dict[rel]["Transitive"]

    def rel_equality(self, rel):
        """If a relation is reflexive, symmetric, and transitive, then it is an
        equivalence relation, called equality here."""
        return self.rel_reflexive(rel) & self.rel_symmetric(rel) & self.rel_transitive(rel)

    def converse(self, rel_or_relset):
        """Return the converse of a relation (str) or relation set (bitset).
        e.g., 'A before B' has converse 'B after A', so 'after' is the converse of 'before',
        and vice versa."""
        if isinstance(rel_or_relset, str):
            return self.rel_info_dict[rel_or_relset]["Converse"]
        else:
            return self.elements_bitset((self.converse(r) for r in rel_or_relset.members()))

    def __str__(self):
        """Return a string representation of the Algebra."""
        return f"<{self.name}: {self.description}>"

    @property
    def all_equality_relations(self):
        """Return all of the algebra's equality relations."""
        return self.__equality_relations

    def get_domain_or_range_equality_rel(self, domain_or_range):
        return self.equality_relations_dict[domain_or_range]

    def relset(self, relations):
        """Return a relation set (bitset) for the given relations."""
        if isinstance(relations, str):  # if relations is like 'B|M|O' or 'B', or ''
            if relations == '':
                return self.relset([])
            else:
                return self.string_to_relset(relations)
        elif isinstance(relations, abc.Iterable):  # relations is like ['B','M','O'], ('B',), or []
            return self.elements_bitset(relations)
        else:
            raise TypeError("Input must be a string, list, tuple, or set.")

    def string_to_relset(self, st, delimiter='|'):
        """Take a string, st, like 'B|M|O' and turn it into a relation set."""
        return self.relset(st.split(delimiter))

    def compose(self, relset1, relset2):
        """Composition is done, element-by-element, on the cross-product
        of the two sets using the algebra's transitivity table, and
        then reducing those results to a single relation set using set
        union.
        """
        result = self.elements_bitset.infimum  # the empty relation set
        for r1 in relset1:
            for r2 in relset2:
                result = result.union(self.transitivity_table[r1][r2])
        return result

    def check_composition_identity(self, verbose=False):
        """Check the validity of the composition identity for every
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
                prod1 = self.compose(r_rs, s_rs)
                prod2 = self.converse(self.compose(self.converse(s_rs), self.converse(r_rs)))
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
            print(f"\n{self.name} -- Composition Identity Check:")
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
        print(f" Equality Rels: {self.all_equality_relations}")
        print("     Relations:")
        print("{:>25s} {:>25s} {:>10s} {:>10s} {:>10s} {:>8s} {:>12s}".format("NAME (SYMBOL)", "CONVERSE (ABBREV)",
                                                                              "REFLEXIVE", "SYMMETRIC", "TRANSITIVE",
                                                                              "DOMAIN", "RANGE"))
        # TODO: Vary spacing between columns based on max word lengths
        # For syntax used below see https://docs.python.org/3/library/string.html#format-string-syntax
        for r in self.elements:
            print(f"{self.rel_name(r):>19s} ({r:>3s}) "
                  f"{self.rel_name(self.converse(r)):>19s} ({self.converse(r):>3s}) "
                  f"{self.rel_reflexive(r)!s:>8} {self.rel_symmetric(r)!s:>10} {self.rel_transitive(r)!s:>10}"
                  f"{abbrev(self.rel_domain(r))!s:>11} {abbrev(self.rel_range(r))!s:>13}")
        # TODO: Don't hard code the legend below; make it depend on an abbreviations file (JSON)
        print("\nDomain & Range Abbreviations:")
        print("   Pt = Point")
        print(" PInt = Proper Interval")

    def element_summary(self, rel_string_name):
        print(f"                  Symbol: {rel_string_name}")
        print(f"                    Name: {self.rel_name(rel_string_name)}")
        print(f"                  Domain: {self.rel_domain(rel_string_name)}")
        print(f"                   Range: {self.rel_range(rel_string_name)}")
        print(f"                Converse: {self.rel_converse_name(rel_string_name)}")
        print(f"           Is Reflexive?: {self.rel_reflexive(rel_string_name)}")
        print(f"           Is Symmetric?: {self.rel_symmetric(rel_string_name)}")
        print(f"          Is Transitive?: {self.rel_transitive(rel_string_name)}")
        print(f"Is an Equality Relation?: {self.rel_equality(rel_string_name)}")

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
        print(f"TEST SUMMARY: {countok} OK, {countskipped} Skipped, {countfailed} Failed ({counttotal} Total)")
        numrels = len(rels)
        totaltests = numrels * numrels * numrels
        if counttotal != totaltests:
            print(f"Test counts do not add up; Total should be {totaltests}")
        return result


# Used to break out of Network propagation if it is found to be inconsistent
class InconsistentNetwork(Exception):
    pass


# load_network reads a JSON file similar to the example below and returns the network
# that corresponds to it.
#
# {
#     "name": "RCC8 Example 1",
#     "algebra": "RCC8Algebra",
#     "abbreviations": {"?": "DC|EC|TPP|TPPI|PO|EQ|NTPP|NTPPI"},
#     "nodes": {
#         "h1": ["House1", "Region"],
#         "h2": ["House2", "Region"],
#         ...
#     },
#     "edges": [
#         ["h1", "h2", "DC"],
#         ["h1", "p1", "TPP|NTPP"],
#         ...
#     ]
# }

class Network(nx.DiGraph):

    # def __init__(self, algebra, name=None):
    #     self.algebra = algebra
    #     super().__init__(name=name)

    def __init__(self, algebra=None, name=None,
                 algebra_path=None, json_file_name=None, network_dict=None,
                 json_ext=".json"):
        # If an Algebra object is input then we're done
        if algebra:
            self.algebra = algebra
            super().__init__(name=make_name(name))
        # Else read from a JSON file or a Python dictionary
        else:
            if json_file_name:
                with open(json_file_name, "r") as json_file:
                    net_dict = json.load(json_file)
            else:
                net_dict = network_dict
            # At this point we're working with a dictionary
            self.algebra = Algebra(algebra_path + net_dict["algebra"] + json_ext)
            if "name" in net_dict:
                name = net_dict["name"]
            nodes = net_dict["nodes"]
            entities = {}
            for nkey, nspec in nodes.items():
                node_name = nspec[0]
                classes = nspec[1]
                # entities[nkey] = class_type_dict[nspec[1]](nspec[1:], nspec[0])
                entities[nkey] = class_type_dict[classes[0]](classes, node_name)
            super().__init__(name=make_name(name))
            for espec in net_dict["edges"]:
                if len(espec) == 3:
                    cons = espec[2]
                else:
                    cons = self.algebra.elements
                if cons in net_dict["abbreviations"]:
                    constraint = net_dict["abbreviations"][cons]
                else:
                    constraint = cons
                self.add_constraint(entities[espec[0]], entities[espec[1]], constraint)

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
                          (map(lambda t1: self.algebra.get_domain_or_range_equality_rel(t1),
                               entity1.classes)))
        eq_rels2 = reduce(lambda r2, s2: r2.union(s2),
                          (map(lambda t2: self.algebra.get_domain_or_range_equality_rel(t2),
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

    def __add__(self, other):
        """Combine this network with another network, and return the new, combined network."""
        new_net = Network(self.algebra, "")
        new_net.graph.update(other.graph)
        new_net.graph.update(self.graph)
        new_net.add_nodes_from(other.nodes(data=True))
        new_net.add_nodes_from(self.nodes(data=True))
        new_net.add_edges_from(other.edges(data=True))
        new_net.add_edges_from(self.edges(data=True))
        new_net.name = self.name + "+" + other.name
        return new_net

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

    def propagate(self, verbose=False):
        """Propagate constraints in the network. Constraint propagation is a fixed-point
        iteration of a square constraint matrix.  That is, we treat the network as if it's
        a matrix, multiplying it by itself, repeatedly, until it stops changing.
        The algebra's compose method plays the role of multiplication and the RelSet +
        operation plays the role of addition in the constraint matrix multiplication.
        :param verbose: If True, then the number of iterations required is printed
        :return: True if network is consistent, otherwise False
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
                            prod += self.algebra.compose(c13, c32)
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


# def load_network(alg_path, json_file, net_ext=".json"):
#     """Loads a network specification from a JSON file. Returns the resulting network."""
#     with open(json_file, "r") as file:
#         net_dict = json.load(file)
#     net_alg = Algebra(alg_path + net_dict["algebra"] + net_ext)
#     nodes = net_dict["nodes"]
#     entities = {}
#     for nkey, nspec in nodes.items():
#         entities[nkey] = class_type_dict[nspec[1]](nspec[1:], nspec[0])
#     ntwk = Network(net_alg, net_dict["name"])
#     for espec in net_dict["edges"]:
#         cons = espec[2]
#         if cons in net_dict["abbreviations"]:
#             constraint = net_dict["abbreviations"][cons]
#         else:
#             constraint = cons
#         ntwk.add_constraint(entities[espec[0]], entities[espec[1]], constraint)
#     return ntwk


# IMPORTANT: The only intended purpose of the class, FourPointNet, is to generate point-based
# representations of interval relations using the function, generate_consistent_networks.
# It has no other intended purpose.

class FourPointNet(Network):
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

    def __ontology_classes(self, start, end):
        """The constraints between the start and end points of a temporal entity
        determine whether it belongs to the class of Point, ProperIntervals, or
        both.  Return a list containing the class names for the input network, net."""
        class_list = []
        constr = self.edges[start, end]['constraint']
        if '=' in constr:
            class_list.append('Point')
        if '<' in constr:
            class_list.append('ProperInterval')
        return class_list

    def domain_and_range(self):
        """Return a tuple, (domain, range), for the interval/point relation
        represented by the input 4-point network."""
        return (self.__ontology_classes(self.start1, self.end1),
                self.__ontology_classes(self.start2, self.end2))


# Map 4-Point network "signatures" to typical relation names.
# This mapping is used in generate_consistent_networks, below.
signature_name_mapping = {
    '<,<,<,<': 'B', '>,>,>,>': 'BI',
    '>,<,>,<': 'D', '<,<,>,>': 'DI',
    '=,<,>,=': 'E', '=,=,=,=': 'PE',
    '>,<,>,=': 'F', '<,<,>,=': 'FI',
    '<,<,=,<': 'M', '>,=,>,>': 'MI',
    '<,<,>,<': 'O', '>,<,>,>': 'OI',
    '=,<,>,<': 'S', '=,<,>,>': 'SI',
    '>,=,>,=': 'PF', '<,<,=,=': 'PFI',
    '=,<,=,<': 'PS', '=,=,>,>': 'PSI',
    '<,<,>,r~': 'RO', '<,<,r~,r~': 'RB',
    '=,<,>,r~': 'RS', '>,<,>,r~': 'ROI',
    '>,r~,>,r~': 'RBI', 'r~,r~,r~,r~': 'R~',
    'l~,<,>,<': 'LO', 'l~,<,>,=': 'LF',
    'l~,<,>,>': 'LOI', 'l~,l~,>,>': 'LBI',
    'l~,<,l~,<': 'LB', 'l~,l~,l~,l~': 'L~'
}


# A 4-point network (generated by FourPoint) only has constraints specified so that the first two points define an
# interval, and same for the second two points. No constraints are specified between the two implied intervals (e.g.,
# no constraint between StartPt1/EndPt1 and StartPt2/EndPt2).  Depending on which point algebra is used there are
# either 3^4 (81) or 4^4 (256) different ways the unassigned constraint pairs can be made.  The function,
# <i>generate_consistent_networks</i> tries all of these possibilities and returns the ones that are consistent.
# Doing this for the linear point algebra ('<', '=', '>') results in 13 consistent networks that correspond to
# Allen's Temporal Algebra of Proper Time Intervals.  Using ('<|=', '=', '>|=") results in 18 consistent networks
# that are a superset of Allen's relations that includes 5 additional relations that integrate points into the
# algebra.  Using ('<|=', '=', '>|=', '~'), where '~' is either the left-incomparable or right-incomparable relation
# of the left- or right-branching time point algebra will result in 24 consistent networks that integrate points into
# a left- or right-branching time interval algebra.

# Viewing the network as a matrix, 'elem13', below, refers to the element in row 1 col 3,
# and so on for 'elem23', etc.  The matrix is 4x4, so if we partition it into four 2x2
# matrices, then the two partitions on the diagonal represent two intervals and the two
# off-diagonal partitions represent how the end points those two intervals relate to
# each other. Also, the off-diagonal 2x2 partitions are converse transposes of each other.
# Oh, and the intervals represented by the diagonal partitions could be intervals,
# proper intervals, or points.


def generate_consistent_networks(point_algebra, lessthan="<", startname="StartPt", endname="EndPt",
                                 verbose=False):
    consistent_nets = dict()
    for elem13 in point_algebra.elements:
        for elem23 in point_algebra.elements:
            for elem14 in point_algebra.elements:
                for elem24 in point_algebra.elements:
                    four_pt_net_name = elem13 + ',' + elem23 + ',' + elem14 + ',' + elem24
                    ptnet = FourPointNet(point_algebra, four_pt_net_name, lessthan, startname, endname)
                    pt1, pt2, pt3, pt4 = ptnet.get_points()
                    rs13 = point_algebra.relset(elem13)
                    rs23 = point_algebra.relset(elem23)
                    rs14 = point_algebra.relset(elem14)
                    rs24 = point_algebra.relset(elem24)
                    ptnet.add_constraint(pt1, pt3, rs13)
                    ptnet.add_constraint(pt2, pt3, rs23)
                    ptnet.add_constraint(pt1, pt4, rs14)
                    ptnet.add_constraint(pt2, pt4, rs24)
                    if ptnet.propagate():
                        elem_key = ",".join([str(rs13), str(rs14), str(rs23), str(rs24)])
                        consistent_nets[signature_name_mapping[elem_key]] = ptnet
                        if verbose:
                            print("==========================")
                            if elem_key in signature_name_mapping:
                                print(signature_name_mapping[elem_key])
                            else:
                                print("UNKNOWN")
                            print(np.array(ptnet.to_list()))
    print(f"\n{len(consistent_nets)} consistent networks")
    return consistent_nets


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
    print("Check algebra composition identity")
    print("-------------------------------------")

    verbosity = False

    for a in alg:
        print(f"\n{a.name}:")
        print(f"Relations: {a.elements}")
        if a.check_composition_identity():
            print("Composition Identity OK")
        else:
            print("Composition Identity Failed")

    print("\n---------------------------")
    print("Check algebra associativity")
    print("---------------------------")

    for a in alg:
        print(f"\n{a.name}:")
        print(f"Relations: {a.elements}")
        if a.is_associative():
            print(f"{a.name} is associative.")
        else:
            print(f"{a.name} is NOT associative.")

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

    # Example in book on constraint processing for temporal reasoning
    # (extended to intervals & points)
    pint_I = TemporalEntity(["Point", "ProperInterval"], "I")
    pint_J = TemporalEntity(["Point", "ProperInterval"], "J")
    pint_K = TemporalEntity(["Point", "ProperInterval"], "K")
    pint_L = TemporalEntity(["Point", "ProperInterval"], "L")
    net2x = Network(alg[1], "Book Example Extended")
    net2x.add_constraint(pint_I, pint_J, "F|FI")
    net2x.add_constraint(pint_I, pint_L, "S|M")
    net2x.add_constraint(pint_L, pint_J, "S|M")
    net2x.add_constraint(pint_K, pint_I, "D|DI")
    net2x.add_constraint(pint_K, pint_J, "D|DI")
    net2x.add_constraint(pint_L, pint_K, "O")
    net2x.summary()
    net2x.propagate(verbose=True)
    net2x.summary()

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

    print("""\nNote on example above:
    According to Wikipedia,
    https://en.wikipedia.org/wiki/Region_connection_calculus#Examples,
    the correct constraints
    between 'road' and 'property1', and
    between 'road' and 'property2' are:
      road property1 EC|PO
      road property2 PO|TPP""")

    # net4.converse().summary()

    print("""    ------------
    END OF TESTS
    ------------""")

    # End of File
