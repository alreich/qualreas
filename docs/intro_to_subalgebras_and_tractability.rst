Reasoning with Relation Algebras: Subalgebras, Consistency, and Tractability
============================================================================

A Primer for the Notebook, *Subalgebras of Allen’s Algebra*
-----------------------------------------------------------

*qualreas* began as a teaching tool: a way to see how relation algebras
such as Allen’s algebra of time intervals and the Region Connection
Calculus work, and how constraint networks over them are propagated. The
notebook, **subalgebras_of_allens_algebra**, takes the package a step
toward being a research tool. It generates and tests *subalgebras* of
Allen’s algebra, and it asks which of them can be reasoned with
efficiently.

To do that, it uses a vocabulary from the research literature on
qualitative temporal and spatial reasoning that appears nowhere else in
this documentation: *closure*, *generators*, *convex*, *pointisable*,
*ORD-Horn clause*, *path consistent but inconsistent*, *NP-hard*,
*tractable*, *maximality*, and more. This notebook is the bridge. It
introduces those terms one at a time, in the setting of the algebras
that *qualreas* supports, and it gives code that you can run and change.
It is meant to be read **before** the subalgebras notebook.

**What you need to know first.** Only the basics from the README and the
notebook *Allens_Interval_Algebra*:

- An **Algebra** is built from a set of *basic relations*, such as the
  13 relations of Allen’s algebra.
- A **RelSet** is a set of basic relations, read as “one of these
  holds”, such as ``B|M``.
- RelSets can be intersected (``+``), have converses taken
  (``Algebra.converse``), and be composed (``Algebra.compose``).
- A **constraint network** has entities as nodes and RelSets as edge
  constraints.

Some comfort with sets and with logical *and* / *or* is enough for the
rest. No background in complexity theory is assumed; the necessary parts
are explained in the section on complexity.

**Scope.** The examples use Allen’s algebra of proper time intervals (13
basic relations) and the linear point algebra (3 basic relations: ``<``,
``=``, ``>``). They are used because the families of RelSets that the
next notebook studies are defined for them, and because the algebras are
small enough to explore exhaustively. The vocabulary, however, applies
to any of the algebras in *qualreas*, RCC8 included.

**The code.** The functions defined in this notebook (``draw``,
``basic_relation``, ``find_solution``, and so on) are helpers for
teaching; they are not part of *qualreas*. The functions that *are* part
of *qualreas* have the prefix ``qr.`` or are methods of an Algebra, such
as ``allen.closure``.

Table of Contents
-----------------

- `Setting Up <#setup>`__
- `1. RelSets, Disjunctions and Conjunctions <#relsets>`__
- `2. The Three Operations: Intersection, Converse,
  Composition <#ops>`__
- `3. Subalgebras, Closure, and Generators <#subalg>`__
- `4. Intervals Are Made of Points: Convex, Pointisable and ORD-Horn
  RelSets <#families>`__
- `5. Consistency and Inconsistency <#consistency>`__
- `6. Path Consistency, and Networks that are Path Consistent but
  Inconsistent <#pc>`__
- `7. Complexity: Decidability, NP-hard, NP-complete, Tractable,
  Maximal <#complexity>`__
- `8. Searching for Tractable Subalgebras: Refuted
  Subalgebras <#search>`__
- `Glossary <#glossary>`__
- `Exercises <#exercises>`__
- `References <#refs>`__

Setting Up 
-----------

.. code:: ipython3

    import itertools
    import os
    from functools import lru_cache
    
    import qualreas as qr
    
    allen = qr.Algebra(os.path.join(qr.ALGEBRA_DIR, "Linear_Interval_Algebra.json"))
    points = qr.Algebra(os.path.join(qr.ALGEBRA_DIR, "Linear_Point_Algebra.json"))
    
    print(allen)
    print(f"{len(allen.elements)} basic relations: {allen.elements}")
    print()
    print(points)
    print(f"{len(points.elements)} basic relations: {points.elements}")


.. parsed-literal::

    <Linear_Interval_Algebra: Allen's algebra of proper time intervals>
    13 basic relations: B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI
    
    <Linear_Point_Algebra: Linear Point Algebra>
    3 basic relations: <|=|>


A small helper that prints a collection of RelSets, from the smallest to
the largest:

.. code:: ipython3

    def show(relsets, limit=None):
        ordered = sorted(relsets, key=lambda rs: (len(rs.members()), str(rs)))
        for rs in ordered[:limit]:
            print(str(rs) or "{} (the empty RelSet)")

1. RelSets, Disjunctions and Conjunctions 
------------------------------------------

A **basic relation** (also called an **atom**) is one of the relations
from which an algebra is built: the 13 relations **B**, **BI**, **M**,
**MI**, **O**, **OI**, **S**, **SI**, **D**, **DI**, **F**, **FI**,
**E** of Allen’s algebra, or ``<``, ``=``, ``>`` for the point algebra.
Between any two entities exactly one basic relation holds, though we may
not know which.

A **RelSet** expresses what we know. The constraint “X ``B|M`` Y” says
that X is before Y **or** X meets Y. Two words from logic are needed
here:

- A **disjunction** is an *or*: “A or B” is true when at least one of A
  and B is true.
- A **conjunction** is an *and*: “A and B” is true only when both A and
  B are true.

Each RelSet is a *disjunction* of basic relations. A constraint network
is a *conjunction* of such constraints, since every edge’s constraint
must hold at the same time. So a network is an *and* of *or*\ s. The
more relations a RelSet has, the weaker it is: the RelSet with all 13
relations, called here the **universal RelSet**, says nothing at all; a
RelSet with a single relation says everything; and the **empty RelSet**
says something impossible.

To make this concrete, here are proper intervals as pairs of end points,
a function that tells which basic relation holds between two of them,
and a way to draw them. (The relation is found from the order of the
four end points. The function ``qr.endpoint_orderings`` is used by
*qualreas* to derive interval algebras from point algebras, and is
explained further in Section 4.)

.. code:: ipython3

    orderings = qr.endpoint_orderings(allen)
    
    PAIRS = [(0, 1), (2, 3), (0, 2), (0, 3), (1, 2), (1, 3)]    # the order used by endpoint_orderings
    by_ordering = {tuple(orderings[name][pair] for pair in PAIRS): name for name in allen.elements}
    
    def compare(a, b):
        return '<' if a < b else ('=' if a == b else '>')
    
    @lru_cache(maxsize=None)
    def basic_relation(x, y):
        # The basic relation of Allen's algebra that holds between proper intervals x = (s1, e1) and y = (s2, e2).
        ends = (x[0], x[1], y[0], y[1])
        return by_ordering[tuple(compare(ends[i], ends[j]) for (i, j) in PAIRS)]
    
    def draw(**intervals):
        # Print intervals (s, e) as bars; the bar covers the unit cells s, s+1, ..., e-1.
        width = max(e for (s, e) in intervals.values())
        for name, (s, e) in intervals.items():
            print(f"{name:>3}  " + "".join('=' if s <= t < e else '.' for t in range(width)) + f"   ({s}, {e})")
    
    X, Y = (1, 3), (3, 6)
    draw(X=X, Y=Y)
    print("basic relation between X and Y:", basic_relation(X, Y))


.. parsed-literal::

      X  .==...   (1, 3)
      Y  ...===   (3, 6)
    basic relation between X and Y: M


The interval X ends exactly where Y begins, so X **M**\ eets Y. A RelSet
constraint holds when the actual basic relation is one of its members:

.. code:: ipython3

    def holds(constraint, x, y):
        return basic_relation(x, y) in allen.relset(constraint).members()
    
    print("X B|M Y :", holds("B|M", X, Y))
    print("X B|D Y :", holds("B|D", X, Y))


.. parsed-literal::

    X B|M Y : True
    X B|D Y : False


A network is a conjunction of constraints. Here is a network of three
nodes, 0, 1 and 2, given as a dictionary that maps a pair of node
numbers to a constraint. (This is the form that the *Algebra* methods
used in this notebook take. It is lighter than a *Network* object, and
it has the same meaning: a pair that is left out is unconstrained.) An
assignment of an interval to each node satisfies the network when it
satisfies *every* constraint:

