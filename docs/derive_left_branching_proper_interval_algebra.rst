Derive Left-Branching Proper Interval Algebra
=============================================

NOTE: This algebra derivation restricts intervals to be proper
intervals, similar to Allen’s time interval algebra. So, time points are
not permitted. However, this algebra adds a new point relation,
incomparable, denoted by, l~, which expresses the relationship between
two points on different time branches. The transitivity/composition
table of the left-branching point algebra is defined so that time
branches from the left (i.e., out of the past). See the section, below,
titled, “Left-Branching Point Algebra”.

References
----------

1. `“Maintaining Knowledge about Temporal Intervals” by J.F.
   Allen <https://cse.unl.edu/~choueiry/Documents/Allen-CACM1983.pdf>`__
   - Allen’s original paper
2. `Allen’s Interval
   Algebra <https://www.ics.uci.edu/~alspaugh/cls/shr/allen.html>`__ or
   `here <https://thomasalspaugh.org/pub/fnd/allen.html>`__ - summarizes
   Allen’s algebra of proper time intervals
3. `“Intervals, Points, and Branching Time” by A.J.
   Reich <https://www.researchgate.net/publication/220810644_Intervals_Points_and_Branching_Time>`__
   - basis for the extensions here to Allen’s algebra
4. `W3C Time Ontology in OWL <https://www.w3.org/TR/owl-time/>`__ -
   temporal vocabulary used here is based on the W3C vocabulary of time
5. `bitsets Python
   package <https://bitsets.readthedocs.io/en/stable/>`__ - used to
   implement Algebra relation sets and operations
6. `NetworkX Python package <http://networkx.github.io/>`__ - used to
   represent directed graph of constraints
7. `Python format string
   syntax <https://docs.python.org/3/library/string.html#format-string-syntax>`__
   - used in Algebra summary method
8. `Spatial Ontology <https://www.w3.org/2017/sdwig/bp/>`__ - I’m still
   looking for a standard spatial vocabulary; maybe start here
9. `Qualitative Spatial Relations (QSR)
   Library <https://qsrlib.readthedocs.io/en/latest/index.html>`__ - an
   alternative library to the one defined here

Dependencies
------------

.. code:: ipython3

    import os
    import qualreas as qr
    import numpy as np
    
    import sys

.. code:: ipython3

    sys.setrecursionlimit(10000)

.. code:: ipython3

    path = os.path.join(os.getenv('PYPROJ'), 'qualreas')

Deriving the LB Proper Interval Algebra from LB Point Algebra
-------------------------------------------------------------

Left-Branching Point Algebra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    pt_alg = qr.Algebra(os.path.join(path, "Algebras/Left_Branching_Point_Algebra.json"))

.. code:: ipython3

    pt_alg.summary()


.. parsed-literal::

      Algebra Name: Left_Branching_Point_Algebra
       Description: Left-Branching Point Algebra
     Equality Rels: =
         Relations:
                NAME (SYMBOL)         CONVERSE (ABBREV)  REFLEXIVE  SYMMETRIC TRANSITIVE   DOMAIN        RANGE
               LessThan (  <)         GreaterThan (  >)    False      False       True         Pt            Pt
                 Equals (  =)              Equals (  =)     True       True       True         Pt            Pt
            GreaterThan (  >)            LessThan (  <)    False      False       True         Pt            Pt
           Incomparable ( l~)        Incomparable ( l~)    False       True      False         Pt            Pt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


.. code:: ipython3

    qr.print_point_algebra_composition_table(pt_alg)


.. parsed-literal::

    Left_Branching_Point_Algebra
    Elements: <, =, >, l~
    ==============================
     rel1 ; rel2 = composition
    ==============================
       <      <      <
       <      =      <
       <      >      <|=|>|l~
       <     l~      l~
    ------------------------------
       =      <      <
       =      =      =
       =      >      >
       =     l~      l~
    ------------------------------
       >      <      <|=|>
       >      =      >
       >      >      >
       >     l~      >|l~
    ------------------------------
      l~      <      <|l~
      l~      =      l~
      l~      >      l~
      l~     l~      <|=|>|l~
    ------------------------------


