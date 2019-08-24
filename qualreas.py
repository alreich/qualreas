"""
Created on 3 Jan 2011

@author: Alfred J. Reich, Ph.D.

"""

import json
import uuid


__author__ = 'Alfred J. Reich'
__version__ = '0.1.0'

# TODO: Use "from __future__ import print_function, division"


class Relation(object):
    """A Relation object represents a relationship between elements of
    one set (domain) and another set (range).  The Relation object
    stores information about the relationship, such as its inverse,
    its names (normal & abbreviated), whether it is reflexive,
    symmetric, etc., and so on.  It is important that Relation objects
    be immutable.  All of their properties are carefully defined by
    the Relation Algebra that they belong to.  Relations are defined
    as part of an algebra in a JSON file.

    """

    def __init__(self, relation_name, abbreviated_name, inverse_name, relation_domain,
                 relation_range, is_reflexive=False, is_symmetric=False, is_transitive=False):
        # Once set, none of these attributes should be changed.  For this reason they are hidden
        # and only accessed (read-only) via the property decorator.
        self.__fullname = relation_name
        self.__abbrev_name = abbreviated_name
        self.__inv_name = inverse_name
        self.__inv = None  # Will be automatically set below
        self.__domain = relation_domain
        self.__range = relation_range
        self.__is_reflexive = is_reflexive
        self.__is_symmetric = is_symmetric
        self.__is_transitive = is_transitive
        self.__is_equality = is_reflexive & is_symmetric & is_transitive

    # This method violates the convention that __repr__ return a string that could be used to
    # recreate the Relation object.  One reason for this is for readability in sets of relations.
    # Another reason is that there should only be one copy of any Relation.  Once created, all
    # references to the Relation should (and hopefully do) refer to that copy.
    def __repr__(self):
        return "{}".format(self.__abbrev_name)

    def __lt__(self, other):
        if isinstance(other, Relation):
            return self.__abbrev_name < other.__abbrev_name
        else:
            return False

    @property
    def inverse_name(self):
        return self.__inv_name

    @property
    def inverse(self):
        return self.__inv

    # This function should never be called by the user.  It is called automatically during
    # the loading and setup of an algebra.
    def set_inverse(self, inv_relation):
        self.__inv = inv_relation

    @property
    def short_name(self):
        return self.__abbrev_name

    @property
    def full_name(self):
        return self.__fullname

    @property
    def is_reflexive(self):
        return self.__is_reflexive

    @property
    def is_symmetric(self):
        return self.__is_symmetric

    @property
    def is_transitive(self):
        return self.__is_transitive

    @property
    def is_equality(self):
        return self.__is_equality

    @property
    def domain(self):
        return self.__domain

    @property
    def range(self):
        return self.__range


