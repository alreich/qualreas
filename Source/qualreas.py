"""
@author: Alfred J. Reich

"""

# BITSETS: https://bitsets.readthedocs.io/en/stable/
from bitsets import bitset, bases
import os
import json
import random
import string
# NETWORKX: https://networkx.github.io/
import networkx as nx
from functools import reduce
from collections import abc, OrderedDict
import numpy as np

__author__ = 'Alfred J. Reich'
__version__ = '0.5.0'


def make_name(name=None, prefix="Network:", size=8):
    """If no name, then return a random name; otherwise return name."""
    if not name:
        chars = string.ascii_letters + string.digits + '!@#$%&*'
        name = prefix + "".join([random.choice(chars) for _ in range(size)])
    return name


def flatten(lst):
    """Flatten a shallow list."""
    return reduce(lambda x, y: x + y, lst)


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

# TODO: Eliminate Entities.  Just use NetworkX node attributes.

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

    def __init__(self, filename=None, alg_dict=None):
        """An algebra is created from a JSON file containing the algebra's
        relation and transitivity table definitions.  An algebra can also
        be instantiated from a dictionary.
        """
        if filename:
            with open(filename, 'r') as f:
                self.algebra_dict = json.load(f)
        else:
            self.algebra_dict = alg_dict

        if "Name" in self.algebra_dict:
            self.name = self.algebra_dict["Name"]
        else:
            self.name = make_name(prefix="Algebra:")

        if "Description" in self.algebra_dict:
            self.description = self.algebra_dict["Description"]
        else:
            self.description = "No description provided."

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

        # Setup the transitivity (or composition) table to be used by Relation Set composition.
        # This code can read both the original transitivity table format and the newer compact
        # transitivity table format, which is now the default.
        self.transitivity_table = dict()
        tabledefs = self.algebra_dict["TransTable"]
        for rel1 in tabledefs:
            self.transitivity_table[rel1] = dict()
            for rel2 in tabledefs[rel1]:
                table_entry = tabledefs[rel1][rel2]
                if type(table_entry) == list:
                    entry = table_entry
                elif type(table_entry) == str:
                    if table_entry == "":
                        entry = []  # because "".split('|') = ['']
                    else:
                        entry = table_entry.split('|')
                else:
                    raise Exception("Bad entry in transitivity table")
                # print(rel1, rel2)
                self.transitivity_table[rel1][rel2] = self.elements_bitset(tuple(entry))

    # TODO: Write a to_dict() method for Algebras

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

    def get_domain_classes(self, relset):
        """Returns the set of domain classes supported by the relations in a relset."""
        return set(flatten(list(map(lambda x: self.rel_domain(x),
                                    list(self.relset(relset))
                                    ))))

    def get_range_classes(self, relset):
        """Returns the set of range classes supported by the relations in a relset."""
        return set(flatten(list(map(lambda x: self.rel_range(x),
                                    list(self.relset(relset))
                                    ))))

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
        count_skipped = 0
        count_ok = 0
        count_failed = 0
        count_total = 0
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
                                count_failed += 1
                                count_total += 1
                                result = False
                            else:
                                if verbose:
                                    print("  Associativity OK")
                                count_ok += 1
                                count_total += 1
                        else:
                            if verbose:
                                print(
                                    f"  Skipping check due to b x c: {self.rel_range(_b)}::{self.rel_domain(_c)}")
                            count_skipped += 1
                            count_total += 1
                    else:
                        if verbose:
                            print(f"  Skipping check due to a x b: {self.rel_range(_a)}::{self.rel_domain(_b)}")
                        count_skipped += 1
                        count_total += 1
        print(f"TEST SUMMARY: {count_ok} OK, {count_skipped} Skipped, {count_failed} Failed ({count_total} Total)")
        numrels = len(rels)
        total_tests = numrels * numrels * numrels
        if count_total != total_tests:
            print(f"Test counts do not add up; Total should be {total_tests}")
        return result

    def print_compact_transitivity_table(self):
        """This function's only purpose was to convert the original transitivity table format
        to the new compact representation.  It's preserved for posterity here in case it's ever
        needed again."""
        num_elements = len(self.elements)
        print("    \"TransTable\": {")
        outer_count = num_elements  # Used to avoid printing last comma in outer list
        for rel1 in self.transitivity_table:
            outer_count -= 1
            print(f"        \"{rel1}\": {{")
            inner_count = num_elements  # Used to avoid printing last comma in inner list
            for rel2 in self.transitivity_table[rel1]:
                inner_count -= 1
                if inner_count > 0:
                    print(f"            \"{rel2}\": \"{self.transitivity_table[rel1][rel2]}\",")
                else:
                    print(f"            \"{rel2}\": \"{self.transitivity_table[rel1][rel2]}\"")
            if outer_count > 0:
                print(f"        }},")
            else:
                print(f"        }}")
        print("    }")

    def equivalent_algebra(self, other_alg):
        """Two algebras are equivalent if they have the same relations and transitivity tables."""
        rels_equiv = (self.algebra_dict['Relations'] == other_alg.algebra_dict['Relations'])
        tbls_equiv = (self.algebra_dict['TransTable'] == other_alg.algebra_dict['TransTable'])
        return rels_equiv and tbls_equiv