.. code:: ipython3

    network = {(0, 1): "B|M", (1, 2): "D"}      # node 0 is before-or-meets node 1, and node 1 is during node 2
    
    def satisfies(network, assignment):
        return all(holds(constraint, assignment[i], assignment[j]) for (i, j), constraint in network.items())
    
    good = [(0, 2), (3, 5), (2, 6)]
    bad  = [(0, 2), (3, 5), (4, 8)]
    
    draw(n0=good[0], n1=good[1], n2=good[2])
    print("satisfies the network:", satisfies(network, good))
    print()
    draw(n0=bad[0], n1=bad[1], n2=bad[2])
    print("satisfies the network:", satisfies(network, bad), "  (node 1, (3, 5), is not during node 2, (4, 8))")


.. parsed-literal::

     n0  ==....   (0, 2)
     n1  ...==.   (3, 5)
     n2  ..====   (2, 6)
    satisfies the network: True
    
     n0  ==......   (0, 2)
     n1  ...==...   (3, 5)
     n2  ....====   (4, 8)
    satisfies the network: False   (node 1, (3, 5), is not during node 2, (4, 8))


2. The Three Operations: Intersection, Converse, Composition 
-------------------------------------------------------------

Three operations on RelSets matter for everything that follows. They are
in the README, but they are central here, so they are restated.

+------------------+-------------+-------------+---------------------------+
| Operation        | Written     | Meaning     | In *qualreas*             |
+==================+=============+=============+===========================+
| **Intersection** | R + S       | Both R and  | ``R + S``                 |
|                  |             | S hold:     |                           |
|                  |             | keep the    |                           |
|                  |             | relations   |                           |
|                  |             | that are in |                           |
|                  |             | both        |                           |
|                  |             | RelSets.    |                           |
+------------------+-------------+-------------+---------------------------+
| **Converse**     | R⁻¹         | If X R Y,   | ``Algebra.converse(R)``   |
|                  |             | then Y R⁻¹  |                           |
|                  |             | X: replace  |                           |
|                  |             | each        |                           |
|                  |             | relation by |                           |
|                  |             | its         |                           |
|                  |             | converse.   |                           |
+------------------+-------------+-------------+---------------------------+
| **Composition**  | R ; S       | If X R Y    | ``Algebra.compose(R, S)`` |
|                  |             | and Y S Z,  |                           |
|                  |             | then X (R ; |                           |
|                  |             | S) Z: the   |                           |
|                  |             | relations   |                           |
|                  |             | that can    |                           |
|                  |             | hold        |                           |
|                  |             | between X   |                           |
|                  |             | and Z.      |                           |
+------------------+-------------+-------------+---------------------------+

(Union, the relations that are in *either* RelSet, is also available, as
``R.union(S)``. It is left out of the list because the subalgebras
studied here are **not** required to be closed under it; see the next
section.)

The composition of basic relations is stored in the algebra’s
composition table. What does that table mean? It is the answer to this
question: “knowing only that X R Y and that Y S Z, what *can* the
relation between X and Z be?” We can check that against actual
intervals, by trying every triple of intervals with end points in 0, 1,
…, 5 (six positions are enough for three intervals, because only the
order of the end points matters):

.. code:: ipython3

    b, d = allen.relset("B"), allen.relset("D")
    print("B ; D =", allen.compose(b, d))
    
    grid = range(6)
    intervals = [(s, e) for s in grid for e in grid if s < e]
    
    seen = {basic_relation(x, z)
            for x, y, z in itertools.product(intervals, repeat=3)
            if basic_relation(x, y) == "B" and basic_relation(y, z) == "D"}
    
    print("relations actually seen between X and Z, over all X B Y and Y D Z:", "|".join(sorted(seen)))


.. parsed-literal::

    B ; D = B|D|M|O|S
    relations actually seen between X and Z, over all X B Y and Y D Z: B|D|M|O|S


The two agree, so the table is right in this case. The other operations
are used the same way:

.. code:: ipython3

    bm = allen.relset("B|M")
    
    print("intersection:  B|M + B|O      =", bm + allen.relset("B|O"))
    print("union:         B|M union B|O  =", bm.union(allen.relset("B|O")))
    print("converse:      (B|M)^-1       =", allen.converse(bm))
    print("composition:   (B|M) ; D      =", allen.compose(bm, d))
    print()
    print("A disjoint intersection is the empty RelSet:", repr(allen.relset("B") + allen.relset("D")))


.. parsed-literal::

    intersection:  B|M + B|O      = B
    union:         B|M union B|O  = B|M|O
    converse:      (B|M)^-1       = BI|MI
    composition:   (B|M) ; D      = B|D|M|O|S
    
    A disjoint intersection is the empty RelSet: relset()


3. Subalgebras, Closure, and Generators 
----------------------------------------

Allen’s algebra with 13 basic relations has :math:`2^{13} = 8192`
RelSets (the empty one included). The **algebra** is made of all of
them, together with the three operations above. It is often useful to
work with only some of the RelSets: those that are simple enough to
reason with efficiently, say. To keep such a collection useful, it
should be **closed** under the operations, so that reasoning with its
members never forces us out of the collection. That gives the following
definitions.

- A collection of RelSets is **closed** under an operation if applying
  the operation to members of the collection always gives a member of
  the collection. For example, a collection is closed under converse if
  the converse of every member is a member.
- A **subalgebra** is a collection of RelSets that is closed under
  intersection, converse and composition. (This is the sense used in the
  literature on qualitative reasoning, for example by Nebel and
  Bürckert. In universal algebra one might also ask for closure under
  union and complement. Those operations are deliberately *not* required
  here; the ORD-Horn subalgebra of the next section, for instance, is
  not closed under union.)
- The **closure** of a collection of RelSets is the smallest subalgebra
  that contains the collection. It is computed by applying the three
  operations over and over to the RelSets, and to everything that they
  produce, until nothing new appears. In *qualreas* it is
  ``Algebra.closure``.
- If the closure of a collection :math:`G` is a subalgebra :math:`S`, we
  say that :math:`G` **generates** :math:`S`, and that the RelSets in
  :math:`G` are **generators** of :math:`S`. A subalgebra can have many
  different sets of generators.

First, a function that checks whether a collection is closed, straight
from the definition:

.. code:: ipython3

    def is_closed(algebra, family):
        family = set(family)
        for a in family:
            if algebra.converse(a) not in family:
                return False
        for a, b in itertools.product(family, repeat=2):
            if (a + b) not in family or algebra.compose(a, b) not in family:
                return False
        return True
    
    S = {allen.relset("B"), allen.relset("D")}
    print(f"{{B, D}} is closed: {is_closed(allen, S)}")
    print(f"  because B ; D = {allen.compose(allen.relset('B'), allen.relset('D'))}, and converse(B) = {allen.converse(allen.relset('B'))}; neither is in the collection.")


.. parsed-literal::

    {B, D} is closed: False
      because B ; D = B|D|M|O|S, and converse(B) = BI; neither is in the collection.


The closure of :math:`\{B, D\}` adds whatever is needed:

.. code:: ipython3

    closure = allen.closure(["B", "D"])
    
    print(f"The closure of {{B, D}} has {len(closure)} RelSets, and it is closed: {is_closed(allen, closure)}")
    print(f"It contains B and D: {allen.relset('B') in closure and allen.relset('D') in closure}")
    print()
    show(closure)


.. parsed-literal::

    The closure of {B, D} has 21 RelSets, and it is closed: True
    It contains B and D: True
    
    {} (the empty RelSet)
    B
    BI
    D
    DI
    O
    OI
    BI|MI|OI
    B|M|O
    DI|FI|O
    DI|OI|SI
    D|F|OI
    D|O|S
    BI|DI|MI|OI|SI
    BI|D|F|MI|OI
    B|DI|FI|M|O
    B|D|M|O|S
    D|DI|E|F|FI|O|OI|S|SI
    BI|D|DI|E|F|FI|MI|O|OI|S|SI
    B|D|DI|E|F|FI|M|O|OI|S|SI
    B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI


Those are all of the RelSets that can be produced from **B** and **D**
with the three operations, and no others. Note that closure never adds
*union*: **B|D**, for example, is not in the list.

The point algebra is small enough that we can see every closure. It has
only :math:`2^3 = 8` RelSets. Which subalgebras are generated depends on
the generators chosen:

.. code:: ipython3

    def closure_of(*relsets):
        result = points.closure(relsets)
        print(f"closure of {{{', '.join(relsets)}}} has {len(result)} RelSets:")
        show(result)
        print()
    
    closure_of("<", "=", ">")
    closure_of("<", "=", ">", "<|=")
    closure_of("<", "=", ">", "<|>")
    closure_of("<|=", ">|=")