class RelationSet(object):
    """A RelationSet is a set of Relation instances.  RelationSets are
    the algebraic elements that make up an algebra.  A RelationSet
    represents the disjunction of the Relations it contains.  So, if R
    = {A, B, C}, then X R Y if and only if (X A Y) or (X B Y) or (X C
    Y).  The multiplication table (transitivity table) for singleton
    RelationSets is defined by an algebra in a JSON file.  e.g., {B} *
    {D} = {B,D,M,O,S}

    """
    def __init__(self, elements, algebra=None):
        # TODO: If algebra is not None, then check that 'elements' are in its relations.
        self.__elements = frozenset(sorted(elements))
        self.__algebra = algebra

    def __contains__(self, element):
        return self.__elements.__contains__(element)

    def __len__(self):
        return self.__elements.__len__()

    def __iter__(self):
        return self.__elements.__iter__()

    def __eq__(self, other):
        return (self.__elements == other.elements) and (self.__algebra == other.algebra)

    def __ne__(self, other):
        return self.__elements != other.elements

    def __repr__(self):
        return "<RelationSet" + self.__elements.__repr__()[9:] + ">"

    def __add__(self, relset):
        """Addition for relation sets is equivalent to set intersection."""
        if self.algebra == relset.algebra:
            result = self.elements & relset.elements
            return RelationSet(result, relset.algebra)
        else:
            raise Exception("Algebra's must agree")

    def union(self, relset):
        if self.algebra == relset.algebra:
            result = self.elements | relset.elements
            return RelationSet(result, relset.algebra)
        else:
            raise Exception("Algebras must agree")

    def __mul__(self, relset):
        """Multiplication is done, element-by-element, on the cross-product
        of the two sets using the algebra's transitivity table, and
        then reducing those results to a single relation set using set
        union.

        """
        if self.algebra == relset.algebra:
            result = RelationSet([], self.algebra)
            tbl = relset.algebra.trans_table
            for rel1 in self:
                for rel2 in relset:
                    result = result.union(tbl[rel1.short_name][rel2.short_name])
            return RelationSet(result, self.algebra)
        else:
            raise Exception("Mismatched algebras")

    def sorted_list(self):
        """Sort the elements of the RelationSet by their short_name property.
        :return: Sorted list of Relations

        """
        return sorted(self, key=lambda rel: rel.short_name)

    @property
    def elements(self):
        return self.__elements

    @property
    def algebra(self):
        return self.__algebra

    @property
    def inverse(self):
        return RelationSet([rel.inverse for rel in self.__elements], self.algebra)

    @property
    def names(self):
        return sorted([rel.short_name for rel in self.__elements])

    @property
    def fullnames(self):
        return sorted([rel.full_name for rel in self.__elements])


