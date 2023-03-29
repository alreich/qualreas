Derive Allen’s Algebra
======================

NOTE: The code below derives Allen’s original algebra of proper time
intervals.

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

Deriving Allen’s Interval Algebra from Basic Point Algebra
----------------------------------------------------------

Basic Point Algebra
~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    pt_alg = qr.Algebra(os.path.join(path, "Algebras/Linear_Point_Algebra.json"))

.. code:: ipython3

    pt_alg.summary()


.. parsed-literal::

      Algebra Name: Linear_Point_Algebra
       Description: Linear Point Algebra
     Equality Rels: =
         Relations:
                NAME (SYMBOL)         CONVERSE (ABBREV)  REFLEXIVE  SYMMETRIC TRANSITIVE   DOMAIN        RANGE
               LessThan (  <)         GreaterThan (  >)    False      False       True         Pt            Pt
                 Equals (  =)              Equals (  =)     True       True       True         Pt            Pt
            GreaterThan (  >)            LessThan (  <)    False      False       True         Pt            Pt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


.. code:: ipython3

    qr.print_point_algebra_composition_table(pt_alg)


.. parsed-literal::

    Linear_Point_Algebra
    Elements: <, =, >
    ==============================
     rel1 ; rel2 = composition
    ==============================
       <      <      <
       <      =      <
       <      >      <|=|>
    ------------------------------
       =      <      <
       =      =      =
       =      >      >
    ------------------------------
       >      <      <|=|>
       >      =      >
       >      >      >
    ------------------------------


Derive Allen’s Algebra as a Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The definition of less than, below, either restricts intervals to be
proper (‘<’) or allows intervals to be degenerate (‘=|<’) (i.e.,
integrates points and intervals).

.. code:: ipython3

    #less_than_rel = '=|<'
    less_than_rel = '<'

.. code:: ipython3

    allen_alg_name = "Derived_Allen_Algebra"
    allen_alg_desc = "Allens algebra derived from point relations"
    
    verbose = True
    
    %time test_allen_alg_dict = qr.derive_algebra(pt_alg, less_than_rel, name=allen_alg_name, description=allen_alg_desc, verbose=verbose)


.. parsed-literal::

    ==========================
    <,<,<,<
    B
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '<' '<']
     ['>' '=' '<' '<']
     ['>' '>' '=' '<']
     ['>' '>' '>' '=']]
    ==========================
    <,<,=,<
    M
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '<' '<']
     ['>' '=' '=' '<']
     ['>' '=' '=' '<']
     ['>' '>' '>' '=']]
    ==========================
    <,<,>,<
    O
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '<' '<']
     ['>' '=' '>' '<']
     ['>' '<' '=' '<']
     ['>' '>' '>' '=']]
    ==========================
    <,<,>,=
    FI
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '<' '<']
     ['>' '=' '>' '=']
     ['>' '<' '=' '<']
     ['>' '=' '>' '=']]
    ==========================
    <,<,>,>
    DI
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '<' '<']
     ['>' '=' '>' '>']
     ['>' '<' '=' '<']
     ['>' '<' '>' '=']]
    ==========================
    =,<,>,<
    S
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '=' '<']
     ['>' '=' '>' '<']
     ['=' '<' '=' '<']
     ['>' '>' '>' '=']]
    ==========================
    =,<,>,=
    E
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '=' '<']
     ['>' '=' '>' '=']
     ['=' '<' '=' '<']
     ['>' '=' '>' '=']]
    ==========================
    =,<,>,>
    SI
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '=' '<']
     ['>' '=' '>' '>']
     ['=' '<' '=' '<']
     ['>' '<' '>' '=']]
    ==========================
    >,<,>,<
    D
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '>' '<']
     ['>' '=' '>' '<']
     ['<' '<' '=' '<']
     ['>' '>' '>' '=']]
    ==========================
    >,<,>,=
    F
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '>' '<']
     ['>' '=' '>' '=']
     ['<' '<' '=' '<']
     ['>' '=' '>' '=']]
    ==========================
    >,<,>,>
    OI
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '>' '<']
     ['>' '=' '>' '>']
     ['<' '<' '=' '<']
     ['>' '<' '>' '=']]
    ==========================
    >,=,>,>
    MI
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '>' '=']
     ['>' '=' '>' '>']
     ['<' '<' '=' '<']
     ['=' '<' '>' '=']]
    ==========================
    >,>,>,>
    BI
    (['ProperInterval'], ['ProperInterval'])
    [['=' '<' '>' '>']
     ['>' '=' '>' '>']
     ['<' '<' '=' '<']
     ['<' '<' '>' '=']]
    
    13 consistent networks
    CPU times: user 869 ms, sys: 428 ms, total: 1.3 s
    Wall time: 714 ms


.. code:: ipython3

    test_allen_alg_dict