.. parsed-literal::

    closure of {<, =, >} has 5 RelSets:
    {} (the empty RelSet)
    <
    =
    >
    <|=|>
    
    closure of {<, =, >, <|=} has 7 RelSets:
    {} (the empty RelSet)
    <
    =
    >
    <|=
    =|>
    <|=|>
    
    closure of {<, =, >, <|>} has 6 RelSets:
    {} (the empty RelSet)
    <
    =
    >
    <|>
    <|=|>
    
    closure of {<|=, >|=} has 4 RelSets:
    =
    <|=
    =|>
    <|=|>
    


In the first of these, the three basic relations generate five RelSets:
the three basic ones, the universal RelSet ``<|=|>``, and the empty
RelSet (since ``<`` + ``>`` is empty). Adding the RelSet “less than or
equal”, ``<|=``, gives seven RelSets; adding “not equal”, ``<|>``,
instead gives six. The last example shows that a *small* set of
generators, here just ``<|=`` and ``>|=``, can generate a subalgebra
that does not contain the basic relations ``<`` and ``>`` at all.

Closure can also tell us what **cannot** be reached. The closure of the
13 basic relations of Allen’s algebra is much smaller than the algebra,
and does not even contain the RelSet **S|SI** (“X and Y start
together”):

.. code:: ipython3

    basics = [allen.relset([rel]) for rel in allen.elements]
    generated = allen.closure(basics)
    
    print(f"The closure of the 13 basic relations has {len(generated)} RelSets (out of {2**13}).")
    print(f"S|SI is in it: {allen.relset('S|SI') in generated}")


.. parsed-literal::

    The closure of the 13 basic relations has 30 RelSets (out of 8192).
    S|SI is in it: False


To get **S|SI** (and the other RelSets of the next section) we must add
it, or another RelSet from which it can be made, to the generators.
Which small sets of extra generators are enough to produce a whole
family is exactly the sort of question that the next notebook asks of
``Algebra.closure``.

**A caution about the word “closure”.** The literature on constraint
networks uses *algebraic closure* as another name for *path
consistency*, which is the subject of Section 6 (Ladkin and Maddux,
1994). It is a process applied to **one network**. In *qualreas*,
``Algebra.closure`` is something else: it is applied to **a collection
of RelSets**, and it has nothing to do with any network. The two ideas
are related in the next notebook, but they are not the same, and the
*qualreas* method for the first is ``Algebra.path_consistency``.

4. Intervals Are Made of Points: Convex, Pointisable and ORD-Horn RelSets 
--------------------------------------------------------------------------

Every basic relation of Allen’s algebra is one of the 13 ways in which
the four end points of two proper intervals can be ordered. Let the
first interval be X = (s1, e1) and the second Y = (s2, e2), where s1 <
e1 and s2 < e2. The function ``qr.endpoint_orderings`` gives the
ordering for each relation. The end points are numbered 0 to 3, for s1,
e1, s2 and e2. For example:

.. code:: ipython3

    for name in ["B", "M", "S"]:
        print(f"{name:>2}: {orderings[name]}")


.. parsed-literal::

     B: {(0, 1): '<', (2, 3): '<', (0, 2): '<', (0, 3): '<', (1, 2): '<', (1, 3): '<'}
     M: {(0, 1): '<', (2, 3): '<', (0, 2): '<', (0, 3): '<', (1, 2): '=', (1, 3): '<'}
     S: {(0, 1): '<', (2, 3): '<', (0, 2): '=', (0, 3): '<', (1, 2): '>', (1, 3): '<'}


The relation **M** (Meets) has ``(1, 2): '='``, which says that e1 = s2;
the relation **S** (Starts) has ``(0, 2): '='`` and ``(1, 3): '<'``,
which say that s1 = s2 and e1 < e2. So a RelSet is a set of orderings of
end points, and a statement about end points *describes* a RelSet: the
set of basic relations whose orderings make the statement true. This
gives a new way to get RelSets, starting from statements about points.

**Point formulas, clauses and conjunctions.** Let p and q be two of the
four end points. The simplest statements are the **atomic formulas**
``p < q``, ``p <= q``, ``p = q`` and ``p != q``. (``p > q`` and
``p >= q`` are the same as ``q < p`` and ``q <= p``.) Atomic formulas
can be combined:

- a **clause** is a disjunction of atomic formulas, such as
  ``e1 < s2 or e2 < s1``;
- a **conjunction** of clauses is a statement that all of the clauses
  are true, such as ``s1 = s2 and e1 != e2``, which is a conjunction of
  two clauses of one atomic formula each.

The following helper turns such a statement into the RelSet that it
describes. (The statement is read as a conjunction, separated by
``and``, of clauses, separated by ``or``.)

.. code:: ipython3

    END = {"s1": 0, "e1": 1, "s2": 2, "e2": 3}
    FLIP = {"<": ">", "=": "=", ">": "<"}
    ALLOWED = {"<": {"<"}, "<=": {"<", "="}, "=": {"="}, "!=": {"<", ">"}}
    
    def end_relation(name, p, q):
        # The point relation between end points p and q, in the basic relation `name`
        i, j = END[p], END[q]
        return orderings[name][(i, j)] if i < j else FLIP[orderings[name][(j, i)]]
    
    def parse(formula):
        return [[tuple(atom.split()) for atom in clause.strip("() ").split(" or ")]
                for clause in formula.split(" and ")]
    
    def relset_of(formula):
        # The RelSet of the basic relations that make a conjunction of clauses true
        clauses = parse(formula)
        names = [name for name in allen.elements
                 if all(any(end_relation(name, p, q) in ALLOWED[op] for (p, op, q) in clause) for clause in clauses)]
        return allen.relset(names)
    
    print("e1 <= s2                :", relset_of("e1 <= s2"))
    print("s1 = s2 and e1 != e2    :", relset_of("s1 = s2 and e1 != e2"))
    print("e1 < s2 or e2 < s1      :", relset_of("e1 < s2 or e2 < s1"))


.. parsed-literal::

    e1 <= s2                : B|M
    s1 = s2 and e1 != e2    : S|SI
    e1 < s2 or e2 < s1      : B|BI


So “e1 <= s2” (“X ends no later than Y starts”) is **B|M**; “X and Y
start together but end differently” is **S|SI**; and “X is entirely
before Y, or entirely after Y” is **B|BI**.

Not every RelSet can be described by a statement of a simple kind, and
the *simplicity* of the statement is what matters for reasoning. Three
families of RelSets are defined by how simple the statement is:

+-----------------+----------------------------+--------------------------+
| Family          | In *qualreas*              | Described by             |
+=================+============================+==========================+
| **Convex**      | ``qr.convex_relsets``      | a conjunction of atomic  |
|                 |                            | formulas of the forms    |
|                 |                            | ``p < q``, ``p <= q``    |
|                 |                            | and ``p = q``            |
+-----------------+----------------------------+--------------------------+
| **Pointisable** | ``qr.pointisable_relsets`` | a conjunction of atomic  |
|                 |                            | formulas of those forms  |
|                 |                            | and also ``p != q``      |
+-----------------+----------------------------+--------------------------+
| **ORD-Horn**    | ``qr.ord_horn_relsets``    | a conjunction of         |
| (H)             |                            | **ORD-Horn clauses**     |
+-----------------+----------------------------+--------------------------+

An **ORD-Horn clause** is a disjunction of atomic formulas that has any
number of formulas of the form ``p != q``, but **at most one** formula
of the forms ``p < q``, ``p <= q`` and ``p = q``. The name comes from
*Horn clauses* in propositional logic, which are disjunctions of at most
one non-negated literal and any number of negated ones. The analogy is
loose, but helpful: ``p != q`` is the negation of ``p = q``, so it plays
the part of a negated literal, and the other three play the part of
non-negated literals. A clause like ``e1 < s2 or e2 < s1`` has *two* of
those, so it is **not** an ORD-Horn clause, and a clause like
``s1 != s2 or e1 != e2`` is one (it has none).

The words *pointisable* (“can be turned into points”) and *convex* come
from the literature (see the references). *Pointisable* is because an
interval constraint of this kind can be translated into constraints
between points, and *convex* is explained next, using the point algebra.