class Algebra(object):

    def __init__(self, filename):
        """An algebra is created from a JSON file containing the algebra's
        relation and transitivity table definitions.

        """

        with open(filename, 'r') as f:
            _alg = json.load(f)
        self.__name = _alg["Name"]
        self.__description = _alg["Description"]
        self.__type = _alg["Type"]
        self.__relation_dict = dict()  # Initialized below
        self.__trans_table = dict()  # Initialized below

        # Create each relation and setup its properties
        # for relname, reldict in _alg["Relations"].iteritems():
        for (relname, reldict) in _alg["Relations"].items():
            self.__relation_dict[relname] = Relation(reldict["Name"], relname, reldict["Inverse"],
                                                     frozenset(reldict["Domain"]), frozenset(reldict["Range"]),
                                                     reldict["Reflexive"], reldict["Symmetric"],
                                                     reldict["Transitive"])

        # For each Relation, replace the short_name of its inverse with the actual inverse Relation object itself
        for rel in self.__relation_dict.values():
            rel.set_inverse(self.__relation_dict[rel.inverse_name])

        # The algebraic identity of an algebra is the RelationSet containing all relations
        self.__identity = RelationSet(self.__relation_dict.values(), self)

        # The equality relations of the algebra
        self.__equality_relations = [rel for rel in self.__identity if rel.is_equality]

        # Populate a dictionary that allows equality relations to be looked-up based on their domain/range.
        self.equality_relation_dict = dict()
        for eqrel in self.__equality_relations:
            dom = list(eqrel.domain)[0]  # Get the single item out of the eqrel's domain set.
            self.equality_relation_dict[dom] = eqrel

        # Setup the transitivity table used by RelationSet multiplication
        tabledefs = _alg["TransTable"]
        for rel1 in tabledefs:
            self.__trans_table[rel1] = dict()
            for rel2 in tabledefs[rel1]:
                self.__trans_table[rel1][rel2] = \
                    RelationSet([self.__relation_dict[relname] for relname in tabledefs[rel1][rel2]], self)

    @property
    def identity_relset(self):
        """Returns the algebra's identity element for addition (i.e., the set
        of all elements in the algebra)

        """
        return self.__identity

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def type(self):
        return self.__type

    @property
    def relations(self):
        """A convenience function for looking up and returning a single
        relation (e.g., alg.relations['B']).  Without any arguments
        this function will return the relation lookup dictionary for
        the algebra.

        """
        return self.__relation_dict

    @property
    def equality_relations(self):
        return self.__equality_relations

    def relset(self, relnames):
        """A convenience function for creating relation sets from an algebra.

        """
        return RelationSet([self.__relation_dict[relname] for relname in relnames], self)

    @property
    def trans_table(self):
        return self.__trans_table

    def check_multiplication_identity(self, verbose=False):
        """Check the validity of the multiplicative identity for every
        combination of singleton relset.  :param verbose: Print out
        the details of each test :return: True or False

        """
        count = 0
        result = True
        rels = self.relations
        for r in rels.values():
            for s in rels.values():
                count += 1
                r_rs = RelationSet([r], self)
                s_rs = RelationSet([s], self)
                prod1 = r_rs * s_rs
                prod2 = (s_rs.inverse * r_rs.inverse).inverse
                if prod1 != prod2:
                    if verbose:
                        print("FAIL:")
                        print("      r    = {}".format(r_rs))
                        print("      s    = {}".format(s_rs))
                        print("( r *  s)  = {}".format(prod1))
                        print("(si * ri)i = {}".format(prod2))
                        print("{} != {}".format(prod1, prod2))
                    result = False
        if verbose:
            print("\n{} -- Multiplication Identity Check:".format(self.name))
        if result:
            if verbose:
                print("PASSED . {} products tested.".format(count))
        else:
            if verbose:
                print("FAILED. See FAILURE output above.")
        return result

    def print_info(self):
        mapping = {frozenset([u'ProperInterval', u'Point']): "Int",
                   frozenset([u'Point']): "Pt",
                   frozenset([u'ProperInterval']): "PInt",
                   frozenset([u'Region']): "Region"
                   }
        print("  Algebra Name: {}".format(self.name))
        print("   Description: {}".format(self.description))
        print("          Type: {}".format(self.type))
        print(" Equality Rels: {}".format(self.equality_relations))
        print("     Relations:")
        sorted_rels = sorted(self.relations.values(), key=lambda rel: rel.short_name)
        print("{:>25s} {:>25s} {:>10s} {:>10s} {:>10s} {:>7s} {:>7s}".format("NAME (ABBREV)", "INVERSE (ABBREV)",
                                                                             "REFLEXIVE", "SYMMETRIC", "TRANSITIVE",
                                                                             "DOMAIN", "RANGE"))
        # TODO: Vary spacing between columns based on max word lengths
        for r in sorted_rels:
            print("{:>19s} ({:>3s}) {:>19s} ({:>3s}) {:>8s} {:>10s} {:>10s} {:>8s} {:>7s}".format(r.full_name,
                                                                                                  r.short_name,
                                                                                                  r.inverse.full_name,
                                                                                                  r.inverse.short_name,
                                                                                                  str(r.is_reflexive),
                                                                                                  str(r.is_symmetric),
                                                                                                  str(r.is_transitive),
                                                                                                  mapping[r.domain],
                                                                                                  mapping[r.range]))

    def is_associative(self, verbose=False):
        result = True
        countskipped = 0
        countok = 0
        countfailed = 0
        counttotal = 0
        rels = self.relations
        for _a in rels.values():
            for _b in rels.values():
                for _c in rels.values():
                    if verbose:
                        print("{} x {} x {} :".format(_a, _b, _c))
                    if (set(_a.range) & set(_b.domain)) & (set(_b.range) & set(_c.domain)):
                        a_rs = RelationSet([_a], self)
                        b_rs = RelationSet([_b], self)
                        c_rs = RelationSet([_c], self)
                        prod_ab = a_rs * b_rs
                        prod_bc = b_rs * c_rs
                        prod_ab_c = prod_ab * c_rs
                        prod_a_bc = a_rs * prod_bc
                        if not (prod_ab_c == prod_a_bc):
                            if verbose:
                                print("  Associativity fails for a = {}, b = {}, c = {}".format(a_rs, b_rs, c_rs))
                                print("    associativity check: {}::{} {}::{}".format(_a.range, _b.domain,
                                                                                      _b.range, _c.domain))
                                print("    (a * b) * c = {}".format(prod_ab_c))
                                print("    a * (b * c) = {}".format(prod_a_bc))
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
                            print("  Skipping associativity check: {}::{} {}::{}".format(
                                _a.range, _b.domain, _b.range, _c.domain))
                        countskipped += 1
                        counttotal += 1
        if verbose:
            print("\nTEST SUMMARY: {} OK, {} Skipped, {} Failed ({} Total)".format(
                countok, countskipped, countfailed, counttotal))
        numrels = len(rels)
        totaltests = numrels * numrels * numrels
        if (counttotal != totaltests) and verbose:
            print("Test counts do not add up; Total should be {}".format(totaltests))
        return result


