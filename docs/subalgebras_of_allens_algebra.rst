Subalgebras of Allen’s Algebra Defined by Point Relations
=========================================================

Allen’s algebra of proper time intervals has 13 basic relations, but the
algebra itself is really made of all :math:`2^{13} = 8192` sets of those
relations, each of which is represented in qualreas by a RelSet. A
subalgebra is a collection of RelSets that is closed under the algebra’s
operations: intersection, converse, and composition. Some subalgebras
are important because reasoning with their relation sets is tractable,
whereas reasoning with arbitrary RelSets is NP-hard.

This notebook shows how to use qualreas to generate three well-known
subalgebras of Allen’s algebra, the convex, pointisable, and ORD-Horn
relation sets, and how Algebra.closure is used with them. In particular,
it shows that the ORD-Horn subalgebra, H, of [Nebel and Bürckert, 1995]
can be generated from the 13 basic relations together with a single
additional RelSet.

The notebook has three parts: 1. The families are defined, using
formulas about the end points of the two intervals. This is done by the
functions convex_relsets, pointisable_relsets and ord_horn_relsets. 1.
Algebra.closure is used to verify that each family is closed under
intersection, converse and composition. 1. Algebra.closure is used to
generate H from a small set of RelSets.

One caution up front. Computing a closure tells us what the smallest
subalgebra containing some RelSets is. It does not tell us whether the
result is tractable. The tractability of H, and the fact that no larger
set of RelSets that contains the basic relations is tractable, are
theorems in [Nebel and Bürckert, 1995]; they are not something qualreas
establishes (yet).

Table of Contents
-----------------

- `Imports and the Algebra <#imports>`__
- `Relations are Orderings of End Points <#endpoints>`__
- `Three Families of Relation Sets <#families>`__

  - `Examples <#examples>`__

- `Checking that the Families are Subalgebras <#closed>`__
- `Generating the ORD-Horn Subalgebra <#generating>`__
- `The Point Algebra <#point_algebra>`__
- `References <#refs>`__

Imports and the Algebra 
------------------------

.. code:: ipython3

    import os
    import qualreas as qr
    
    allen = qr.Algebra(os.path.join(qr.ALGEBRA_DIR, "Linear_Interval_Algebra.json"))
    
    print(allen)
    print(f"{len(allen.elements)} basic relations: {allen.elements}")


.. parsed-literal::

    <Linear_Interval_Algebra: Allen's algebra of proper time intervals>
    13 basic relations: B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI


A small helper, to print a collection of RelSets from the smallest to
the largest:

.. code:: ipython3

    def show(relsets, limit=None):
        ordered = sorted(relsets, key=lambda rs: (len(rs.members()), str(rs)))
        for rs in ordered[:limit]:
            print(str(rs) or "{} (the empty RelSet)")

Relations are Orderings of End Points 
--------------------------------------

A relation of Allen’s algebra relates two proper intervals, X = (s1, e1)
and Y = (s2, e2), where s1 < e1 and s2 < e2. Each of the 13 basic
relations is one of the 13 possible ways to order the four end points.
So a RelSet is a set of such orderings, and a formula about the end
points, such as “e1 <= s2”, describes the set of orderings that satisfy
it.

The function endpoint_orderings gives the ordering for each relation.
The end points are numbered 0 to 3, for s1, e1, s2 and e2, and each
ordering gives the point relation between each pair (i, j), i < j, of
end points. The orderings come from the same table that qualreas uses to
derive interval algebras from point algebras.

.. code:: ipython3

    orderings = qr.endpoint_orderings(allen)
    
    for name in ["B", "M", "O", "S", "D", "E"]:
        print(f"{name:>2}: {orderings[name]}")


.. parsed-literal::

     B: {(0, 1): '<', (2, 3): '<', (0, 2): '<', (0, 3): '<', (1, 2): '<', (1, 3): '<'}
     M: {(0, 1): '<', (2, 3): '<', (0, 2): '<', (0, 3): '<', (1, 2): '=', (1, 3): '<'}
     O: {(0, 1): '<', (2, 3): '<', (0, 2): '<', (0, 3): '<', (1, 2): '>', (1, 3): '<'}
     S: {(0, 1): '<', (2, 3): '<', (0, 2): '=', (0, 3): '<', (1, 2): '>', (1, 3): '<'}
     D: {(0, 1): '<', (2, 3): '<', (0, 2): '>', (0, 3): '<', (1, 2): '>', (1, 3): '<'}
     E: {(0, 1): '<', (2, 3): '<', (0, 2): '=', (0, 3): '<', (1, 2): '>', (1, 3): '='}