# Used to break out of Network propagation if it is found to be inconsistent
class InconsistentNetwork(Exception):
    pass


class Network(nx.DiGraph):

    def __init__(self, algebra=None, name=None,
                 algebra_path=None, json_file_name=None, network_dict=None,
                 json_ext=".json"):

        # Create the network in dictionary form (net_dict)
        if json_file_name:
            with open(json_file_name, "r") as json_file:
                net_dict = json.load(json_file)
            json_file.close()
        # ...or use the input dictionary,
        elif network_dict:
            net_dict = network_dict
        # ...or start from scratch (assumes an Algebra was input, though).
        else:
            net_dict = {"name": make_name(name),
                        "description": "undefined",
                        "nodes": [],
                        "edges": []}

        # If an algebra was input, use it...
        if algebra:
            self.algebra = algebra
        # ...otherwise read the required algebra from a JSON file.
        else:
            self.algebra = Algebra(os.path.join(algebra_path, net_dict["algebra"]) + json_ext)

        # TODO: Make name & description attributes of the DiGraph
        if "name" in net_dict:
            name = net_dict["name"]
        if "description" in net_dict:
            self.description = net_dict["description"]

        # Create 'nodes' as a dictionary where key:value = node_name:node_classes
        # TODO: Eliminate this dictionary and incorporate it in 'entities' below
        node_list = net_dict["nodes"]
        nodes = dict()
        for nd in node_list:
            nodes[nd[0]] = nd[1]

        # Create 'entities' as a dictionary where key:value = node_name:Entity(classes, node_name)
        entities = dict()
        for node_name, node_classes in nodes.items():
            entities[node_name] = class_type_dict[node_classes[0]](node_classes, node_name)

        # Initialize the superclass
        super().__init__(name=make_name(name))

        # Add the constraint to the network as an attribute on an edge
        for edge_spec in net_dict["edges"]:
            if len(edge_spec) == 3:
                cons = edge_spec[2]
            else:
                cons = self.algebra.elements
            if ("abbreviations" in net_dict) and (cons in net_dict["abbreviations"]):
                constraint = net_dict["abbreviations"][cons]
            else:
                constraint = cons
            self.add_constraint(entities[edge_spec[0]], entities[edge_spec[1]], constraint)

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

    def set_constraint(self, src, tgt, relset):
        """Assuming that an edge exists between src & tgt, this function destructively changes
         whatever constraint was between them to be relset"""
        self.edges[src, tgt]['constraint'] = relset
        # Don't bother looking at the converse for equality relations
        if src != tgt:
            self.edges[tgt, src]['constraint'] = self.algebra.converse(relset)

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

    def get_entity_by_name(self, name):
        """Return the node (entity) with the input name. If more than one have the same name,
        then the first one found is returned.  So, try to give entities different names."""
        result = None
        for node in self.nodes:
            if node.name == name:
                result = node
                break
        return result

    def get_entities_by_name(self, name_list):
        """Return an iterator over entities with the names in 'name_list', in the order
        that they appear in the list."""
        return map(lambda name: self.get_entity_by_name(name), name_list)

    def get_edge_by_names(self, source_name, target_name, return_names=True):
        """Returns the Source Name/Node, Target Name/Node, and Constraint of the
        Edge corresponding to the input Source/Target Names."""
        source_node = self.get_entity_by_name(source_name)
        target_node = self.get_entity_by_name(target_name)
        con = str(self.edges[source_node, target_node]['constraint'])
        if return_names:
            return source_name, target_name, con
        else:
            return source_node, target_node, con

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
            # Update the Entity/Node classes to reflect changes due to constraint propagation
            for nd in self.nodes():
                # Only consider domains since the edges below are from the node to itself
                nd.classes = list(self.algebra.get_domain_classes(self.edges[nd, nd]['constraint']))
            if verbose:
                print(f"Number of iterations: {loop_count}")
            return True
        except InconsistentNetwork:
            if verbose:
                print(f"Propagation suspended; the network is inconsistent.")
            return False

    def summary(self, show_all=True):
        """Prints a summary of the network and its nodes/classes, edges, & constraints.
        By default, all edges are printed.  That is, every edge and its converse are
        shown, e.g., A-->B and B-->A, which is a bit redundant.  To just show one of
        the edges, set show_all to False."""
        print(f"\n{self.name}: {len(self.nodes)} nodes, {len(self.edges)} edges")
        print(f"  Algebra: {self.algebra.name}")
        done = []
        for head in self.nodes:
            print(f"  {head.name}:{head.classes}")
            for tail in self.neighbors(head):
                if (tail not in done) or show_all:
                    print(f"    => {tail.name}: {str(self.edges[head, tail]['constraint'])}")
            done.append(head)

    def to_dict(self):
        """Return a dictionary representation of the network."""
        net_dict = {
            "name": self.name,
            "algebra": self.algebra.name,
            "description": self.description,
            "nodes": [],
            "edges": []
        }
        # Create an entry for each node in the dictionary, including the classes
        # that each node is in, based on the domain of the equality relations on
        # the edge from each node to itself.
        for node in self.nodes:
            self_constraints = self.get_edge_by_names(node.name, node.name)[2]
            classes = list(self.algebra.get_domain_classes(self_constraints))
            net_dict["nodes"].append([node.name, classes])
        reverse_edges = set()  # Keep track of reverse edges and don't output them
        for head in self.nodes:
            for tail in self.neighbors(head):
                if head.name != tail.name:  # Don't output an edge from a node to itself
                    if not ((head.name, tail.name) in reverse_edges):
                        net_dict["edges"].append(list(self.get_edge_by_names(head.name, tail.name)))
                        reverse_edges.add((tail.name, head.name))  # Remember the reverse of this edge
        return net_dict

    def mostly_copy(self):
        """Returns a mostly deep copy of the network, except for the Algebra, which is shared."""
        return Network(algebra=self.algebra, network_dict=self.to_dict())

    def expand(self):
        """Expands the first edge it comes across with multiple relations into
        multiple network copies with single relations on the same edge."""
        expansion = []
        for src, tgt in self.edges:
            edge_constraint = self.edges[src, tgt]['constraint']
            if len(edge_constraint) > 1:
                for rel in edge_constraint:
                    net_copy = self.mostly_copy()
                    src_node, tgt_node, _ = net_copy.get_edge_by_names(src.name, tgt.name, return_names=False)
                    net_copy.set_constraint(src_node, tgt_node, net_copy.algebra.relset(rel))
                    expansion = expansion + [net_copy]
                break
        return expansion

    def expand_all(self):
        def exp_aux(in_work, result):
            if len(in_work) == 0:
                return result
            else:
                next_net = in_work.pop()
                if next_net.has_only_singleton_constraints():
                    return exp_aux(in_work, result + [next_net])
                else:
                    return exp_aux(next_net.expand() + in_work, result)
        return exp_aux([self], [])

    def has_only_singleton_constraints(self):
        """Returns True if all constraints consist of single relations."""
        answer = True
        for src, tgt in self.edges:
            edge_constraint = self.edges[src, tgt]['constraint']
            if len(edge_constraint) > 1:
                answer = False
                break
        return answer

    def all_realizations(self):
        return [net for net in self.expand_all() if net.propagate()]

    def get_submatrix_constraints(self, rows, cols, entity_name_list):
        entities = list(self.get_entities_by_name(entity_name_list))
        result = []
        for row in rows:
            for col in cols:
                result.append(str(self.edges[entities[row], entities[col]]['constraint']))
        return result

    def get_2x2_partition_constraints(self, startrow, startcol, name_list):
        result = self.get_submatrix_constraints([startrow, startrow + 1],
                                                [startcol, startcol + 1], name_list)
        return ','.join(result)


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
        s1 = startname + "1"
        e1 = endname + "1"
        self.start1 = TemporalEntity(["Point"], name=s1)
        self.end1 = TemporalEntity(["Point"], name=e1)
        # Start & End Points of Interval 2
        s2 = startname + "2"
        e2 = endname + "2"
        self.start2 = TemporalEntity(["Point"], name=s2)
        self.end2 = TemporalEntity(["Point"], name=e2)
        self.name_list = [s1, e1, s2, e2]
        super().__init__(algebra, name)
        self.add_constraint(self.start1, self.end1, self.lessthan, verbose=False)
        self.add_constraint(self.start2, self.end2, self.lessthan, verbose=False)

    def get_points(self):
        return [self.start1, self.end1, self.start2, self.end2]

    # def get_point_names(self):
    #     return map(lambda pt: pt.name, self.get_points())

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