class Network(object):
    def __init__(self, algebra, network_name=None):
        self.__algebra = algebra
        self.__constraints = dict()
        self.__entities = set([])
        if network_name:
            self.__name = network_name
        else:
            self.__name = uuid.uuid4()

    def __len__(self):
        return len(self.__entities)

    @property
    def name(self):
        return str(self.__name)

    def __repr__(self):
        return "<Network: {}, {} entities>".format(self.name, len(self.__entities))

    def __add_constraint(self, e1, e2, rs):
        """
        Add a constraint, rs (RelationSet), between two entities (e1 & e2).
        """
        if e1 not in self.__constraints:
            self.__constraints[e1] = {e2: rs}
        else:
            if e2 not in self.__constraints[e1]:
                self.__constraints[e1][e2] = rs
            else:
                self.__constraints[e1][e2].union(rs)

    def __set_unconstrained_values(self):
        ident = self.__algebra.identity_relset
        for ent1 in self.__entities:
            for ent2 in self.__entities:
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

    def constraint(self, entity1, entity2, rels=None):
        """Assert that entity1 relates to entity2 in one of the ways
        contained in the set of relations, rels.  For example: (e1
        [before, overlaps, meets] e2) iff (e1 before e2) OR (e1
        overlaps e2) OR (e1 meets e2).

        """

        # Remember Entities:
        self.__entities.add(entity1)
        self.__entities.add(entity2)

        if rels:
            relset = RelationSet(rels, self.__algebra)
        else:
            relset = self.__algebra.identity_relset

        self.__add_constraint(entity1, entity2, relset)
        self.__add_constraint(entity2, entity1, relset.inverse)

        equality1 = [self.__algebra.equality_relation_dict[t] for t in entity1.gettype()]
        equality2 = [self.__algebra.equality_relation_dict[t] for t in entity2.gettype()]

        self.__add_constraint(entity1, entity1, RelationSet(equality1, self.__algebra))
        self.__add_constraint(entity2, entity2, RelationSet(equality2, self.__algebra))

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

    def print_constraints(self):
        print("\n{}\nConstraints: (Source, Target, RelationSet)".format(self))
        for x in self.__constraints:
            for y in self.__constraints[x]:
                rels = self.__constraints[x][y]
                print("  {}, {}, {}".format(x.name, y.name, sorted(list(rels))))


class TemporalObject(object):

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
            return "<TemporalObject {} {}>".format(self.__name, self.__type)
        else:
            return "<TemporalObject {}>".format(self.__type)


class SpatialObject(object):

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
            return "<SpatialObject {} {}>".format(self.__name, self.__type)
        else:
            return "<SpatialObject {}>".format(self.__type)


