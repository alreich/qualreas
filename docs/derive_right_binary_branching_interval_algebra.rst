Derive Right-Binary-Branching Interval Algebra
==============================================

NOTE: This algebra derives an algebra very similar to the Right
Branching Interval Algebra, except that it uses a right-branching point
algebra that only allows binary branching. See the section, below,
titled, “Right-Binary-Branching Point Algebra”.

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

Deriving the Right-Binary-Branching (RBB) Interval Algebra from RBB Point Algebra
---------------------------------------------------------------------------------

RBB Point Algebra
~~~~~~~~~~~~~~~~~

.. code:: ipython3

    pt_alg = qr.Algebra(os.path.join(path, "Algebras/Right_Binary_Branching_Point_Algebra.json"))

.. code:: ipython3

    pt_alg.summary()


.. parsed-literal::

      Algebra Name: Right_Binary_Branching_Point_Algebra
       Description: Right-Binary-Branching Point Algebra
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

    Right_Binary_Branching_Point_Algebra
    Elements: <, =, >, r~
    ==============================
     rel1 ; rel2 = composition
    ==============================
       <      <      <
       <      =      <
       <      >      <|=|>
       <     r~      <|r~
    ------------------------------
       =      <      <
       =      =      =
       =      >      >
       =     r~      r~
    ------------------------------
       >      <      <|=|>|r~
       >      =      >
       >      >      >
       >     r~      r~
    ------------------------------
      r~      <      r~
      r~      =      r~
      r~      >      >|r~
      r~     r~      <|=|>
    ------------------------------


Derive RBB Algebra as a Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The definition of less than, below, either restricts intervals to be
proper (‘<’) or allows intervals to be degenerate (‘=|<’) (i.e.,
integrates points and intervals).

.. code:: ipython3

    less_than_rel = '=|<'
    #less_than_rel = '<'

.. code:: ipython3

    rbb_alg_name="Derived_Right_Binary_Branching_Interval_Algebra"
    rbb_alg_desc="Extended right-binary-branching interval algebra derived from point relations"
    
    %time test_rbb_alg_dict = qr.derive_algebra(pt_alg, less_than_rel, name=rbb_alg_name, description=rbb_alg_desc)


.. parsed-literal::

    
    24 consistent networks


.. code:: ipython3

    test_rbb_alg_dict

Save RBB Algebra Dictionary to JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_rbb_json_path = os.path.join(path, "Algebras/test_derived_right_binary_branching_interval_algebra.json")
    test_rbb_json_path

.. code:: ipython3

    qr.algebra_to_json_file(test_rbb_alg_dict, test_rbb_json_path)

Instantiate a RBB Algebra Object from JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_rbb_alg = qr.Algebra(test_rbb_json_path)
    test_rbb_alg

.. code:: ipython3

    test_rbb_alg.summary()

.. code:: ipython3

    test_rbb_alg.check_composition_identity()

.. code:: ipython3

    test_rbb_alg.is_associative()
