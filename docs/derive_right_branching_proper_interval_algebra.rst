Derive Right-Branching Proper Interval Algebra
==============================================

NOTE: This algebra derivation restricts intervals to be proper
intervals, similar to Allen’s time interval algebra. So, time points are
not permitted. However, this algebra adds a new point relation,
incomparable, denoted by, r~, which expresses the relationship between
two points on different time branches. The transitivity/composition
table of the right-branching point algebra is defined so that time
branches to the right (i.e., into the future). See the section, below,
titled, “Right-Branching Point Algebra”.

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

Deriving the RB Proper Interval Algebra from RB Point Algebra
-------------------------------------------------------------

Right-Branching Point Algebra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    pt_alg = qr.Algebra(os.path.join(path, "Algebras/Right_Branching_Point_Algebra.json"))

.. code:: ipython3

    pt_alg.summary()


.. parsed-literal::

      Algebra Name: Right_Branching_Point_Algebra
       Description: Right-Branching Point Algebra
     Equality Rels: =
         Relations:
                NAME (SYMBOL)         CONVERSE (ABBREV)  REFLEXIVE  SYMMETRIC TRANSITIVE   DOMAIN        RANGE
               LessThan (  <)         GreaterThan (  >)    False      False       True         Pt            Pt
                 Equals (  =)              Equals (  =)     True       True       True         Pt            Pt
            GreaterThan (  >)            LessThan (  <)    False      False       True         Pt            Pt
           Incomparable ( r~)        Incomparable ( r~)    False       True      False         Pt            Pt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


.. code:: ipython3

    qr.print_point_algebra_composition_table(pt_alg)


.. parsed-literal::

    Right_Branching_Point_Algebra
    Elements: <, =, >, r~
    ==============================
     rel1 ; rel2 = composition
    ==============================
       <      <      <
       <      =      <
       <      >      <\|=\|>
       <     r~      <\|r~
    ------------------------------
       =      <      <
       =      =      =
       =      >      >
       =     r~      r~
    ------------------------------
       >      <      <\|=\|>\|r~
       >      =      >
       >      >      >
       >     r~      r~
    ------------------------------
      r~      <      r~
      r~      =      r~
      r~      >      >\|r~
      r~     r~      <\|=\|>\|r~
    ------------------------------


Derive Right-Branching Proper Interval Algebra as a Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The definition of less than, below, either restricts intervals to be
proper (‘<’) or allows intervals to be degenerate (‘=\|<’) (i.e.,
integrates points and intervals).

.. code:: ipython3

    #less_than_rel = '=|<'
    less_than_rel = '<'

.. code:: ipython3

    rb_proper_alg_name="Derived_Right_Branching_Proper_Interval_Algebra"
    rb_proper_alg_desc="Extended right-branching proper interval algebra derived from point relations"
    
    %time test_rb_proper_alg_dict = qr.derive_algebra(pt_alg, less_than_rel, name=rb_proper_alg_name, description=rb_proper_alg_desc)


.. parsed-literal::

    
    19 consistent networks
    CPU times: user 2.18 s, sys: 436 ms, total: 2.62 s
    Wall time: 2.04 s


.. code:: ipython3

    test_rb_proper_alg_dict