if __name__ == '__main__':

    import os

    path = os.path.join(os.getenv('PYPROJ'), 'qualreas')

    alg = [Algebra(os.path.join(path, "IntervalAlgebra.json")),
           Algebra(os.path.join(path, "IntervalAndPointAlgebra.json")),
           Algebra(os.path.join(path, "LeftBranchingIntervalAndPointAlgebra.json")),
           Algebra(os.path.join(path, "RightBranchingIntervalAndPointAlgebra.json")),
           Algebra(os.path.join(path, "rcc8Algebra.json")),
           Algebra(os.path.join(path, "linearPointAlgebra.json")),
           Algebra(os.path.join(path, "rightBranchingPointAlgebra.json")),
           Algebra(os.path.join(path, "leftBranchingPointAlgebra.json"))
           ]

    for a in alg:
        print("\n{}:".format(a.name))
        print("Relations {}: ".format(a.relations))
        if a.check_multiplication_identity():
            print("Multiplication Identity OK for {}.".format(a.name))
        else:
            print("Multiplication Identity Failed for {}.".format(a.name))

    print("{}:".format(alg[0].name))
    entity_x = TemporalObject(["ProperInterval"], "X")
    entity_y = TemporalObject(["ProperInterval"], "Y")
    entity_z = TemporalObject(["ProperInterval"], "Z")
    r12 = alg[0].relations["B"]
    r23 = alg[0].relations["D"]
    print("\n")
    print("Constraint: {} {} {}".format(entity_x.name, r12.full_name, entity_y.name))
    print("Constraint: {} {} {}".format(entity_y.name, r23.full_name, entity_z.name))
    net0 = Network(alg[0], "Test0")
    net0.constraint(entity_x, entity_y, [r12])
    net0.constraint(entity_y, entity_z, [r23])
    net0.print_constraints()
    net0.propagate(verbose=True)
    net0.print_constraints()
    print("\n")

    print("{}:".format(alg[1].name))
    entity_x1 = TemporalObject(["Point", "ProperInterval"], "X1")
    entity_y1 = TemporalObject(["Point", "ProperInterval"], "Y1")
    entity_z1 = TemporalObject(["Point", "ProperInterval"], "Z1")
    s12 = alg[1].relations["B"]
    s23 = alg[1].relations["D"]
    print("\n")
    print("Constraint: {} {} {}".format(entity_x1, s12.full_name, entity_y1))
    print("Constraint: {} {} {}".format(entity_y1, s23.full_name, entity_z1))
    net1 = Network(alg[1], "Test1")
    net1.constraint(entity_x1, entity_y1, [s12])
    net1.constraint(entity_y1, entity_z1, [s23])
    # net1.constraint(entity_x1, entity_z1)
    net1.print_constraints()
    net1.propagate(verbose=True)
    net1.print_constraints()
    print("\n")

    # Example in book on constraint processing for temporal reasoning
    pint_I = TemporalObject(["ProperInterval"], "I")
    pint_J = TemporalObject(["ProperInterval"], "J")
    pint_K = TemporalObject(["ProperInterval"], "K")
    pint_L = TemporalObject(["ProperInterval"], "L")
    D0 = alg[0].relations["D"]
    DI0 = alg[0].relations["DI"]
    F0 = alg[0].relations["F"]
    FI0 = alg[0].relations["FI"]
    M0 = alg[0].relations["M"]
    O0 = alg[0].relations["O"]
    S0 = alg[0].relations["S"]
    net2 = Network(alg[0], "Book Example")
    net2.constraint(pint_I, pint_J, [F0, FI0])
    net2.constraint(pint_I, pint_L, [S0, M0])
    net2.constraint(pint_L, pint_J, [S0, M0])
    net2.constraint(pint_K, pint_I, [D0, DI0])
    net2.constraint(pint_K, pint_J, [D0, DI0])
    net2.constraint(pint_L, pint_K, [O0])
    net2.print_constraints()
    net2.propagate(verbose=True)
    net2.print_constraints()

    # Example in book on constraint processing for temporal reasoning
    # (extended to intervals & points)
    pint_I = TemporalObject(["Point", "ProperInterval"], "I")
    pint_J = TemporalObject(["Point", "ProperInterval"], "J")
    pint_K = TemporalObject(["Point", "ProperInterval"], "K")
    pint_L = TemporalObject(["Point", "ProperInterval"], "L")
    D1 = alg[1].relations["D"]
    DI1 = alg[1].relations["DI"]
    F1 = alg[1].relations["F"]
    FI1 = alg[1].relations["FI"]
    M1 = alg[1].relations["M"]
    O1 = alg[1].relations["O"]
    S1 = alg[1].relations["S"]
    net2x = Network(alg[1], "Book Example Extended")
    net2x.constraint(pint_I, pint_J, [F1, FI1])
    net2x.constraint(pint_I, pint_L, [S1, M1])
    net2x.constraint(pint_L, pint_J, [S1, M1])
    net2x.constraint(pint_K, pint_I, [D1, DI1])
    net2x.constraint(pint_K, pint_J, [D1, DI1])
    net2x.constraint(pint_L, pint_K, [O1])
    net2x.print_constraints()
    net2x.propagate(verbose=True)
    net2x.print_constraints()

    # Associativity example done as a network instead
    x1 = TemporalObject(["Point", "ProperInterval"], "X")
    y1 = TemporalObject(["Point", "ProperInterval"], "Y")
    z1 = TemporalObject(["Point", "ProperInterval"], "Z")
    u1 = TemporalObject(["Point", "ProperInterval"], "U")
    ps1 = alg[1].relations["PS"]
    b1 = alg[1].relations["B"]
    d1 = alg[1].relations["D"]
    net3 = Network(alg[1], "Associativity Test")
    net3.constraint(x1, y1, [ps1])
    net3.constraint(y1, z1, [b1])
    net3.constraint(z1, u1, [d1])
    net3.print_constraints()
    net3.propagate(verbose=True)
    net3.print_constraints()

    print("\n{} is associative? {}\n".format(alg[0].name, str(alg[0].is_associative())))