Derive Left-Branching Proper Interval Algebra as a Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The definition of less than, below, either restricts intervals to be
proper (‘<’) or allows intervals to be degenerate (‘=|<’) (i.e.,
integrates points and intervals).

.. code:: ipython3

    #less_than_rel = '=|<'
    less_than_rel = '<'

.. code:: ipython3

    lb_proper_alg_name="Derived_Left_Branching_Proper_Interval_Algebra"
    lb_proper_alg_desc="Extended left-branching proper interval algebra derived from point relations"
    
    %time test_lb_proper_alg_dict = qr.derive_algebra(pt_alg, less_than_rel, name=lb_proper_alg_name, description=lb_proper_alg_desc)


.. parsed-literal::

    
    19 consistent networks
    CPU times: user 2.24 s, sys: 503 ms, total: 2.75 s
    Wall time: 2.02 s


.. code:: ipython3

    test_lb_proper_alg_dict




.. parsed-literal::

    {'Name': 'Derived_Left_Branching_Proper_Interval_Algebra',
     'Description': 'Extended left-branching proper interval algebra derived from point relations',
     'Relations': {'B': {'Name': 'Before',
       'Converse': 'BI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'BI': {'Name': 'After',
       'Converse': 'B',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'D': {'Name': 'During',
       'Converse': 'DI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'DI': {'Name': 'Contains',
       'Converse': 'D',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'E': {'Name': 'Equals',
       'Converse': 'E',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': True,
       'Symmetric': True,
       'Transitive': True},
      'F': {'Name': 'Finishes',
       'Converse': 'FI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'FI': {'Name': 'Finished-by',
       'Converse': 'F',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'LB': {'Name': 'Left-Before',
       'Converse': 'LBI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'LBI': {'Name': 'Left-After',
       'Converse': 'LB',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'LF': {'Name': 'Left-Finishes',
       'Converse': 'LF',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': True,
       'Transitive': False},
      'LO': {'Name': 'Left-Overlaps',
       'Converse': 'LOI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'LOI': {'Name': 'Left-Overlapped-By',
       'Converse': 'LO',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'L~': {'Name': 'Left-Incomparable',
       'Converse': 'L~',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': True,
       'Transitive': False},
      'M': {'Name': 'Meets',
       'Converse': 'MI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'MI': {'Name': 'Met-By',
       'Converse': 'M',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'O': {'Name': 'Overlaps',
       'Converse': 'OI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'OI': {'Name': 'Overlapped-By',
       'Converse': 'O',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'S': {'Name': 'Starts',
       'Converse': 'SI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'SI': {'Name': 'Started-By',
       'Converse': 'S',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True}},
     'TransTable': {'B': {'B': 'B',
       'BI': 'B|BI|D|DI|E|F|FI|LB|LBI|LF|LO|LOI|L~|M|MI|O|OI|S|SI',
       'D': 'B|D|LB|LO|M|O|S',
       'DI': 'B',
       'E': 'B',
       'F': 'B|D|LB|LO|M|O|S',
       'FI': 'B',
       'LB': 'LB',
       'LBI': 'L~',
       'LF': 'LB',
       'LO': 'LB',
       'LOI': 'LB',
       'L~': 'L~',
       'M': 'B',
       'MI': 'B|D|LB|LO|M|O|S',
       'O': 'B',
       'OI': 'B|D|LB|LO|M|O|S',
       'S': 'B',
       'SI': 'B'},
      'BI': {'B': 'B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI',
       'BI': 'BI',
       'D': 'BI|D|F|MI|OI',
       'DI': 'BI',
       'E': 'BI',
       'F': 'BI',
       'FI': 'BI',
       'LB': 'BI|D|F|LB|LF|LO|LOI|MI|OI',
       'LBI': 'BI',
       'LF': 'BI',
       'LO': 'BI|D|F|MI|OI',
       'LOI': 'BI',
       'L~': 'BI|LBI|L~',
       'M': 'BI|D|F|MI|OI',
       'MI': 'BI',
       'O': 'BI|D|F|MI|OI',
       'OI': 'BI',
       'S': 'BI|D|F|MI|OI',
       'SI': 'BI'},
      'D': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI',
       'E': 'D',
       'F': 'D',
       'FI': 'B|D|M|O|S',
       'LB': 'LB',
       'LBI': 'BI|LBI|L~',
       'LF': 'D|LB|LO',
       'LO': 'D|LB|LO',
       'LOI': 'BI|D|F|LB|LF|LO|LOI|MI|OI',
       'L~': 'L~',
       'M': 'B',
       'MI': 'BI',
       'O': 'B|D|M|O|S',
       'OI': 'BI|D|F|MI|OI',
       'S': 'D',
       'SI': 'BI|D|F|MI|OI'},
      'DI': {'B': 'B|DI|FI|M|O',
       'BI': 'BI|DI|LBI|LOI|MI|OI|SI',
       'D': 'D|DI|E|F|FI|LF|LO|LOI|O|OI|S|SI',
       'DI': 'DI',
       'E': 'DI',
       'F': 'DI|LOI|OI|SI',
       'FI': 'DI',
       'LB': 'LB|LF|LO|LOI',
       'LBI': 'LBI',
       'LF': 'LOI',
       'LO': 'LF|LO|LOI',
       'LOI': 'LOI',
       'L~': 'LBI|L~',
       'M': 'DI|FI|O',
       'MI': 'DI|LOI|OI|SI',
       'O': 'DI|FI|O',
       'OI': 'DI|LOI|OI|SI',
       'S': 'DI|FI|O',
       'SI': 'DI'},
      'E': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'DI',
       'E': 'E',
       'F': 'F',
       'FI': 'FI',
       'LB': 'LB',
       'LBI': 'LBI',
       'LF': 'LF',
       'LO': 'LO',
       'LOI': 'LOI',
       'L~': 'L~',
       'M': 'M',
       'MI': 'MI',
       'O': 'O',
       'OI': 'OI',
       'S': 'S',
       'SI': 'SI'},
      'F': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'BI|DI|MI|OI|SI',
       'E': 'F',
       'F': 'F',
       'FI': 'E|F|FI',
       'LB': 'LB',
       'LBI': 'BI|LBI',
       'LF': 'F|LF',
       'LO': 'D|LO',
       'LOI': 'BI|LOI|MI|OI',
       'L~': 'L~',
       'M': 'M',
       'MI': 'BI',
       'O': 'D|O|S',
       'OI': 'BI|MI|OI',
       'S': 'D',
       'SI': 'BI|MI|OI'},
      'FI': {'B': 'B',
       'BI': 'BI|DI|LBI|LOI|MI|OI|SI',
       'D': 'D|LO|O|S',
       'DI': 'DI',
       'E': 'FI',
       'F': 'E|F|FI|LF',
       'FI': 'FI',
       'LB': 'LB',
       'LBI': 'LBI',
       'LF': 'LF',
       'LO': 'LO',
       'LOI': 'LOI',
       'L~': 'L~',
       'M': 'M',
       'MI': 'DI|LOI|OI|SI',
       'O': 'O',
       'OI': 'DI|LOI|OI|SI',
       'S': 'O',
       'SI': 'DI'},
      'LB': {'B': 'B',
       'BI': 'L~',
       'D': 'LB',
       'DI': 'B|LB|L~',
       'E': 'LB',
       'F': 'LB',
       'FI': 'B|LB',
       'LB': 'LB',
       'LBI': 'B|BI|D|DI|E|F|FI|LB|LBI|LF|LO|LOI|L~|M|MI|O|OI|S|SI',
       'LF': 'B|D|LB|LO|M|O|S',
       'LO': 'B|D|LB|LO|M|O|S',
       'LOI': 'B|D|LB|LO|L~|M|O|S',
       'L~': 'L~',
       'M': 'B',
       'MI': 'L~',
       'O': 'B|LB',
       'OI': 'LB|L~',
       'S': 'LB',
       'SI': 'LB|L~'},
      'LBI': {'B': 'B|DI|FI|LBI|LF|LO|LOI|M|O',
       'BI': 'LBI',
       'D': 'LBI|LF|LO|LOI',
       'DI': 'LBI',
       'E': 'LBI',
       'F': 'LBI',
       'FI': 'LBI',
       'LB': 'D|DI|E|F|FI|LB|LBI|LF|LO|LOI|O|OI|S|SI',
       'LBI': 'LBI',
       'LF': 'LBI',
       'LO': 'LBI|LF|LO|LOI',
       'LOI': 'LBI',
       'L~': 'BI|DI|LBI|LOI|L~|MI|OI|SI',
       'M': 'LBI|LF|LO|LOI',
       'MI': 'LBI',
       'O': 'LBI|LF|LO|LOI',
       'OI': 'LBI',
       'S': 'LBI|LF|LO|LOI',
       'SI': 'LBI'},
      'LF': {'B': 'B',
       'BI': 'LBI',
       'D': 'LO',
       'DI': 'DI|LBI|LOI',
       'E': 'LF',
       'F': 'LF',
       'FI': 'FI|LF',
       'LB': 'LB',
       'LBI': 'BI|DI|LBI|LOI|MI|OI|SI',
       'LF': 'E|F|FI|LF',
       'LO': 'D|LO|O|S',
       'LOI': 'DI|LBI|LOI|OI|SI',
       'L~': 'L~',
       'M': 'M',
       'MI': 'LBI',
       'O': 'LO|O',
       'OI': 'LBI|LOI',
       'S': 'LO',
       'SI': 'LBI|LOI'},
      'LO': {'B': 'B',
       'BI': 'LBI',
       'D': 'LO',
       'DI': 'B|DI|FI|LBI|LF|LO|LOI|M|O',
       'E': 'LO',
       'F': 'LO',
       'FI': 'B|LO|M|O',
       'LB': 'LB',
       'LBI': 'BI|DI|LBI|LOI|L~|MI|OI|SI',
       'LF': 'D|LB|LO|O|S',
       'LO': 'D|LB|LO|O|S',
       'LOI': 'D|DI|E|F|FI|LB|LBI|LF|LO|LOI|O|OI|S|SI',
       'L~': 'L~',
       'M': 'B',
       'MI': 'LBI',
       'O': 'B|LO|M|O',
       'OI': 'LBI|LF|LO|LOI',
       'S': 'LO',
       'SI': 'LBI|LF|LO|LOI'},
      'LOI': {'B': 'B|DI|FI|M|O',
       'BI': 'LBI',
       'D': 'LF|LO|LOI',
       'DI': 'DI|LBI|LOI',
       'E': 'LOI',
       'F': 'LOI',
       'FI': 'DI|LOI',
       'LB': 'LB|LF|LO|LOI',
       'LBI': 'BI|DI|LBI|LOI|MI|OI|SI',
       'LF': 'DI|LOI|OI|SI',
       'LO': 'D|DI|E|F|FI|LF|LO|LOI|O|OI|S|SI',
       'LOI': 'DI|LBI|LOI|OI|SI',
       'L~': 'LBI|L~',
       'M': 'DI|FI|O',
       'MI': 'LBI',
       'O': 'DI|FI|LF|LO|LOI|O',
       'OI': 'LBI|LOI',
       'S': 'LF|LO|LOI',
       'SI': 'LBI|LOI'},
      'L~': {'B': 'B|LB|L~',
       'BI': 'L~',
       'D': 'LB|L~',
       'DI': 'L~',
       'E': 'L~',
       'F': 'L~',
       'FI': 'L~',
       'LB': 'B|D|LB|LO|L~|M|O|S',
       'LBI': 'L~',
       'LF': 'L~',
       'LO': 'LB|L~',
       'LOI': 'L~',
       'L~': 'B|BI|D|DI|E|F|FI|LB|LBI|LF|LO|LOI|L~|M|MI|O|OI|S|SI',
       'M': 'LB|L~',
       'MI': 'L~',
       'O': 'LB|L~',
       'OI': 'L~',
       'S': 'LB|L~',
       'SI': 'L~'},
      'M': {'B': 'B',
       'BI': 'BI|DI|LBI|LOI|MI|OI|SI',
       'D': 'D|LO|O|S',
       'DI': 'B',
       'E': 'M',
       'F': 'D|LO|O|S',
       'FI': 'B',
       'LB': 'LB',
       'LBI': 'L~',
       'LF': 'LB',
       'LO': 'LB',
       'LOI': 'LB',
       'L~': 'L~',
       'M': 'B',
       'MI': 'E|F|FI|LF',
       'O': 'B',
       'OI': 'D|LO|O|S',
       'S': 'M',
       'SI': 'M'},
      'MI': {'B': 'B|DI|FI|M|O',
       'BI': 'BI',
       'D': 'D|F|OI',
       'DI': 'BI',
       'E': 'MI',
       'F': 'MI',
       'FI': 'MI',
       'LB': 'LB|LF|LO|LOI',
       'LBI': 'BI',
       'LF': 'MI',
       'LO': 'D|F|OI',
       'LOI': 'BI',
       'L~': 'LBI|L~',
       'M': 'E|S|SI',
       'MI': 'BI',
       'O': 'D|F|OI',
       'OI': 'BI',
       'S': 'D|F|OI',
       'SI': 'BI'},
      'O': {'B': 'B',
       'BI': 'BI|DI|LBI|LOI|MI|OI|SI',
       'D': 'D|LO|O|S',
       'DI': 'B|DI|FI|M|O',
       'E': 'O',
       'F': 'D|LO|O|S',
       'FI': 'B|M|O',
       'LB': 'LB',
       'LBI': 'LBI|L~',
       'LF': 'LB|LO',
       'LO': 'LB|LO',
       'LOI': 'LB|LF|LO|LOI',
       'L~': 'L~',
       'M': 'B',
       'MI': 'DI|LOI|OI|SI',
       'O': 'B|M|O',
       'OI': 'D|DI|E|F|FI|LF|LO|LOI|O|OI|S|SI',
       'S': 'O',
       'SI': 'DI|FI|O'},
      'OI': {'B': 'B|DI|FI|M|O',
       'BI': 'BI',
       'D': 'D|F|OI',
       'DI': 'BI|DI|MI|OI|SI',
       'E': 'OI',
       'F': 'OI',
       'FI': 'DI|OI|SI',
       'LB': 'LB|LF|LO|LOI',
       'LBI': 'BI|LBI',
       'LF': 'LOI|OI',
       'LO': 'D|F|LF|LO|LOI|OI',
       'LOI': 'BI|LOI|MI|OI',
       'L~': 'LBI|L~',
       'M': 'DI|FI|O',
       'MI': 'BI',
       'O': 'D|DI|E|F|FI|O|OI|S|SI',
       'OI': 'BI|MI|OI',
       'S': 'D|F|OI',
       'SI': 'BI|MI|OI'},
      'S': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'B|DI|FI|M|O',
       'E': 'S',
       'F': 'D',
       'FI': 'B|M|O',
       'LB': 'LB',
       'LBI': 'LBI|L~',
       'LF': 'LB|LO',
       'LO': 'LB|LO',
       'LOI': 'LB|LF|LO|LOI',
       'L~': 'L~',
       'M': 'B',
       'MI': 'MI',
       'O': 'B|M|O',
       'OI': 'D|F|OI',
       'S': 'S',
       'SI': 'E|S|SI'},
      'SI': {'B': 'B|DI|FI|M|O',
       'BI': 'BI',
       'D': 'D|F|OI',
       'DI': 'DI',
       'E': 'SI',
       'F': 'OI',
       'FI': 'DI',
       'LB': 'LB|LF|LO|LOI',
       'LBI': 'LBI',
       'LF': 'LOI',
       'LO': 'LF|LO|LOI',
       'LOI': 'LOI',
       'L~': 'LBI|L~',
       'M': 'DI|FI|O',
       'MI': 'MI',
       'O': 'DI|FI|O',
       'OI': 'OI',
       'S': 'E|S|SI',
       'SI': 'SI'}}}



Save Left-Branching Proper Interval Algebra Dictionary to JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_lb_proper_json_path = os.path.join(path, "Algebras/test_derived_left_branching_proper_interval_algebra.json")
    test_lb_proper_json_path




.. parsed-literal::

    '/Users/alfredreich/Documents/Python/github/myrepos/qualreas/Algebras/test_derived_left_branching_proper_interval_algebra.json'



.. code:: ipython3

    qr.algebra_to_json_file(test_lb_proper_alg_dict, test_lb_proper_json_path)

Instantiate a Left-Branching Proper Interval Algebra Object from JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_lb_proper_alg = qr.Algebra(test_lb_proper_json_path)
    test_lb_proper_alg




.. parsed-literal::

    <qualreas.Algebra at 0x7f840a6ecfa0>



.. code:: ipython3

    test_lb_proper_alg.summary()


.. parsed-literal::

      Algebra Name: Derived_Left_Branching_Proper_Interval_Algebra
       Description: Extended left-branching proper interval algebra derived from point relations
     Equality Rels: E
         Relations:
                NAME (SYMBOL)         CONVERSE (ABBREV)  REFLEXIVE  SYMMETRIC TRANSITIVE   DOMAIN        RANGE
                 Before (  B)               After ( BI)    False      False       True       PInt          PInt
                  After ( BI)              Before (  B)    False      False       True       PInt          PInt
                 During (  D)            Contains ( DI)    False      False       True       PInt          PInt
               Contains ( DI)              During (  D)    False      False       True       PInt          PInt
                 Equals (  E)              Equals (  E)     True       True       True       PInt          PInt
               Finishes (  F)         Finished-by ( FI)    False      False       True       PInt          PInt
            Finished-by ( FI)            Finishes (  F)    False      False       True       PInt          PInt
            Left-Before ( LB)          Left-After (LBI)    False      False       True       PInt          PInt
             Left-After (LBI)         Left-Before ( LB)    False      False       True       PInt          PInt
          Left-Finishes ( LF)       Left-Finishes ( LF)    False       True      False       PInt          PInt
          Left-Overlaps ( LO)  Left-Overlapped-By (LOI)    False      False      False       PInt          PInt
     Left-Overlapped-By (LOI)       Left-Overlaps ( LO)    False      False      False       PInt          PInt
      Left-Incomparable ( L~)   Left-Incomparable ( L~)    False       True      False       PInt          PInt
                  Meets (  M)              Met-By ( MI)    False      False      False       PInt          PInt
                 Met-By ( MI)               Meets (  M)    False      False      False       PInt          PInt
               Overlaps (  O)       Overlapped-By ( OI)    False      False      False       PInt          PInt
          Overlapped-By ( OI)            Overlaps (  O)    False      False      False       PInt          PInt
                 Starts (  S)          Started-By ( SI)    False      False       True       PInt          PInt
             Started-By ( SI)              Starts (  S)    False      False       True       PInt          PInt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


.. code:: ipython3

    test_lb_proper_alg.check_composition_identity()




.. parsed-literal::

    True



.. code:: ipython3

    test_lb_proper_alg.is_associative()


.. parsed-literal::

    TEST SUMMARY: 6859 OK, 0 Skipped, 0 Failed (6859 Total)




.. parsed-literal::

    True