For example, M (Meets) has (1, 2): ‘=’, which says that e1 = s2, and D
(During) has (0, 2): ‘>’ and (1, 3): ‘<’, which say that s1 > s2 and e1
< e2.

Three Families of Relation Sets 
--------------------------------

Each family is the set of RelSets that can be described by a certain
kind of formula about the end points:

+-----------------+---------------------+------------------------------+
| Family          | Function            | Described by                 |
+=================+=====================+==============================+
| Convex          | convex_relsets      | A conjunction of formulas of |
|                 |                     | the forms p < q, p <= q and  |
|                 |                     | p = q                        |
+-----------------+---------------------+------------------------------+
| Pointisable     | pointisable_relsets | A conjunction of formulas of |
|                 |                     | those forms and also p != q  |
+-----------------+---------------------+------------------------------+
| ORD-Horn (H)    | ord_horn_relsets    | A conjunction of ORD-Horn    |
|                 |                     | clauses: disjunctions of     |
|                 |                     | formulas that have any       |
|                 |                     | number of p != q, but at     |
|                 |                     | most one of the forms p < q, |
|                 |                     | p <= q and p = q             |
+-----------------+---------------------+------------------------------+

where p and q are any two of the four end points. Every convex RelSet is
pointisable, and every pointisable RelSet is ORD-Horn. Each function
takes an algebra, and returns a frozenset of RelSets. The empty RelSet,
and the RelSet with all 13 relations, are in every family.

.. code:: ipython3

    convex = qr.convex_relsets(allen)
    pointisable = qr.pointisable_relsets(allen)
    ord_horn = qr.ord_horn_relsets(allen)
    
    print(f"Convex:      {len(convex):4d} RelSets")
    print(f"Pointisable: {len(pointisable):4d} RelSets")
    print(f"ORD-Horn:    {len(ord_horn):4d} RelSets   (out of {2**13})")
    print()
    print(f"Convex is inside Pointisable: {convex < pointisable}")
    print(f"Pointisable is inside ORD-Horn: {pointisable < ord_horn}")


.. parsed-literal::

    Convex:        83 RelSets
    Pointisable:  188 RelSets
    ORD-Horn:     868 RelSets   (out of 8192)
    
    Convex is inside Pointisable: True
    Pointisable is inside ORD-Horn: True


The size of H, 868, is the number proved in [Nebel and Bürckert, 1995].
The convex relations are usually counted as 82, which is 83 here because
the empty RelSet is counted. Here is how many RelSets in H there are
with each number of basic relations:

.. code:: ipython3

    from collections import Counter
    
    by_size = Counter(len(rs.members()) for rs in ord_horn)
    for size in sorted(by_size):
        print(f"{size:2d} basic relations: {by_size[size]:3d} RelSets")


.. parsed-literal::

     0 basic relations:   1 RelSets
     1 basic relations:  13 RelSets
     2 basic relations:  28 RelSets
     3 basic relations:  52 RelSets
     4 basic relations:  83 RelSets
     5 basic relations:  99 RelSets
     6 basic relations:  98 RelSets
     7 basic relations: 108 RelSets
     8 basic relations: 130 RelSets
     9 basic relations: 126 RelSets
    10 basic relations:  84 RelSets
    11 basic relations:  36 RelSets
    12 basic relations:   9 RelSets
    13 basic relations:   1 RelSets


Examples 
~~~~~~~~~

Here are a few RelSets, and the families that they belong to. The last
column says what the RelSet means in terms of end points.