#    print "\n{} is associative? {}\n" % (alg[1].short_name, str(alg[1].is_associative(verbose=True)))
#    print "\n{} is associative? {}" % (alg2.short_name, str(alg2.is_associative()))
#    print "\n{} is associative? {}" % (alg3.short_name, str(alg3.is_associative()))
#    print "\n{} is associative? {}" % (alg4.short_name, str(alg4.is_associative()))

    # Region Connection Calculus 8:

    # Example from http://en.wikipedia.org/wiki/RCC8
    alg4 = Algebra(os.path.join(path, "rcc8Algebra.json"))

    DC = alg4.relations['DC']
    EC = alg4.relations['EC']
    PO = alg4.relations['PO']
    TPP = alg4.relations['TPP']
    NTPP = alg4.relations['NTPP']
    TPPI = alg4.relations['TPPI']
    NTPPI = alg4.relations['NTPPI']
    EQ = alg4.relations['EQ']

    house1 = SpatialObject(["Region"], "house1")
    house2 = SpatialObject(["Region"], "house2")
    property1 = SpatialObject(["Region"], "property1")
    property2 = SpatialObject(["Region"], "property2")
    road = SpatialObject(["Region"], "road")
    net4 = Network(alg4, "Wikipedia RCC8 Example")

    net4.constraint(house1, house2, [DC])
    net4.constraint(house1, property1, [TPP, NTPP])
    net4.constraint(house1, property2, [DC, EC])
    net4.constraint(house1, road, [EC])
    net4.constraint(house2, property1, [DC, EC])
    net4.constraint(house2, property2, [NTPP])
    net4.constraint(house2, road, [EC])
    net4.constraint(property1, property2, [DC, EC])
    net4.constraint(road, property1, [DC, EC, TPP, TPPI, PO, EQ, NTPP, NTPPI])
    net4.constraint(road, property2, [DC, EC, TPP, TPPI, PO, EQ, NTPP, NTPPI])

    net4.print_constraints()
    net4.propagate(verbose=True)
    net4.print_constraints()

    # Note: According to Wikipedia, the correct constraints
    # between 'road' and 'property1', and
    # between 'road' and 'property2' are:
    #   road { PO, EC } property1
    #   road { PO, TPP } property2

    # End of File