**Convexity, seen in the point algebra.** For the three point relations,
ordered as ``<``, ``=``, ``>``, a RelSet is called **convex** when it
has no gaps: it is a run of neighbours in that order. So ``<|=`` is
convex, but ``<|>`` (“not equal”) is not, because it skips ``=``. There
are seven convex RelSets (counting the empty one), and they are exactly
the RelSets that need no “not equal”:

.. code:: ipython3

    order = ["<", "=", ">"]
    
    def has_no_gaps(relset):
        positions = sorted(order.index(r) for r in relset.members())
        return all(b - a == 1 for a, b in zip(positions, positions[1:]))
    
    all_point_relsets = [points.relset(list(c)) for k in range(4) for c in itertools.combinations(order, k)]
    convex_points = frozenset(rs for rs in all_point_relsets if has_no_gaps(rs))
    
    print(f"{len(all_point_relsets)} RelSets of the point algebra; {len(convex_points)} have no gaps:")
    show(convex_points)
    print()
    print("They are the closure of <, =, > and <|= :", convex_points == points.closure(["<", "=", ">", "<|="]))


.. parsed-literal::

    8 RelSets of the point algebra; 7 have no gaps:
    {} (the empty RelSet)
    <
    =
    >
    <|=
    =|>
    <|=|>
    
    They are the closure of <, =, > and <|= : True


For Allen’s algebra, the convex RelSets are described by the same kind
of statement: conjunctions of ``<``, ``<=`` and ``=`` on end points,
with no ``!=``. Ligozat (1991) gives a geometric characterization of the
family. Here it is defined directly by formulas, which is how
``qr.convex_relsets`` defines it.

Here are the three families for Allen’s algebra, and how they are
related:

.. code:: ipython3

    convex = qr.convex_relsets(allen)
    pointisable = qr.pointisable_relsets(allen)
    ord_horn = qr.ord_horn_relsets(allen)
    
    print(f"Convex:      {len(convex):4d} RelSets")
    print(f"Pointisable: {len(pointisable):4d} RelSets")
    print(f"ORD-Horn:    {len(ord_horn):4d} RelSets   (out of {2**13})")
    print()
    print(f"Every convex RelSet is pointisable:        {convex < pointisable}")
    print(f"Every pointisable RelSet is ORD-Horn:      {pointisable < ord_horn}")


.. parsed-literal::

    Convex:        83 RelSets
    Pointisable:  188 RelSets
    ORD-Horn:     868 RelSets   (out of 8192)
    
    Every convex RelSet is pointisable:        True
    Every pointisable RelSet is ORD-Horn:      True


(The convex RelSets are usually counted as 82; the number here is 83
because the empty RelSet is counted.) Here are some statements, the
RelSets that they describe, and the families that those RelSets belong
to:

.. code:: ipython3

    statements = ["e1 <= s2",
                  "s1 < e2 and s2 < e1",
                  "s1 = s2 and e1 != e2",
                  "s1 != s2 or e1 != e2",
                  "e1 < s2 or e2 < s1"]
    
    print(f"{'statement':24} {'RelSet':32} {'convex':>6} {'pointisable':>12} {'ORD-Horn':>9}")
    for statement in statements:
        rs = relset_of(statement)
        print(f"{statement:24} {str(rs):32} {str(rs in convex):>6} {str(rs in pointisable):>12} {str(rs in ord_horn):>9}")


.. parsed-literal::

    statement                RelSet                           convex  pointisable  ORD-Horn
    e1 <= s2                 B|M                                True         True      True
    s1 < e2 and s2 < e1      D|DI|E|F|FI|O|OI|S|SI              True         True      True
    s1 = s2 and e1 != e2     S|SI                              False         True      True
    s1 != s2 or e1 != e2     B|BI|D|DI|F|FI|M|MI|O|OI|S|SI     False        False      True
    e1 < s2 or e2 < s1       B|BI                              False        False     False


Reading the rows from the top:

- “X ends no later than Y starts” (**B|M**) is convex.
- “X and Y share some time” (everything except **B**, **BI**, **M** and
  **MI**) is convex too.
- “X and Y start together but end differently” (**S|SI**) needs a
  ``!=``, so it is pointisable but not convex.
- “X and Y are different intervals” is every relation except **E**. It
  is a single ORD-Horn clause, with two ``!=`` and nothing else, and it
  is in H, but it is *not* pointisable: it needs an *or*.
- “X and Y do not overlap or touch” (**B|BI**) is not in H at all. The
  statement above is not an ORD-Horn clause, and no other statement of
  that kind describes the RelSet. We will see in Section 7 why that
  makes the RelSet significant.

H is closed under intersection, converse and composition, so it is a
subalgebra, but it is not closed under union: **B** and **BI** are both
in H, but their union, **B|BI**, is not. A check of the definition by
``Algebra.closure``:

.. code:: ipython3

    for name, family in [("Convex", convex), ("Pointisable", pointisable), ("ORD-Horn", ord_horn)]:
        print(f"{name:12} is a subalgebra: {allen.closure(family) == family}")
    
    b, bi = allen.relset("B"), allen.relset("BI")
    print()
    print(f"B in H: {b in ord_horn}    BI in H: {bi in ord_horn}    B|BI in H: {b.union(bi) in ord_horn}")


.. parsed-literal::

    Convex       is a subalgebra: True
    Pointisable  is a subalgebra: True
    ORD-Horn     is a subalgebra: True
    
    B in H: True    BI in H: True    B|BI in H: False


5. Consistency and Inconsistency 
---------------------------------

A constraint network is **consistent** when there is some way to choose
the entities so that every constraint is true: for Allen’s algebra, some
way of choosing actual intervals. Such a choice is a **solution** of the
network. A network with no solution is **inconsistent**. The question,
“is this network consistent?”, is the central problem of qualitative
reasoning, and it is the one whose difficulty is discussed in Section 7.

Here is an inconsistent network: node 0 is before node 1, which is
before node 2, so node 0 cannot also be *after* node 2.

.. code:: ipython3

    consistent_net   = {(0, 1): "B|M", (1, 2): "D"}
    inconsistent_net = {(0, 1): "B", (1, 2): "B", (0, 2): "BI"}
    
    print("consistent_net  :", allen.is_consistent(consistent_net))
    print("inconsistent_net:", allen.is_consistent(inconsistent_net))


.. parsed-literal::

    consistent_net  : True
    inconsistent_net: False


The method ``Algebra.is_consistent`` does not look for intervals. It
uses a different definition: a network is consistent if there is a way
to choose **one** basic relation for every pair of nodes, from the ones
that are allowed, so that the result is path consistent (a term defined
in the next section). Such a choice is called a **singleton labeling**,
or, when it is consistent, a **scenario**. For Allen’s algebra this is
equivalent to the first definition, because a path consistent network of
single relations can always be realized by actual intervals (Ladkin and
Maddux, 1994).

We can see the equivalence in action. The first definition can be tested
directly by a search for intervals. Only the *order* of end points
matters, and n intervals have at most 2n different end points, so it is
enough to try the integer positions 0, 1, …, 2n - 1:

.. code:: ipython3

    def find_solution(network, n):
        # Backtracking search for n proper intervals, with end points in 0..2n-1, that satisfy every constraint.
        # If there is no such assignment, then the network has no solution at all.
        candidates = [(s, e) for s in range(2 * n) for e in range(2 * n) if s < e]
        allowed = {pair: set(allen.relset(c).members()) for pair, c in network.items()}
        chosen = []
    
        def extend(k):
            if k == n:
                return True
            for interval in candidates:
                chosen.append(interval)
                if all(basic_relation(chosen[i], interval) in allowed[(i, k)] for i in range(k) if (i, k) in allowed):
                    if extend(k + 1):
                        return True
                chosen.pop()
            return False
    
        return list(chosen) if extend(0) else None
    
    solution = find_solution(consistent_net, 3)
    draw(**{f"n{i}": interval for i, interval in enumerate(solution)})
    print("a solution of consistent_net   :", solution)
    print("a solution of inconsistent_net :", find_solution(inconsistent_net, 3))


.. parsed-literal::

     n0  =..   (0, 1)
     n1  .=.   (1, 2)
     n2  ===   (0, 3)
    a solution of consistent_net   : [(0, 1), (1, 2), (0, 3)]
    a solution of inconsistent_net : None


The two definitions agree on a few hundred random networks of three
nodes (this is evidence, not a proof; the proof is in the paper cited):