.. parsed-literal::

    {'Name': 'Derived_Right_Branching_Proper_Interval_Algebra',
     'Description': 'Extended right-branching proper interval algebra derived from point relations',
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
      'RB': {'Name': 'Right-Before',
       'Converse': 'RBI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'RBI': {'Name': 'Right-After',
       'Converse': 'RB',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': True},
      'RO': {'Name': 'Right-Overlaps',
       'Converse': 'ROI',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'ROI': {'Name': 'Right-Overlapped-By',
       'Converse': 'RO',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': False,
       'Transitive': False},
      'RS': {'Name': 'Right-Starts',
       'Converse': 'RS',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': True,
       'Transitive': False},
      'R~': {'Name': 'Right-Incomparable',
       'Converse': 'R~',
       'Domain': ['ProperInterval'],
       'Range': ['ProperInterval'],
       'Reflexive': False,
       'Symmetric': True,
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
       'BI': 'B\|BI\|D\|DI\|E\|F\|FI\|M\|MI\|O\|OI\|S\|SI',
       'D': 'B\|D\|M\|O\|S',
       'DI': 'B',
       'E': 'B',
       'F': 'B\|D\|M\|O\|S',
       'FI': 'B',
       'M': 'B',
       'MI': 'B\|D\|M\|O\|S',
       'O': 'B',
       'OI': 'B\|D\|M\|O\|S',
       'RB': 'B',
       'RBI': 'B\|D\|M\|O\|RBI\|RO\|ROI\|RS\|S',
       'RO': 'B',
       'ROI': 'B\|D\|M\|O\|S',
       'RS': 'B',
       'R~': 'B\|RB\|R~',
       'S': 'B',
       'SI': 'B'},
      'BI': {'B': 'B\|BI\|D\|DI\|E\|F\|FI\|M\|MI\|O\|OI\|RB\|RBI\|RO\|ROI\|RS\|R~\|S\|SI',
       'BI': 'BI',
       'D': 'BI\|D\|F\|MI\|OI\|RBI\|ROI',
       'DI': 'BI',
       'E': 'BI',
       'F': 'BI',
       'FI': 'BI',
       'M': 'BI\|D\|F\|MI\|OI\|RBI\|ROI',
       'MI': 'BI',
       'O': 'BI\|D\|F\|MI\|OI\|RBI\|ROI',
       'OI': 'BI',
       'RB': 'R~',
       'RBI': 'RBI',
       'RO': 'RBI',
       'ROI': 'RBI',
       'RS': 'RBI',
       'R~': 'R~',
       'S': 'BI\|D\|F\|MI\|OI\|RBI\|ROI',
       'SI': 'BI'},
      'D': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'B\|BI\|D\|DI\|E\|F\|FI\|M\|MI\|O\|OI\|S\|SI',
       'E': 'D',
       'F': 'D',
       'FI': 'B\|D\|M\|O\|S',
       'M': 'B',
       'MI': 'BI',
       'O': 'B\|D\|M\|O\|S',
       'OI': 'BI\|D\|F\|MI\|OI',
       'RB': 'B\|RB\|R~',
       'RBI': 'RBI',
       'RO': 'B\|D\|M\|O\|RBI\|RO\|ROI\|RS\|S',
       'ROI': 'D\|RBI\|ROI',
       'RS': 'D\|RBI\|ROI',
       'R~': 'R~',
       'S': 'D',
       'SI': 'BI\|D\|F\|MI\|OI'},
      'DI': {'B': 'B\|DI\|FI\|M\|O\|RB\|RO',
       'BI': 'BI\|DI\|MI\|OI\|SI',
       'D': 'D\|DI\|E\|F\|FI\|O\|OI\|RO\|ROI\|RS\|S\|SI',
       'DI': 'DI',
       'E': 'DI',
       'F': 'DI\|OI\|SI',
       'FI': 'DI',
       'M': 'DI\|FI\|O\|RO',
       'MI': 'DI\|OI\|SI',
       'O': 'DI\|FI\|O\|RO',
       'OI': 'DI\|OI\|SI',
       'RB': 'RB',
       'RBI': 'RBI\|RO\|ROI\|RS',
       'RO': 'RO',
       'ROI': 'RO\|ROI\|RS',
       'RS': 'RO',
       'R~': 'RB\|R~',
       'S': 'DI\|FI\|O\|RO',
       'SI': 'DI'},
      'E': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'DI',
       'E': 'E',
       'F': 'F',
       'FI': 'FI',
       'M': 'M',
       'MI': 'MI',
       'O': 'O',
       'OI': 'OI',
       'RB': 'RB',
       'RBI': 'RBI',
       'RO': 'RO',
       'ROI': 'ROI',
       'RS': 'RS',
       'R~': 'R~',
       'S': 'S',
       'SI': 'SI'},
      'F': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'BI\|DI\|MI\|OI\|SI',
       'E': 'F',
       'F': 'F',
       'FI': 'E\|F\|FI',
       'M': 'M',
       'MI': 'BI',
       'O': 'D\|O\|S',
       'OI': 'BI\|MI\|OI',
       'RB': 'RB\|R~',
       'RBI': 'RBI',
       'RO': 'RBI\|RO\|ROI\|RS',
       'ROI': 'RBI\|ROI',
       'RS': 'RBI\|ROI',
       'R~': 'R~',
       'S': 'D',
       'SI': 'BI\|MI\|OI'},
      'FI': {'B': 'B',
       'BI': 'BI\|DI\|MI\|OI\|SI',
       'D': 'D\|O\|S',
       'DI': 'DI',
       'E': 'FI',
       'F': 'E\|F\|FI',
       'FI': 'FI',
       'M': 'M',
       'MI': 'DI\|OI\|SI',
       'O': 'O',
       'OI': 'DI\|OI\|SI',
       'RB': 'RB',
       'RBI': 'RBI\|RO\|ROI\|RS',
       'RO': 'RO',
       'ROI': 'RO\|ROI\|RS',
       'RS': 'RO',
       'R~': 'RB\|R~',
       'S': 'O',
       'SI': 'DI'},
      'M': {'B': 'B',
       'BI': 'BI\|DI\|MI\|OI\|SI',
       'D': 'D\|O\|S',
       'DI': 'B',
       'E': 'M',
       'F': 'D\|O\|S',
       'FI': 'B',
       'M': 'B',
       'MI': 'E\|F\|FI',
       'O': 'B',
       'OI': 'D\|O\|S',
       'RB': 'B',
       'RBI': 'RBI\|RO\|ROI\|RS',
       'RO': 'B',
       'ROI': 'D\|O\|S',
       'RS': 'M',
       'R~': 'RB\|R~',
       'S': 'M',
       'SI': 'M'},
      'MI': {'B': 'B\|DI\|FI\|M\|O\|RB\|RO',
       'BI': 'BI',
       'D': 'D\|F\|OI\|ROI',
       'DI': 'BI',
       'E': 'MI',
       'F': 'MI',
       'FI': 'MI',
       'M': 'E\|RS\|S\|SI',
       'MI': 'BI',
       'O': 'D\|F\|OI\|ROI',
       'OI': 'BI',
       'RB': 'R~',
       'RBI': 'RBI',
       'RO': 'RBI',
       'ROI': 'RBI',
       'RS': 'RBI',
       'R~': 'R~',
       'S': 'D\|F\|OI\|ROI',
       'SI': 'BI'},
      'O': {'B': 'B',
       'BI': 'BI\|DI\|MI\|OI\|SI',
       'D': 'D\|O\|S',
       'DI': 'B\|DI\|FI\|M\|O',
       'E': 'O',
       'F': 'D\|O\|S',
       'FI': 'B\|M\|O',
       'M': 'B',
       'MI': 'DI\|OI\|SI',
       'O': 'B\|M\|O',
       'OI': 'D\|DI\|E\|F\|FI\|O\|OI\|S\|SI',
       'RB': 'B\|RB',
       'RBI': 'RBI\|RO\|ROI\|RS',
       'RO': 'B\|M\|O\|RO',
       'ROI': 'D\|O\|RO\|ROI\|RS\|S',
       'RS': 'O\|RO',
       'R~': 'RB\|R~',
       'S': 'O',
       'SI': 'DI\|FI\|O'},
      'OI': {'B': 'B\|DI\|FI\|M\|O\|RB\|RO',
       'BI': 'BI',
       'D': 'D\|F\|OI\|ROI',
       'DI': 'BI\|DI\|MI\|OI\|SI',
       'E': 'OI',
       'F': 'OI',
       'FI': 'DI\|OI\|SI',
       'M': 'DI\|FI\|O\|RO',
       'MI': 'BI',
       'O': 'D\|DI\|E\|F\|FI\|O\|OI\|RO\|ROI\|RS\|S\|SI',
       'OI': 'BI\|MI\|OI',
       'RB': 'RB\|R~',
       'RBI': 'RBI',
       'RO': 'RBI\|RO\|ROI\|RS',
       'ROI': 'RBI\|ROI',
       'RS': 'RBI\|ROI',
       'R~': 'R~',
       'S': 'D\|F\|OI\|ROI',
       'SI': 'BI\|MI\|OI'},
      'RB': {'B': 'RB',
       'BI': 'BI\|DI\|MI\|OI\|RB\|RO\|ROI\|RS\|SI',
       'D': 'RB\|RO\|ROI\|RS',
       'DI': 'RB',
       'E': 'RB',
       'F': 'RB\|RO\|ROI\|RS',
       'FI': 'RB',
       'M': 'RB',
       'MI': 'RB\|RO\|ROI\|RS',
       'O': 'RB',
       'OI': 'RB\|RO\|ROI\|RS',
       'RB': 'RB',
       'RBI': 'D\|DI\|E\|F\|FI\|O\|OI\|RB\|RBI\|RO\|ROI\|RS\|S\|SI',
       'RO': 'RB',
       'ROI': 'RB\|RO\|ROI\|RS',
       'RS': 'RB',
       'R~': 'B\|DI\|FI\|M\|O\|RB\|RO\|R~',
       'S': 'RB',
       'SI': 'RB'},
      'RBI': {'B': 'R~',
       'BI': 'BI',
       'D': 'RBI',
       'DI': 'BI\|RBI\|R~',
       'E': 'RBI',
       'F': 'RBI',
       'FI': 'RBI\|R~',
       'M': 'R~',
       'MI': 'BI',
       'O': 'RBI\|R~',
       'OI': 'BI\|RBI',
       'RB': 'B\|BI\|D\|DI\|E\|F\|FI\|M\|MI\|O\|OI\|RB\|RBI\|RO\|ROI\|RS\|R~\|S\|SI',
       'RBI': 'RBI',
       'RO': 'BI\|D\|F\|MI\|OI\|RBI\|ROI\|R~',
       'ROI': 'BI\|D\|F\|MI\|OI\|RBI\|ROI',
       'RS': 'BI\|D\|F\|MI\|OI\|RBI\|ROI',
       'R~': 'R~',
       'S': 'RBI',
       'SI': 'BI\|RBI'},
      'RO': {'B': 'RB',
       'BI': 'BI\|DI\|MI\|OI\|SI',
       'D': 'RO\|ROI\|RS',
       'DI': 'DI\|RB\|RO',
       'E': 'RO',
       'F': 'RO\|ROI\|RS',
       'FI': 'RB\|RO',
       'M': 'RB',
       'MI': 'DI\|OI\|SI',
       'O': 'RB\|RO',
       'OI': 'DI\|OI\|RO\|ROI\|RS\|SI',
       'RB': 'B\|DI\|FI\|M\|O\|RB\|RO',
       'RBI': 'RBI\|RO\|ROI\|RS',
       'RO': 'DI\|FI\|O\|RB\|RO',
       'ROI': 'D\|DI\|E\|F\|FI\|O\|OI\|RO\|ROI\|RS\|S\|SI',
       'RS': 'DI\|FI\|O\|RO',
       'R~': 'RB\|R~',
       'S': 'RO',
       'SI': 'DI\|RO'},
      'ROI': {'B': 'RB',
       'BI': 'BI',
       'D': 'ROI',
       'DI': 'BI\|DI\|MI\|OI\|RB\|RO\|ROI\|RS\|SI',
       'E': 'ROI',
       'F': 'ROI',
       'FI': 'RB\|RO\|ROI\|RS',
       'M': 'RB',
       'MI': 'BI',
       'O': 'RB\|RO\|ROI\|RS',
       'OI': 'BI\|MI\|OI\|ROI',
       'RB': 'B\|DI\|FI\|M\|O\|RB\|RO\|R~',
       'RBI': 'RBI',
       'RO': 'D\|DI\|E\|F\|FI\|O\|OI\|RB\|RBI\|RO\|ROI\|RS\|S\|SI',
       'ROI': 'D\|F\|OI\|RBI\|ROI',
       'RS': 'D\|F\|OI\|RBI\|ROI',
       'R~': 'R~',
       'S': 'ROI',
       'SI': 'BI\|MI\|OI\|ROI'},
      'RS': {'B': 'RB',
       'BI': 'BI',
       'D': 'ROI',
       'DI': 'DI\|RB\|RO',
       'E': 'RS',
       'F': 'ROI',
       'FI': 'RB\|RO',
       'M': 'RB',
       'MI': 'MI',
       'O': 'RB\|RO',
       'OI': 'OI\|ROI',
       'RB': 'B\|DI\|FI\|M\|O\|RB\|RO',
       'RBI': 'RBI',
       'RO': 'DI\|FI\|O\|RB\|RO',
       'ROI': 'D\|F\|OI\|ROI',
       'RS': 'E\|RS\|S\|SI',
       'R~': 'R~',
       'S': 'RS',
       'SI': 'RS\|SI'},
      'R~': {'B': 'R~',
       'BI': 'BI\|RBI\|R~',
       'D': 'RBI\|R~',
       'DI': 'R~',
       'E': 'R~',
       'F': 'RBI\|R~',
       'FI': 'R~',
       'M': 'R~',
       'MI': 'RBI\|R~',
       'O': 'R~',
       'OI': 'RBI\|R~',
       'RB': 'R~',
       'RBI': 'BI\|D\|F\|MI\|OI\|RBI\|ROI\|R~',
       'RO': 'R~',
       'ROI': 'RBI\|R~',
       'RS': 'R~',
       'R~': 'B\|BI\|D\|DI\|E\|F\|FI\|M\|MI\|O\|OI\|RB\|RBI\|RO\|ROI\|RS\|R~\|S\|SI',
       'S': 'R~',
       'SI': 'R~'},
      'S': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'B\|DI\|FI\|M\|O',
       'E': 'S',
       'F': 'D',
       'FI': 'B\|M\|O',
       'M': 'B',
       'MI': 'MI',
       'O': 'B\|M\|O',
       'OI': 'D\|F\|OI',
       'RB': 'B\|RB',
       'RBI': 'RBI',
       'RO': 'B\|M\|O\|RO',
       'ROI': 'D\|ROI',
       'RS': 'RS\|S',
       'R~': 'R~',
       'S': 'S',
       'SI': 'E\|S\|SI'},
      'SI': {'B': 'B\|DI\|FI\|M\|O\|RB\|RO',
       'BI': 'BI',
       'D': 'D\|F\|OI\|ROI',
       'DI': 'DI',
       'E': 'SI',
       'F': 'OI',
       'FI': 'DI',
       'M': 'DI\|FI\|O\|RO',
       'MI': 'MI',
       'O': 'DI\|FI\|O\|RO',
       'OI': 'OI',
       'RB': 'RB',
       'RBI': 'RBI',
       'RO': 'RO',
       'ROI': 'ROI',
       'RS': 'RS',
       'R~': 'R~',
       'S': 'E\|RS\|S\|SI',
       'SI': 'SI'}}}