.. code:: ipython3

    examples = [("B|M",  "e1 <= s2"),
                ("S|SI", "s1 = s2 and e1 != e2"),
                ("B|BI", "e1 < s2 or e2 < s1"),
                ("D|DI", "(s2 < s1 and e1 < e2) or (s1 < s2 and e2 < e1)"),
                ("M|MI", "e1 = s2 or e2 = s1")]
    
    print(f"{'RelSet':8} {'convex':>7} {'pointisable':>12} {'ORD-Horn':>9}   meaning")
    for text, meaning in examples:
        rs = allen.relset(text)
        print(f"{text:8} {str(rs in convex):>7} {str(rs in pointisable):>12} {str(rs in ord_horn):>9}   {meaning}")


.. parsed-literal::

    RelSet    convex  pointisable  ORD-Horn   meaning
    B|M         True         True      True   e1 <= s2
    S|SI       False         True      True   s1 = s2 and e1 != e2
    B|BI       False        False     False   e1 < s2 or e2 < s1
    D|DI       False        False     False   (s2 < s1 and e1 < e2) or (s1 < s2 and e2 < e1)
    M|MI       False        False     False   e1 = s2 or e2 = s1


B|BI (“X is before Y or after Y”, i.e., the two intervals do not overlap
or touch) is not in H, because its formula has two “<” formulas in one
clause, so it is not Horn. By the maximality of H [Nebel and Bürckert,
1995], adding it to the basic relations makes reasoning NP-hard.

H is not closed under union, even though it is closed under the other
three operations. B and BI are both in H, but their union is not:

.. code:: ipython3

    b, bi = allen.relset("B"), allen.relset("BI")
    
    print(f"B in H: {b in ord_horn}    BI in H: {bi in ord_horn}    B|BI in H: {b.union(bi) in ord_horn}")


.. parsed-literal::

    B in H: True    BI in H: True    B|BI in H: False


Checking that the Families are Subalgebras 
-------------------------------------------

A collection of RelSets is a subalgebra when it is closed under
intersection, converse and composition. For such a collection, the
closure of the collection is the collection itself. Algebra.closure
takes a collection of RelSets and returns the smallest collection that
contains them and is closed under those three operations:

.. code:: ipython3

    for name, family in [("Convex", convex), ("Pointisable", pointisable), ("ORD-Horn", ord_horn)]:
        closure = allen.closure(family)
        print(f"{name:12} closure has {len(closure):4d} RelSets; it equals the family: {closure == family}")


.. parsed-literal::

    Convex       closure has   83 RelSets; it equals the family: True
    Pointisable  closure has  188 RelSets; it equals the family: True
    ORD-Horn     closure has  868 RelSets; it equals the family: True


So each of the three families is a subalgebra of Allen’s algebra.

Generating the ORD-Horn Subalgebra 
-----------------------------------

We can also go the other way, starting from a few RelSets and using
closure to generate a subalgebra. A natural place to start is the 13
basic relations, each taken as a RelSet with one relation in it:

.. code:: ipython3

    basics = [allen.relset([rel]) for rel in allen.elements]
    
    generated = allen.closure(basics)
    
    print(f"The closure of the 13 basic relations has {len(generated)} RelSets.")
    print(f"It is inside H: {generated <= ord_horn}")
    print()
    show(generated - set(basics))


.. parsed-literal::

    The closure of the 13 basic relations has 30 RelSets.
    It is inside H: True
    
    {} (the empty RelSet)
    BI|MI|OI
    B|M|O
    DI|FI|O
    DI|OI|SI
    D|F|OI
    D|O|S
    E|F|FI
    E|S|SI
    BI|DI|MI|OI|SI
    BI|D|F|MI|OI
    B|DI|FI|M|O
    B|D|M|O|S
    D|DI|E|F|FI|O|OI|S|SI
    BI|D|DI|E|F|FI|MI|O|OI|S|SI
    B|D|DI|E|F|FI|M|O|OI|S|SI
    B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI


That is far fewer than the 868 RelSets in H. Besides the 13 basic
relations, the closure has the empty RelSet and 16 other RelSets that
come from combining the basic relations (for example, composing B with D
gives B|D|M|O|S). H also has RelSets that this never produces, such as
S|SI.

What is missing? Here is a search: for each RelSet in H that was not
generated, add it to the 13 basic relations and see whether the closure
is then all of H.