.. code:: ipython3

    import random
    random.seed(0)
    names = list(allen.elements)
    agree = 0
    trials = 300
    for _ in range(trials):
        net = {pair: "|".join(random.sample(names, random.randint(1, 4))) for pair in [(0, 1), (0, 2), (1, 2)]}
        agree += allen.is_consistent(net) == (find_solution(net, 3) is not None)
    print(f"is_consistent and the search for intervals agree on {agree} of {trials} random networks")


.. parsed-literal::

    is_consistent and the search for intervals agree on 300 of 300 random networks


6. Path Consistency, and Networks that are Path Consistent but Inconsistent 
----------------------------------------------------------------------------

Searching for intervals, or for a scenario, can take a very long time.
**Path consistency** is a cheap, local way to *reduce* a network, which
sometimes shows that it is inconsistent. Its idea: for any three nodes
i, j and k, the constraint on (i, k) can be no looser than what the
constraints on (i, j) and (j, k) allow, namely their composition. So the
constraint C(i,k) is replaced by

   C(i,k) + ( C(i,j) ; C(j,k) )

where “+” is intersection and “;” is composition. This is repeated, for
every triple of nodes, until nothing changes. The result is called
**path consistent**. (It is also called *algebraically closed*; see the
caution in Section 3.) The idea is due to Montanari (1974) and Mackworth
(1977), and Allen (1983) used a propagation of this kind for networks of
intervals. If, at some stage, a constraint becomes the empty RelSet,
then the network is **inconsistent**, and we stop. The running time
grows with the *cube* of the number of nodes. In *qualreas* this is
``Algebra.path_consistency``, and it does the same thing as
``Network.propagate``, but on a bare dictionary, so it is much faster.

.. code:: ipython3

    for pair, relset in allen.path_consistency({(0, 1): "B", (1, 2): "D"}).items():
        print(f"{pair}: {relset}")
    print()
    print("path consistency of inconsistent_net:", allen.path_consistency(inconsistent_net))


.. parsed-literal::

    (0, 1): B
    (0, 2): B|D|M|O|S
    (1, 2): D
    
    path consistency of inconsistent_net: None


In the first network, node 0 is before node 1, which is during node 2,
and path consistency infers the new constraint on the pair (0, 2),
namely ``B|D|M|O|S``. This is the composition **B** ; **D**, which we
saw in Section 2. In the second, one constraint becomes empty, and the
result is ``None``: **path consistency has proved that the network is
inconsistent**.

This is a *sound* test: if it ever says “inconsistent”, it is right. But
it is not always *complete*: it can fail to notice an inconsistency. A
network that is path consistent, so that no triple of nodes shows a
problem, can still be inconsistent as a whole, because the contradiction
involves four or more nodes together. We say that it is **path
consistent but inconsistent**. Here is a network of four nodes that is
one. (It was found by a random search, as in Section 8, and it is
checked below by three independent methods.)

.. code:: ipython3

    trap = {(0, 1): "F|M", (0, 2): "DI|OI|S", (0, 3): "BI|S",
            (1, 2): "DI|F|O", (1, 3): "BI|D|F|SI", (2, 3): "D|SI"}
    
    def is_path_consistent(network, nodes):
        result = allen.path_consistency(network, nodes=nodes)
        if result is None:
            return False
        return all(result[pair] == (allen.relset(network[pair]) if pair in network else allen.elements) for pair in result)
    
    print("1. Path consistent as given (nothing changes, nothing empties):", is_path_consistent(trap, 4))
    print("2. Consistent according to is_consistent:", allen.is_consistent(trap))
    print("3. Intervals that satisfy it, by exhaustive search:", find_solution(trap, 4))


.. parsed-literal::

    1. Path consistent as given (nothing changes, nothing empties): True
    2. Consistent according to is_consistent: False
    3. Intervals that satisfy it, by exhaustive search: None


Check 3 is conclusive: four intervals have at most eight different end
points, so the search tried every possibility. The third method gives no
intervals, so there are none.

Why does ``is_consistent`` say so? Each pair of nodes has between two
and four possible relations, so there are
:math:`2 \times 3 \times 2 \times 3 \times 4 \times 2 = 288` singleton
labelings. If any of them were path consistent, the network would be
consistent. None is:

.. code:: ipython3

    pairs = list(trap)
    choices = [allen.relset(trap[pair]).members() for pair in pairs]
    
    total = 0
    path_consistent_ones = 0
    for labeling in itertools.product(*choices):
        total += 1
        if allen.path_consistency(dict(zip(pairs, labeling)), nodes=4) is not None:
            path_consistent_ones += 1
    
    print(f"{total} singleton labelings, of which {path_consistent_ones} are path consistent")


.. parsed-literal::

    288 singleton labelings, of which 0 are path consistent


So the lesson is that **path consistency is a one-way test**. A ``None``
result means that the network is inconsistent, but a result that is not
``None`` does not mean that it is consistent. Whether a result that is
not ``None`` *can* be trusted depends on which RelSets appear in the
network, and that is what the next two sections are about: the networks
whose constraints are all in a subalgebra for which path consistency
never fails in this way.

7. Complexity: Decidability, NP-hard, NP-complete, Tractable, Maximal 
----------------------------------------------------------------------

Is there a fast way to decide whether a network is consistent? The words
that describe the answer come from the theory of computational
complexity. They are used precisely in the literature, and the next
notebook uses them the same way.

**Decidability.** A yes-or-no question about inputs of any size is
**decidable** if some algorithm always finishes, and always gives the
right answer. Whether an Allen network is consistent is decidable, even
for the full algebra: try all singleton labelings, and test each for
path consistency. Not every question has this property (the halting
problem for programs is the standard example of one that does not).
Decidable says nothing about *speed*; the algorithm just described takes
a very long time.

The verb is also used for a method and a class of inputs. The next
notebook says that “path consistency **decides** consistency for a
subalgebra” when, for every network whose constraints are all in that
subalgebra, a result that is not ``None`` means that the network really
is consistent. In other words, on that class of inputs the method is
always right. Section 6 showed that on the full algebra it is not.

**Efficient and inefficient.** An algorithm runs in **polynomial time**
if its running time is bounded by a polynomial in the size of the input
(here, the number of nodes), such as :math:`n^3`. The class of questions
that have such algorithms is called **P**. An algorithm that has to try
all singleton labelings takes **exponential time**, which is hopeless
for large inputs:

.. code:: ipython3

    print(f"{'nodes':>5} {'pairs':>6}   {'13^pairs (singleton labelings, at worst)':>42}   {'n^3 (path consistency)':>22}")
    for n in (3, 4, 5, 6, 8, 10, 15):
        pairs = n * (n - 1) // 2
        print(f"{n:5d} {pairs:6d}   {13 ** pairs:42.2e}   {n ** 3:22d}")


.. parsed-literal::

    nodes  pairs     13^pairs (singleton labelings, at worst)   n^3 (path consistency)
        3      3                                     2.20e+03                       27
        4      6                                     4.83e+06                       64
        5     10                                     1.38e+11                      125
        6     15                                     5.12e+16                      216
        8     28                                     1.55e+31                      512
       10     45                                     1.34e+50                     1000
       15    105                                    9.21e+116                     3375


**NP.** A question is in **NP** if, whenever the answer is *yes*, there
is evidence that can be *checked* in polynomial time, called a
**certificate** (or witness). For Allen networks, a certificate that a
network is consistent is a scenario: a singleton labeling that is path
consistent. Checking it takes only a path consistency test. Finding one
may take much longer. P is contained in NP, and it is not known whether
they are equal; this is the famous **P versus NP** problem, and most
researchers believe that they are not.

.. code:: ipython3

    # A certificate that consistent_net is consistent: a singleton labeling, checked by one path consistency test.
    labeling = {(i, j): basic_relation(solution[i], solution[j]) for i, j in itertools.combinations(range(3), 2)}
    print("certificate:", labeling)
    print("it respects every constraint:", all(basic_relation(solution[i], solution[j]) in allen.relset(c).members()
                                               for (i, j), c in consistent_net.items()))
    print("and it is path consistent   :", is_path_consistent(labeling, 3))


.. parsed-literal::

    certificate: {(0, 1): 'M', (0, 2): 'S', (1, 2): 'D'}
    it respects every constraint: True
    and it is path consistent   : True