.. parsed-literal::

    {'Name': 'Derived_Allen_Algebra',
     'Description': 'Allens algebra derived from point relations',
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
       'BI': 'B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI',
       'D': 'B|D|M|O|S',
       'DI': 'B',
       'E': 'B',
       'F': 'B|D|M|O|S',
       'FI': 'B',
       'M': 'B',
       'MI': 'B|D|M|O|S',
       'O': 'B',
       'OI': 'B|D|M|O|S',
       'S': 'B',
       'SI': 'B'},
      'BI': {'B': 'B|BI|D|DI|E|F|FI|M|MI|O|OI|S|SI',
       'BI': 'BI',
       'D': 'BI|D|F|MI|OI',
       'DI': 'BI',
       'E': 'BI',
       'F': 'BI',
       'FI': 'BI',
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
       'M': 'B',
       'MI': 'BI',
       'O': 'B|D|M|O|S',
       'OI': 'BI|D|F|MI|OI',
       'S': 'D',
       'SI': 'BI|D|F|MI|OI'},
      'DI': {'B': 'B|DI|FI|M|O',
       'BI': 'BI|DI|MI|OI|SI',
       'D': 'D|DI|E|F|FI|O|OI|S|SI',
       'DI': 'DI',
       'E': 'DI',
       'F': 'DI|OI|SI',
       'FI': 'DI',
       'M': 'DI|FI|O',
       'MI': 'DI|OI|SI',
       'O': 'DI|FI|O',
       'OI': 'DI|OI|SI',
       'S': 'DI|FI|O',
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
       'S': 'S',
       'SI': 'SI'},
      'F': {'B': 'B',
       'BI': 'BI',
       'D': 'D',
       'DI': 'BI|DI|MI|OI|SI',
       'E': 'F',
       'F': 'F',
       'FI': 'E|F|FI',
       'M': 'M',
       'MI': 'BI',
       'O': 'D|O|S',
       'OI': 'BI|MI|OI',
       'S': 'D',
       'SI': 'BI|MI|OI'},
      'FI': {'B': 'B',
       'BI': 'BI|DI|MI|OI|SI',
       'D': 'D|O|S',
       'DI': 'DI',
       'E': 'FI',
       'F': 'E|F|FI',
       'FI': 'FI',
       'M': 'M',
       'MI': 'DI|OI|SI',
       'O': 'O',
       'OI': 'DI|OI|SI',
       'S': 'O',
       'SI': 'DI'},
      'M': {'B': 'B',
       'BI': 'BI|DI|MI|OI|SI',
       'D': 'D|O|S',
       'DI': 'B',
       'E': 'M',
       'F': 'D|O|S',
       'FI': 'B',
       'M': 'B',
       'MI': 'E|F|FI',
       'O': 'B',
       'OI': 'D|O|S',
       'S': 'M',
       'SI': 'M'},
      'MI': {'B': 'B|DI|FI|M|O',
       'BI': 'BI',
       'D': 'D|F|OI',
       'DI': 'BI',
       'E': 'MI',
       'F': 'MI',
       'FI': 'MI',
       'M': 'E|S|SI',
       'MI': 'BI',
       'O': 'D|F|OI',
       'OI': 'BI',
       'S': 'D|F|OI',
       'SI': 'BI'},
      'O': {'B': 'B',
       'BI': 'BI|DI|MI|OI|SI',
       'D': 'D|O|S',
       'DI': 'B|DI|FI|M|O',
       'E': 'O',
       'F': 'D|O|S',
       'FI': 'B|M|O',
       'M': 'B',
       'MI': 'DI|OI|SI',
       'O': 'B|M|O',
       'OI': 'D|DI|E|F|FI|O|OI|S|SI',
       'S': 'O',
       'SI': 'DI|FI|O'},
      'OI': {'B': 'B|DI|FI|M|O',
       'BI': 'BI',
       'D': 'D|F|OI',
       'DI': 'BI|DI|MI|OI|SI',
       'E': 'OI',
       'F': 'OI',
       'FI': 'DI|OI|SI',
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
       'M': 'DI|FI|O',
       'MI': 'MI',
       'O': 'DI|FI|O',
       'OI': 'OI',
       'S': 'E|S|SI',
       'SI': 'SI'}}}



Save Algebra Dictionary to JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_allen_json_path = os.path.join(path, "Algebras/test_derived_allen_algebra.json")
    test_allen_json_path




.. parsed-literal::

    '/Users/alfredreich/Documents/Python/github/myrepos/qualreas/Algebras/test_derived_allen_algebra.json'



.. code:: ipython3

    qr.algebra_to_json_file(test_allen_alg_dict, test_allen_json_path)

Instantiate an Algebra Object from JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_allen_alg = qr.Algebra(test_allen_json_path)
    test_allen_alg




.. parsed-literal::

    <qualreas.Algebra at 0x7feb4892fd60>



.. code:: ipython3

    test_allen_alg.summary()


.. parsed-literal::

      Algebra Name: Derived_Allen_Algebra
       Description: Allens algebra derived from point relations
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
                 Starts (  S)          Started-By ( SI)    False      False       True       PInt          PInt
             Started-By ( SI)              Starts (  S)    False      False       True       PInt          PInt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


.. code:: ipython3

    test_allen_alg.check_composition_identity()




.. parsed-literal::

    True



.. code:: ipython3

    test_allen_alg.is_associative()


.. parsed-literal::

    TEST SUMMARY: 2197 OK, 0 Skipped, 0 Failed (2197 Total)




.. parsed-literal::

    True



Load Original Allen’s Algebra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    allen_alg = qr.Algebra(os.path.join(path, "Algebras/Linear_Interval_Algebra.json"))
    allen_alg




.. parsed-literal::

    <qualreas.Algebra at 0x7feb4892f430>



.. code:: ipython3

    allen_alg.summary()


.. parsed-literal::

      Algebra Name: Linear_Interval_Algebra
       Description: Allen's algebra of proper time intervals
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
                 Starts (  S)          Started-By ( SI)    False      False       True       PInt          PInt
             Started-By ( SI)              Starts (  S)    False      False       True       PInt          PInt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


Compare Derived Allen Algebra with Original
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    print(f"Same as original algebra? {allen_alg.equivalent_algebra(test_allen_alg)}")


.. parsed-literal::

    Same as original algebra? True