.. code:: ipython3

    missing = sorted(ord_horn - generated, key=lambda rs: (len(rs.members()), str(rs)))
    
    completing = [rs for rs in missing if allen.closure(basics + [rs]) == ord_horn]
    
    print(f"{len(missing)} RelSets of H are not in the closure of the basic relations.")
    print(f"{len(completing)} of them, added to the basic relations, generate all of H.")
    print()
    smallest = min(len(rs.members()) for rs in completing)
    print(f"The ones with the fewest relations ({smallest} each):")
    show([rs for rs in completing if len(rs.members()) == smallest])


.. parsed-literal::

    838 RelSets of H are not in the closure of the basic relations.
    60 of them, added to the basic relations, generate all of H.
    
    The ones with the fewest relations (7 each):
    BI|D|DI|E|FI|O|OI
    BI|D|DI|E|M|O|OI
    BI|D|DI|E|O|OI|S
    B|D|DI|E|F|O|OI
    B|D|DI|E|MI|O|OI
    B|D|DI|E|O|OI|SI


So a single additional RelSet is enough. Using the first one:

.. code:: ipython3

    extra = allen.relset("B|D|DI|E|F|O|OI")
    
    h = allen.closure(basics + [extra])
    
    print(f"closure(13 basic relations + {extra}) has {len(h)} RelSets.")
    print(f"It equals the ORD-Horn subalgebra, H: {h == ord_horn}")


.. parsed-literal::

    closure(13 basic relations + B|D|DI|E|F|O|OI) has 868 RelSets.
    It equals the ORD-Horn subalgebra, H: True


Note that the RelSet, B|D|DI|E|F|O|OI, was found by this search; it was
not derived from theory. For comparison, a RelSet that is not in H
generates a different subalgebra, one that is not inside H:

.. code:: ipython3

    outside = allen.relset("B|BI")
    larger = allen.closure(basics + [outside])
    
    print(f"closure(13 basic relations + {outside}) has {len(larger)} RelSets.")
    print(f"It equals H: {larger == ord_horn}")
    print(f"It is inside H: {larger <= ord_horn}   ({outside} is in it, but not in H)")


.. parsed-literal::

    closure(13 basic relations + B|BI) has 317 RelSets.
    It equals H: False
    It is inside H: False   (B|BI is in it, but not in H)


The Point Algebra 
------------------

The same kind of experiment works for the point algebra,
Linear_Point_Algebra, which has just three basic relations, <, = and >,
and therefore only :math:`2^3 = 8` RelSets. (The functions that define
families from end points are only for interval algebras. Here we just
use closure.)

.. code:: ipython3

    points = qr.Algebra(os.path.join(qr.ALGEBRA_DIR, "Linear_Point_Algebra.json"))
    
    def closure_of(*relsets):
        print(f"closure of {{{', '.join(relsets)}}} has {len(points.closure(relsets))} RelSets:")
        show(points.closure(relsets))
        print()
    
    closure_of("<", "=", ">")
    closure_of("<", "=", ">", "<|=")
    closure_of("<", "=", ">", "<|>")


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
    


The first closure has the three basic relations, the empty RelSet and
the RelSet with all three relations. Adding “<=” gives the 7 RelSets
that need no “not equal” (</>), which are the convex RelSets of the
point algebra. Adding “!=” instead (that is, “<\|>”) gives 6. All 8
RelSets of the point algebra together are also a tractable algebra, so,
unlike Allen’s algebra, there is no smaller maximal tractable subalgebra
to look for.

References 
-----------

1. `[Allen, 1983] “Maintaining Knowledge about Temporal Intervals” by
   James F.
   Allen <https://cse.unl.edu/~choueiry/Documents/Allen-CACM1983.pdf>`__
   - Allen’s original paper (PDF)
2. [Nebel and Bürckert, 1995] “Reasoning about Temporal Relations: A
   Maximal Tractable Subclass of Allen’s Interval Algebra” by Bernhard
   Nebel and Hans-Jürgen Bürckert, Journal of the ACM 42(1) - defines
   the ORD-Horn subalgebra, H, and proves that it is the largest
   tractable set of relations that contains all of the basic relations