**NP-hard and NP-complete.** A problem is **NP-hard** if it is *at least
as hard as every problem in NP*: a fast algorithm for it would give a
fast algorithm for every problem in NP. A problem that is both NP-hard
and in NP is **NP-complete**; these are the hardest problems in NP. If P
is not equal to NP, as is generally believed, then **no polynomial-time
algorithm exists for an NP-hard problem**. Consistency of networks of
the full Allen algebra is NP-hard (Vilain and Kautz, 1986) and, by the
certificate above, NP-complete. (Some NP-hard problems are not in NP,
which is why “NP-hard” is the more common thing to say about problems
that ask for more than a yes or a no, such as computing the *minimal*
labeling of a network.) Notice the direction of the claims: “NP-hard” is
evidence of *difficulty*, and it is conditional on P not being NP. An
algorithm, on the other hand, is a proof of *ease*, and needs no
assumption.

**Tractable.** A set of RelSets is a **tractable algebra** (or
*tractable subalgebra*, or *tractable class*) if consistency can be
decided in polynomial time for every network whose constraints all
belong to the set. The question is always about a *subset*, because the
problem for the full algebra is NP-complete. The point algebra is an
example of a tractable algebra, even in full (Vilain and Kautz, 1986).
The ORD-Horn subalgebra H is another, for Allen’s algebra, and for it
path consistency decides consistency (Nebel and Bürckert, 1995). So, to
reason about intervals, one can use H and obtain answers in cubic time.

**Maximal.** Larger tractable sets are better, since they can say more.
A tractable set is **maximal** if no tractable set properly contains it;
equivalently, if adding *any* RelSet to it makes the problem NP-hard
(assuming that P is not NP). *Maximal* is not the same as *largest*: a
set can be maximal without being the biggest one, and an algebra can
have several maximal tractable subalgebras. Nebel and Bürckert (1995)
proved that H is maximal, and in fact that it is the *only* maximal
tractable subalgebra that contains all 13 basic relations. Krokhin,
Jeavons and Jonsson (2003) found *all* of the maximal tractable
subalgebras of Allen’s algebra, 18 of them including H.

The significance of **B|BI** in Section 4 is that it is *not* in H.
Adding it to H, and taking the closure, gives a strictly larger
subalgebra, and, by the maximality of H, reasoning with it is NP-hard:

.. code:: ipython3

    bigger = allen.closure(ord_horn | {allen.relset("B|BI")})
    print(f"closure(H and B|BI) has {len(bigger)} RelSets, against {len(ord_horn)} for H.")
    print(f"It contains H: {ord_horn <= bigger}")
    print("By the maximality of H [Nebel and Bürckert, 1995], consistency for networks over this larger subalgebra is NP-hard.")


.. parsed-literal::

    closure(H and B|BI) has 1063 RelSets, against 868 for H.
    It contains H: True
    By the maximality of H [Nebel and Bürckert, 1995], consistency for networks over this larger subalgebra is NP-hard.


**What qualreas can and cannot establish.** Closure, the three families,
path consistency and the search of the next section are computations.
They can **verify** that a family is closed, and they can **refute** the
claim that path consistency decides a subalgebra. They cannot, by
themselves, show that a subalgebra is tractable or NP-hard; those are
theorems. The next notebook is careful about that, and so should be any
use of it.

8. Searching for Tractable Subalgebras: Refuted Subalgebras 
------------------------------------------------------------

Here is a way to look for tractable subalgebras outside H. If path
consistency **decides** a subalgebra, which means that every path
consistent network built from its RelSets is consistent, then the
subalgebra is tractable, because path consistency takes cubic time. This
is a sufficient condition for tractability, but not a necessary one.

``Algebra.check_path_consistency`` goes looking for the opposite: a
network, built from the RelSets of a subalgebra, that is **path
consistent but inconsistent**, exactly like the four-node network of
Section 6. The subalgebra is given by generators, from which ``closure``
makes the subalgebra. The result is a record with these fields:

+------------------------------+---------------------------------------+
| Field                        | Meaning                               |
+==============================+=======================================+
| ``refuted``                  | ``True`` if a counterexample was      |
|                              | found                                 |
+------------------------------+---------------------------------------+
| ``counterexample``           | the network that is path consistent   |
|                              | but inconsistent, or ``None``         |
+------------------------------+---------------------------------------+
| ``nodes``                    | its number of nodes                   |
+------------------------------+---------------------------------------+
| ``exhaustive``, ``sampled``  | the sizes of network for which        |
|                              | *every* network was tried, and those  |
|                              | for which only a *random sample* was  |
+------------------------------+---------------------------------------+
| ``checked``                  | the number of path consistent         |
|                              | networks that were tested             |
+------------------------------+---------------------------------------+

Two terms describe what comes out. *Refuted* is *qualreas*\ ’s own word,
taken from the field above, and *refuted but tractable* builds on it.

- A subalgebra is **refuted** if a counterexample was found. The
  counterexample is a **certificate**: anyone can check it with
  ``path_consistency`` and ``is_consistent``, as in Section 6. A
  refutation is *conclusive*, and it says that path consistency is
  **not** what makes the subalgebra tractable, if it is tractable at
  all. A subalgebra that is inside H can never be refuted, since H is
  decided by path consistency.
- A subalgebra that is **not refuted** is only a *candidate*. The search
  covers networks of up to a given size, and it samples when there are
  too many to try, so failing to find a counterexample is *evidence*,
  not proof. Counterexamples can need many nodes. The notebook that
  follows shows an example that a modest search does not find, and a
  larger one does.

There is a third possibility to keep in mind, and it is why the phrase
**refuted but tractable** is used. A refuted subalgebra might still be
tractable, because *some other algorithm*, one that does more than path
consistency, might decide it. Refutation removes one explanation of
tractability; it does not show intractability. That is why the search is
a *filter*: it removes candidates, and what is left must be investigated
by other means, such as comparing with the 18 maximal tractable
subalgebras of Krokhin, Jeavons and Jonsson (2003).

A first look, on four sets of generators. The search here is a modest
one: networks of up to 5 nodes, and 150 random walks for each size of
network that is too large to try exhaustively. Two of the subalgebras,
those generated by ``B|M`` and by ``SI|F``, are not refuted (the first
is inside H, so we know that it cannot be); the other two are refuted. A
different number of walks, or a different ``seed``, can change which
ones are refuted, as the next notebook shows.

.. code:: ipython3

    candidates = [["B|M"], ["SI|F"], ["F|B|MI|SI|OI"], ["B|F|OI"]]
    
    print(f"{'generators':16} {'size':>5} {'inside H':>9}   result of the search (up to 5 nodes)")
    for generators in candidates:
        subalgebra = allen.closure([allen.relset(g) for g in generators])
        check = allen.check_path_consistency(generators, nodes=5, walks=150)
        result = f"refuted, with a counterexample of {check.nodes} nodes" if check.refuted else "not refuted (a candidate)"
        print(f"{'; '.join(generators):16} {len(subalgebra):5d} {str(subalgebra <= ord_horn):>9}   {result}")


.. parsed-literal::

    generators        size  inside H   result of the search (up to 5 nodes)
    B|M                  6      True   not refuted (a candidate)
    SI|F                 9     False   not refuted (a candidate)
    F|B|MI|SI|OI         5     False   refuted, with a counterexample of 5 nodes
    B|F|OI               7     False   refuted, with a counterexample of 5 nodes


Here is the counterexample for the third one, the subalgebra generated
by **F|B|MI|SI|OI**, checked in the same three ways as the network of
Section 6:

.. code:: ipython3

    check = allen.check_path_consistency(["F|B|MI|SI|OI"])
    print(check)
    print()
    print(f"exhaustive: {check.exhaustive}   sampled: {check.sampled}   path consistent networks tested: {check.checked}")
    print()
    net = {pair: relset for pair, relset in check.counterexample.items() if relset != allen.elements}
    print("the counterexample (pairs that are not shown are unconstrained):")
    for pair, relset in net.items():
        print(f"  {pair}: {relset}")
    print()
    print("path consistent:", is_path_consistent(net, check.nodes))
    print("consistent     :", allen.is_consistent(net, nodes=check.nodes))


.. parsed-literal::

    Path consistency does not decide this subalgebra (5 relation sets): a path consistent network of 5 nodes that is not consistent was found.
    
    exhaustive: (4,)   sampled: ()   path consistent networks tested: 5174
    
    the counterexample (pairs that are not shown are unconstrained):
      (0, 1): BI|FI|M|O|S
      (0, 2): B|F|MI|OI|SI
      (0, 3): B|F|MI|OI|SI
      (0, 4): BI|FI|M|O|S
      (1, 2): B|F|MI|OI|SI
      (1, 3): BI|FI|M|O|S
      (1, 4): BI|FI|M|O|S
      (2, 3): BI|FI|M|O|S
      (2, 4): B|F|MI|OI|SI
      (3, 4): BI|FI|M|O|S
    
    path consistent: True
    consistent     : False