Save Right-Branching Proper Interval Algebra Dictionary to JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_rb_proper_json_path = os.path.join(path, "Algebras/test_derived_right_branching_proper_interval_algebra.json")
    test_rb_proper_json_path




.. parsed-literal::

    '/Users/alfredreich/Documents/Python/github/myrepos/qualreas/Algebras/test_derived_right_branching_proper_interval_algebra.json'



.. code:: ipython3

    qr.algebra_to_json_file(test_rb_proper_alg_dict, test_rb_proper_json_path)

Instantiate a Right-Branching Proper Interval Algebra Object from JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_rb_proper_alg = qr.Algebra(test_rb_proper_json_path)
    test_rb_proper_alg




.. parsed-literal::

    <qualreas.Algebra at 0x7fab72b158e0>



.. code:: ipython3

    test_rb_proper_alg.summary()


.. parsed-literal::

      Algebra Name: Derived_Right_Branching_Proper_Interval_Algebra
       Description: Extended right-branching proper interval algebra derived from point relations
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
                  Meets (  M)              Met-By ( MI)    False      False      False       PInt          PInt
                 Met-By ( MI)               Meets (  M)    False      False      False       PInt          PInt
               Overlaps (  O)       Overlapped-By ( OI)    False      False      False       PInt          PInt
          Overlapped-By ( OI)            Overlaps (  O)    False      False      False       PInt          PInt
           Right-Before ( RB)         Right-After (RBI)    False      False       True       PInt          PInt
            Right-After (RBI)        Right-Before ( RB)    False      False       True       PInt          PInt
         Right-Overlaps ( RO) Right-Overlapped-By (ROI)    False      False      False       PInt          PInt
    Right-Overlapped-By (ROI)      Right-Overlaps ( RO)    False      False      False       PInt          PInt
           Right-Starts ( RS)        Right-Starts ( RS)    False       True      False       PInt          PInt
     Right-Incomparable ( R~)  Right-Incomparable ( R~)    False       True      False       PInt          PInt
                 Starts (  S)          Started-By ( SI)    False      False       True       PInt          PInt
             Started-By ( SI)              Starts (  S)    False      False       True       PInt          PInt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


.. code:: ipython3

    test_rb_proper_alg.check_composition_identity()




.. parsed-literal::

    True



.. code:: ipython3

    test_rb_proper_alg.is_associative()


.. parsed-literal::

    TEST SUMMARY: 6859 OK, 0 Skipped, 0 Failed (6859 Total)




.. parsed-literal::

    True