# This is the reverse dictionary of the 'signature_name_mapping' dictionary, above.
name_signature_mapping = {val: key.split(',') for key, val in signature_name_mapping.items()}


# The dictionary below includes Allen's Interval Algebra relations plus the additional
# relations defined in [Reich 1994] for Points and Left/Right-Branching Time algebras.
relation_long_names = {
    "B": "Before",
    "BI": "After",
    "D": "During",
    "DI": "Contains",
    "E": "Equals",
    "F": "Finishes",
    "FI": "Finished-by",
    "LB": "Left-Before",
    "LBI": "Left-After",
    "LF": "Left-Finishes",
    "LO": "Left-Overlaps",
    "LOI": "Left-Overlapped-By",
    "L~": "Left-Incomparable",
    "M": "Meets",
    "MI": "Met-By",
    "O":  "Overlaps",
    "OI": "Overlapped-By",
    "PE": "Point-Equals",
    "PF": "Point-Finishes",
    "PFI": "Point-Finished-By",
    "PS": "Point-Starts",
    "PSI": "Point-Started-By",
    "RB": "Right-Before",
    "RBI": "Right-After",
    "RO": "Right-Overlaps",
    "ROI": "Right-Overlapped-By",
    "RS": "Right-Starts",
    "R~": "Right-Incomparable",
    "S": "Starts",
    "SI": "Started-By"
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
                    # four_pt_net_name = elem13 + ',' + elem23 + ',' + elem14 + ',' + elem24
                    four_pt_net_name = elem13 + ',' + elem14 + ',' + elem23 + ',' + elem24
                    ptnet = FourPointNet(point_algebra, four_pt_net_name, lessthan, startname, endname)
                    pt1, pt2, pt3, pt4 = ptnet.get_points()
                    rs13 = point_algebra.relset(elem13)
                    rs14 = point_algebra.relset(elem14)
                    rs23 = point_algebra.relset(elem23)
                    rs24 = point_algebra.relset(elem24)
                    ptnet.add_constraint(pt1, pt3, rs13)
                    ptnet.add_constraint(pt1, pt4, rs14)
                    ptnet.add_constraint(pt2, pt3, rs23)
                    ptnet.add_constraint(pt2, pt4, rs24)
                    if ptnet.propagate():
                        elem_key = ",".join([str(rs13), str(rs14), str(rs23), str(rs24)])
                        consistent_nets[signature_name_mapping[elem_key]] = ptnet
                        if verbose:
                            print("==========================")
                            if elem_key in signature_name_mapping:
                                print(elem_key)
                                print(signature_name_mapping[elem_key])
                            else:
                                print("UNKNOWN")
                            print(ptnet.domain_and_range())
                            print(np.array(ptnet.to_list()))
    print(f"\n{len(consistent_nets)} consistent networks")
    return consistent_nets


class SixPointNet(Network):

    def __init__(self, algebra, lessthanstr, relname1, relname2,
                 startname="StartPt", endname="EndPt"):
        self.algebra = algebra
        self.lessthan = algebra.relset(lessthanstr)

        # Start & End Points of Interval 1
        s1 = startname + "1"
        e1 = endname + "1"
        self.start1 = TemporalEntity(["Point"], name=s1)
        self.end1 = TemporalEntity(["Point"], name=e1)

        # Start & End Points of Interval 2
        s2 = startname + "2"
        e2 = endname + "2"
        self.start2 = TemporalEntity(["Point"], name=s2)
        self.end2 = TemporalEntity(["Point"], name=e2)

        # Start & End Points of Interval 3
        s3 = startname + "3"
        e3 = endname + "3"
        self.start3 = TemporalEntity(["Point"], name=s3)
        self.end3 = TemporalEntity(["Point"], name=e3)

        self.name_list = [s1, e1, s2, e2, s3, e3]

        super().__init__(algebra, relname1 + ";" + relname2)
        self.add_constraint(self.start1, self.end1, self.lessthan, verbose=False)
        self.add_constraint(self.start2, self.end2, self.lessthan, verbose=False)
        self.add_constraint(self.start3, self.end3, self.lessthan, verbose=False)

        c13, c14, c23, c24 = name_signature_mapping[relname1]

        self.add_constraint(self.start1, self.start2, c13, verbose=False)
        self.add_constraint(self.start1, self.end2, c14, verbose=False)
        self.add_constraint(self.end1, self.start2, c23, verbose=False)
        self.add_constraint(self.end1, self.end2, c24, verbose=False)

        c35, c36, c45, c46 = name_signature_mapping[relname2]

        self.add_constraint(self.start2, self.start3, c35, verbose=False)
        self.add_constraint(self.start2, self.end3, c36, verbose=False)
        self.add_constraint(self.end2, self.start3, c45, verbose=False)
        self.add_constraint(self.end2, self.end3, c46, verbose=False)

        c = algebra.elements

        self.add_constraint(self.start1, self.start3, c, verbose=False)
        self.add_constraint(self.start1, self.end3, c, verbose=False)
        self.add_constraint(self.end1, self.start3, c, verbose=False)
        self.add_constraint(self.end1, self.end3, c, verbose=False)

    def get_points(self):
        return [self.start1, self.end1, self.start2, self.end2, self.start3, self.end3]

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


def derive_composition(point_algebra, eq_rel, rel1, rel2):
    pt_net = SixPointNet(point_algebra, eq_rel, rel1, rel2)
    pt_name_list = pt_net.name_list
    pt_net.propagate()
    # print(f"Derive Comp for: {np.array(pt_net.to_list())}")  # DEBUG
    pt_net_realz = pt_net.all_realizations()
    comps = set()
    for realz in pt_net_realz:
        # diag = realz.get_2x2_partition_constraints(0, 0, pt_name_list)
        comp = realz.get_2x2_partition_constraints(0, 4, pt_name_list)
        comps.add(signature_name_mapping[comp])
    comps_list = list(comps)
    comps_list.sort()
    return '|'.join(comps_list)


def derive_composition_table(point_algebra, less_than_rel, relations_list):
    trans_dict = dict()
    for r1 in relations_list:
        trans_dict[r1] = dict()
        for r2 in relations_list:
            trans_dict[r1][r2] = derive_composition(point_algebra, less_than_rel, r1, r2)
    return trans_dict


# def is_transitive(rel_name, pt_alg, less_than_rel):
#     return rel_name == derive_composition(pt_alg, less_than_rel, rel_name, rel_name)


def is_transitive(rel_name, transitivity_table):
    return rel_name == transitivity_table[rel_name][rel_name]


def is_symmetric(rel_name, consistent_nets):
    four_pt_net = consistent_nets[rel_name]
    part02 = four_pt_net.get_2x2_partition_constraints(0, 2, four_pt_net.name_list)
    part20 = four_pt_net.get_2x2_partition_constraints(2, 0, four_pt_net.name_list)
    return part02 == part20


def is_reflexive(rel_name, consistent_nets):
    four_pt_net = consistent_nets[rel_name]
    part00 = four_pt_net.get_2x2_partition_constraints(0, 0, four_pt_net.name_list)
    part02 = four_pt_net.get_2x2_partition_constraints(0, 2, four_pt_net.name_list)
    return part00 == part02


def derive_relation_info(rel_name, pt_net, consistent_nets, transitivity_table):
    info = dict()
    dom_rng = pt_net.domain_and_range()
    part_inv = pt_net.get_2x2_partition_constraints(2, 0, pt_net.name_list)
    rel_inv_name = signature_name_mapping[part_inv]
    info["Name"] = relation_long_names[rel_name]
    info["Converse"] = rel_inv_name
    info["Domain"] = dom_rng[0]
    info["Range"] = dom_rng[1]
    info["Reflexive"] = is_reflexive(rel_name, consistent_nets)
    info["Symmetric"] = is_symmetric(rel_name, consistent_nets)
    info["Transitive"] = is_transitive(rel_name, transitivity_table)
    return info


def derive_relation_dict(consistent_networks, transitivity_table):
    rel_dict = OrderedDict()
    alg_rels_list = list(consistent_networks.keys())
    alg_rels_list.sort()
    for rel_name in alg_rels_list:
        rel_pt_net = consistent_networks[rel_name]
        rel_dict[rel_name] = derive_relation_info(rel_name, rel_pt_net,
                                                  consistent_networks, transitivity_table)
    return dict(rel_dict)


def derive_algebra(base_alg, less_than_rel, name=None, description=None):
    base_nets = generate_consistent_networks(base_alg, lessthan=less_than_rel)
    alg_rels_list = list(base_nets.keys())
    alg_rels_list.sort()
    comp_dict = derive_composition_table(base_alg, less_than_rel, alg_rels_list)
    rels_dict = derive_relation_dict(base_nets, comp_dict)
    alg_dict = dict()
    alg_dict["Name"] = name
    alg_dict["Description"] = description
    alg_dict["Relations"] = rels_dict
    alg_dict["TransTable"] = comp_dict
    return alg_dict


def algebra_to_json_file(algebra, json_path):
    with open(json_path, "w") as out:
        json.dump(algebra, out, indent=4, separators=(',', ':'))


def print_point_algebra_composition_table(pt_alg):
    print(f"{pt_alg.name}")
    print(f"Elements: {', '.join(pt_alg.elements)}")
    print(f"{'='*30}")
    print(f" rel1 ; rel2 = composition")
    print(f"{'='*30}")
    for rel1 in pt_alg.transitivity_table:
        for rel2 in pt_alg.transitivity_table[rel1]:
            comp = pt_alg.transitivity_table[rel1][rel2]
            print(f" {rel1:>3}    {rel2:>3}      {comp}")
        print(f"{'-'*30}")


if __name__ == '__main__':

    print("\n=======================================================================")

    path = os.path.join(os.getenv('PYPROJ'), 'qualreas')

    alg = [Algebra(os.path.join(path, "Algebras/Linear_Interval_Algebra.json")),
           Algebra(os.path.join(path, "Algebras/Extended_Linear_Interval_Algebra.json")),
           Algebra(os.path.join(path, "Algebras/Left_Branching_Interval_Algebra.json")),
           Algebra(os.path.join(path, "Algebras/Right_Branching_Interval_Algebra.json")),
           Algebra(os.path.join(path, "Algebras/RCC8_Algebra.json")),
           Algebra(os.path.join(path, "Algebras/Linear_Point_Algebra.json")),
           Algebra(os.path.join(path, "Algebras/Right_Branching_Point_Algebra.json")),
           Algebra(os.path.join(path, "Algebras/Left_Branching_Point_Algebra.json"))
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

    # Algebra(os.path.join(path, "Algebras/Linear_Interval_Algebra.json"

    # rcc8x = Network(algebra_path=path+"/Algebras/",
    #                 json_file_name=path+"/Networks/rcc8_example.json")

    # print(f"Path = {path}")
    # alg_path = os.path.join(path, "Algebras")
    # print(f"Alg path = {alg_path}")
    # json_fname = os.path.join(path, "Networks/rcc8_example.json")
    # print(f"JSON path = {json_fname}")
    rcc8x = Network(algebra_path=os.path.join(path, "Algebras"),
                    json_file_name=os.path.join(path, "Networks/rcc8_example.json"))
    rcc8x.summary()
    rcc8x.propagate()
    rcc8x.summary()

    # # alg4 = Algebra(os.path.join(path, "Algebras/RCC8_Algebra.json"))
    # alg4 = alg[4]
    #
    # house1 = SpatialEntity(["Region"], "house1")
    # house2 = SpatialEntity(["Region"], "house2")
    # property1 = SpatialEntity(["Region"], "property1")
    # property2 = SpatialEntity(["Region"], "property2")
    # road = SpatialEntity(["Region"], "road")
    #
    # net4 = Network(alg4, "Wikipedia RCC8 Example")
    #
    # net4.add_constraint(house1, house2, "DC", verbosity)
    # net4.add_constraint(house1, property1, "TPP|NTPP", verbosity)
    # net4.add_constraint(house1, property2, "DC|EC", verbosity)
    # net4.add_constraint(house1, road, "EC", verbosity)
    # net4.add_constraint(house2, property1, "DC|EC", verbosity)
    # net4.add_constraint(house2, property2, "NTPP", verbosity)
    # net4.add_constraint(house2, road, "EC", verbosity)
    # net4.add_constraint(property1, property2, "DC|EC", verbosity)
    #
    # net4.summary()
    # net4.propagate()
    # net4.summary()

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