This subalgebra is **refuted**. Whether it is tractable by some other
method is a different question, which this notebook does not try to
answer. The subalgebras that are *not* refuted, and are not inside H,
are the interesting ones, and the next notebook shows how to take them
further. You have the vocabulary to read it now.

Glossary 
---------

+------------------+-------------------------------+--------------------------+
| Term             | Meaning                       | Section                  |
+==================+===============================+==========================+
| **algebraic      | Another name for *path        | 3, 6                     |
| closure**        | consistency* (Ladkin and      |                          |
|                  | Maddux, 1994). Not the same   |                          |
|                  | as ``Algebra.closure``.       |                          |
+------------------+-------------------------------+--------------------------+
| **atom**         | See *basic relation*.         | 1                        |
+------------------+-------------------------------+--------------------------+
| **basic          | One of the relations from     | 1                        |
| relation**       | which an algebra is built (13 |                          |
|                  | in Allen’s algebra; 3 in the  |                          |
|                  | point algebra).               |                          |
+------------------+-------------------------------+--------------------------+
| **certificate**  | Evidence that can be checked  | 6, 7, 8                  |
|                  | quickly: a path consistent    |                          |
|                  | singleton labeling shows that |                          |
|                  | a network is consistent; a    |                          |
|                  | path consistent but           |                          |
|                  | inconsistent network refutes  |                          |
|                  | a subalgebra.                 |                          |
+------------------+-------------------------------+--------------------------+
| **clause**       | A disjunction of atomic       | 4                        |
|                  | formulas about end points.    |                          |
+------------------+-------------------------------+--------------------------+
| **closed (under  | Applying the operation to     | 3                        |
| an operation)**  | members always gives a        |                          |
|                  | member.                       |                          |
+------------------+-------------------------------+--------------------------+
| **closure**      | The smallest subalgebra that  | 3                        |
|                  | contains a given collection   |                          |
|                  | of RelSets:                   |                          |
|                  | ``Algebra.closure``.          |                          |
+------------------+-------------------------------+--------------------------+
| **composition**  | R ; S: the relations that can | 2                        |
|                  | hold between X and Z, if X R  |                          |
|                  | Y and Y S Z.                  |                          |
+------------------+-------------------------------+--------------------------+
| **conjunction**  | An *and*. A network is a      | 1, 4                     |
|                  | conjunction of constraints.   |                          |
+------------------+-------------------------------+--------------------------+
| **consistent**   | A network is consistent if    | 5                        |
|                  | some choice of entities       |                          |
|                  | satisfies every constraint.   |                          |
+------------------+-------------------------------+--------------------------+
| **converse**     | R⁻¹: if X R Y then Y R⁻¹ X.   | 2                        |
+------------------+-------------------------------+--------------------------+
| **convex**       | A RelSet described by a       | 4                        |
|                  | conjunction of ``<``, ``<=``  |                          |
|                  | and ``=`` formulas on end     |                          |
|                  | points (no ``!=``); in the    |                          |
|                  | point algebra, one with no    |                          |
|                  | gaps.                         |                          |
+------------------+-------------------------------+--------------------------+
| **decidable /    | A question is decidable if an | 7                        |
| decides**        | algorithm always finishes     |                          |
|                  | with the right answer. A      |                          |
|                  | method *decides* a class of   |                          |
|                  | inputs if it is always right  |                          |
|                  | on it.                        |                          |
+------------------+-------------------------------+--------------------------+
| **disjunction**  | An *or*. A RelSet is a        | 1, 4                     |
|                  | disjunction of basic          |                          |
|                  | relations.                    |                          |
+------------------+-------------------------------+--------------------------+
| **generates /    | A set of RelSets generates a  | 3                        |
| generators**     | subalgebra when its closure   |                          |
|                  | is that subalgebra; its       |                          |
|                  | members are generators.       |                          |
+------------------+-------------------------------+--------------------------+
| **inconsistent** | Not consistent: no choice of  | 5                        |
|                  | entities satisfies every      |                          |
|                  | constraint.                   |                          |
+------------------+-------------------------------+--------------------------+
| **intersection** | R + S: the relations in both. | 2                        |
+------------------+-------------------------------+--------------------------+
| **maximal**      | A tractable set is maximal if | 7                        |
|                  | no tractable set properly     |                          |
|                  | contains it (adding any       |                          |
|                  | RelSet makes reasoning        |                          |
|                  | NP-hard, unless P = NP).      |                          |
+------------------+-------------------------------+--------------------------+
| **NP**           | The questions whose *yes*     | 7                        |
|                  | answers have certificates     |                          |
|                  | that can be checked in        |                          |
|                  | polynomial time.              |                          |
+------------------+-------------------------------+--------------------------+
| **NP-complete**  | NP-hard and in NP.            | 7                        |
+------------------+-------------------------------+--------------------------+
| **NP-hard**      | At least as hard as every     | 7                        |
|                  | problem in NP; no             |                          |
|                  | polynomial-time algorithm     |                          |
|                  | exists unless P = NP.         |                          |
+------------------+-------------------------------+--------------------------+
| **ORD-Horn       | A clause with any number of   | 4                        |
| clause**         | ``p != q`` and at most one    |                          |
|                  | formula of the forms          |                          |
|                  | ``p < q``, ``p <= q``,        |                          |
|                  | ``p = q``.                    |                          |
+------------------+-------------------------------+--------------------------+
| **ORD-Horn       | The RelSets described by      | 4, 7                     |
| subalgebra (H)** | conjunctions of ORD-Horn      |                          |
|                  | clauses: 868 RelSets in       |                          |
|                  | Allen’s algebra, a tractable  |                          |
|                  | and maximal subalgebra.       |                          |
+------------------+-------------------------------+--------------------------+
| **P**            | The questions that can be     | 7                        |
|                  | decided in polynomial time.   |                          |
+------------------+-------------------------------+--------------------------+
| **path           | Repeating C(i,k) = C(i,k) +   | 6                        |
| consistency**    | (C(i,j) ; C(j,k)) until       |                          |
|                  | nothing changes:              |                          |
|                  | ``Algebra.path_consistency``. |                          |
+------------------+-------------------------------+--------------------------+
| **path           | A network that path           | 6                        |
| consistent but   | consistency leaves alone,     |                          |
| inconsistent**   | though it has no solution.    |                          |
+------------------+-------------------------------+--------------------------+
| **pointisable**  | A RelSet described by a       | 4                        |
|                  | conjunction of ``<``, ``<=``, |                          |
|                  | ``=`` and ``!=`` formulas on  |                          |
|                  | end points.                   |                          |
+------------------+-------------------------------+--------------------------+
| **polynomial     | Running time bounded by a     | 7                        |
| time**           | polynomial in the size of the |                          |
|                  | input, such as n³.            |                          |
+------------------+-------------------------------+--------------------------+
| **refuted        | One for which a path          | 8                        |
| (subalgebra)**   | consistent but inconsistent   |                          |
|                  | network was found: path       |                          |
|                  | consistency does not decide   |                          |
|                  | it.                           |                          |
+------------------+-------------------------------+--------------------------+
| **refuted but    | A refuted subalgebra that is  | 8                        |
| tractable**      | nonetheless tractable, by     |                          |
|                  | some other algorithm.         |                          |
+------------------+-------------------------------+--------------------------+
| **RelSet**       | A set of basic relations,     | 1                        |
|                  | read as a disjunction.        |                          |
+------------------+-------------------------------+--------------------------+
| **scenario /     | A choice of one basic         | 5                        |
| singleton        | relation for each pair of     |                          |
| labeling**       | nodes; a scenario is one that |                          |
|                  | is consistent.                |                          |
+------------------+-------------------------------+--------------------------+
| **solution**     | A choice of entities          | 5                        |
|                  | (intervals, for example) that |                          |
|                  | satisfies every constraint.   |                          |
+------------------+-------------------------------+--------------------------+
| **subalgebra**   | A collection of RelSets       | 3                        |
|                  | closed under intersection,    |                          |
|                  | converse and composition.     |                          |
+------------------+-------------------------------+--------------------------+
| **tractable      | A set of RelSets for which    | 7                        |
| algebra**        | consistency can be decided in |                          |
|                  | polynomial time.              |                          |
+------------------+-------------------------------+--------------------------+
| **universal      | The RelSet of all basic       | 1                        |
| RelSet**         | relations: no information.    |                          |
+------------------+-------------------------------+--------------------------+

Exercises 
----------

1. Find the closure of :math:`\{B|M\}` in Allen’s algebra, and list it.
   Is it inside H? (There are six RelSets.)
2. Use ``relset_of`` to find the RelSet described by “X starts before Y
   starts, and X ends before Y ends”. Is it convex? Then check whether
   **M|MI** is in H, and say what that means for the statements that
   could describe it.
3. The closure of :math:`\{<, =, >, <|=\}` in the point algebra has
   seven RelSets, and the closure of :math:`\{<|=, >|=\}` has four. Find
   a single generator whose closure has exactly two RelSets, and explain
   why it has only two.
4. Explain why a network of only **three** nodes cannot be path
   consistent but inconsistent in Allen’s algebra. (Hint: choose any
   basic relation from the constraint on (i, k). Where must it have come
   from? Then see what that means for a triple of single relations.)
5. Run
   ``allen.check_path_consistency(["B|DI|OI"], nodes=5, walks=150)``,
   and then again with ``nodes=6, walks=1000``. What changes, and what
   does it say about how to read a search that finds nothing?

References 
-----------

1.  `[Allen, 1983] “Maintaining Knowledge about Temporal Intervals” by
    James F.
    Allen <https://cse.unl.edu/~choueiry/Documents/Allen-CACM1983.pdf>`__,
    *Communications of the ACM* 26(11), 832-843 - Allen’s original paper
    (PDF): the 13 relations, composition, and constraint propagation.
2.  [Cook, 1971] “The Complexity of Theorem-Proving Procedures” by
    Stephen A. Cook, *Proceedings of the 3rd Annual ACM Symposium on
    Theory of Computing*, 151-158 - the first NP-completeness result.
3.  [Freuder, 1978] “Synthesizing Constraint Expressions” by Eugene C.
    Freuder, *Communications of the ACM* 21(11), 958-966 - strong
    k-consistency, of which path consistency is the case k = 3.
4.  [Garey and Johnson, 1979] *Computers and Intractability: A Guide to
    the Theory of NP-Completeness* by Michael R. Garey and David S.
    Johnson, W. H. Freeman - the standard textbook for P, NP, NP-hard
    and NP-complete.
5.  [Golumbic and Shamir, 1993] “Complexity and Algorithms for Reasoning
    about Time: A Graph-Theoretic Approach” by Martin C. Golumbic and
    Ron Shamir, *Journal of the ACM* 40(5), 1108-1133 - complexity of
    interval reasoning problems; some of its examples are in the
    notebook *Golumbic_and_Shamir_1993_Examples*.
6.  `[Krokhin, Jeavons and Jonsson, 2003] “Reasoning about Temporal
    Relations: The Tractable Subalgebras of Allen’s Interval Algebra” by
    Andrei Krokhin, Peter Jeavons and Peter
    Jonsson <https://www.cs.ox.ac.uk/publications/publication1679-abstract.html>`__,
    *Journal of the ACM* 50(5), 591-640 - finds all of the maximal
    tractable subalgebras of Allen’s algebra.
7.  `[Ladkin and Maddux, 1994] “On Binary Constraint Problems” by Peter
    B. Ladkin and Roger D.
    Maddux <https://projects.csail.mit.edu/jacm/References/ladkinm1994:435.html>`__,
    *Journal of the ACM* 41(3), 435-469 - algebraic closure; includes
    the result that a path consistent network of single relations in
    Allen’s algebra can be realized by intervals.
8.  `[Ligozat, 1991] “On Generalized Interval Calculi” by Gérard
    Ligozat <https://mlanthology.org/aaai/1991/ligozat1991aaai-generalized>`__,
    *Proceedings of the 9th National Conference on Artificial
    Intelligence (AAAI-91)*, 234-240 - convex relations, and a geometric
    view of the subalgebras of interval calculi.
9.  [Mackworth, 1977] “Consistency in Networks of Relations” by Alan K.
    Mackworth, *Artificial Intelligence* 8(1), 99-118 - arc and path
    consistency for constraint networks.
10. [Montanari, 1974] “Networks of Constraints: Fundamental Properties
    and Applications to Picture Processing” by Ugo Montanari,
    *Information Sciences* 7, 95-132 - the origin of path consistency.
11. `[Nebel and Bürckert, 1995] “Reasoning about Temporal Relations: A
    Maximal Tractable Subclass of Allen’s Interval Algebra” by Bernhard
    Nebel and Hans-Jürgen
    Bürckert <https://www.dfki.de/web/forschung/projekte-publikationen/publikation/1836>`__,
    *Journal of the ACM* 42(1), 43-66 - defines the ORD-Horn subalgebra,
    H, shows that path consistency decides it, and proves that it is the
    largest tractable set of relations that contains all of the basic
    relations.
12. `[Randell, Cui and Cohn, 1992] “A Spatial Logic Based on Regions and
    Connection” <https://en.wikipedia.org/wiki/Region_connection_calculus>`__
    by David A. Randell, Zhan Cui and Anthony G. Cohn, *Proceedings of
    the 3rd International Conference on Principles of Knowledge
    Representation and Reasoning (KR-92)*, 165-176 - RCC8 (the link is
    the Wikipedia article on the Region Connection Calculus).
13. `[Reich, 1994] “Intervals, Points, and Branching Time” by A. J.
    Reich <https://www.researchgate.net/publication/220810644_Intervals_Points_and_Branching_Time>`__
    - the basis for the point and branching time extensions of Allen’s
    algebra in *qualreas*.
14. `[Renz and Nebel, 1999] “On the Complexity of Qualitative Spatial
    Reasoning: A Maximal Tractable Fragment of the Region Connection
    Calculus” by Jochen Renz and Bernhard
    Nebel <https://researchportalplus.anu.edu.au/en/publications/on-the-complexity-of-qualitative-spatial-reasoning-a-maximal-trac/>`__,
    *Artificial Intelligence* 108(1-2), 69-123 - the same questions as
    in this notebook, for RCC8.
15. `[Renz and Nebel, 2007] “Qualitative Spatial Reasoning Using
    Constraint Calculi” by Jochen Renz and Bernhard
    Nebel <https://researchportalplus.anu.edu.au/en/publications/qualitative-spatial-reasoning-using-constraint-calculi/>`__,
    in *Handbook of Spatial Logics*, Springer, 161-215 - a survey that
    covers consistency, path consistency, tractable classes and maximal
    tractable classes.
16. `[van Beek, 1992] “Reasoning about Qualitative Temporal Information”
    by Peter van
    Beek <https://cs.uwaterloo.ca/~vanbeek/Publications/vanbeek_abs.html>`__,
    *Artificial Intelligence* 58(1-3), 297-326 - the point algebra and
    Allen’s algebra, and the algorithms for them. (The link is to the
    author’s PhD thesis, which is closely related.)
17. `[van Beek and Cohen, 1990] “Exact and Approximate Reasoning about
    Temporal Relations” by Peter van Beek and Robin
    Cohen <https://cs.uwaterloo.ca/~vanbeek/Publications/ci90.pdf>`__,
    *Computational Intelligence* 6, 132-144 - exact and approximate
    reasoning in Allen’s algebra.
18. `[Vilain and Kautz, 1986] “Constraint Propagation Algorithms for
    Temporal Reasoning” by Marc B. Vilain and Henry A.
    Kautz <https://mlanthology.org/aaai/1986/vilain1986aaai-constraint>`__,
    *Proceedings of the 5th National Conference on Artificial
    Intelligence (AAAI-86)*, 377-382 - the point algebra and the
    intractability of the interval algebra.
19. [Vilain, Kautz and van Beek, 1990] “Constraint Propagation
    Algorithms for Temporal Reasoning: A Revised Report” by Marc Vilain,
    Henry Kautz and Peter van Beek, in *Readings in Qualitative
    Reasoning about Physical Systems*, Morgan Kaufmann, 373-381 -
    corrects and extends [Vilain and Kautz, 1986].

**Next:** *subalgebras_of_allens_algebra*, which uses all of these
terms.
