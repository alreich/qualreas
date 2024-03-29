Time Point Algebras
===================

.. code:: ipython3

    >>> import os
    >>> import qualreas as qr

.. code:: ipython3

    >>> path = os.path.join(os.getenv('PYPROJ'), 'qualreas')

References
----------

1. James F. Allen, “Maintaining knowledge about temporal intervals”,
   Communications of the ACM 26(11) pp.832-843, Nov. 1983
2. J. F. A. K. van Benthem, “The Logic of Time”, D. Reidel Publishing
   Co., 1983
3. Alfred J. Reich, “Intervals, Points, and Branching Time”, In:
   Goodwin, S.D., Hamilton, H.J. (eds.) Proceedings of the TIME-94
   International Workshop on Temporal Reasoning, University of Regina,
   Regina, SK, Canada, pp. 121–133, 1994

The Structures of Linear and Branching Time
-------------------------------------------

The point (and interval) algebras of time, supported by qualreas,
consider the structure of time to be either linear or branching as shown
in the figures below.

.. code:: ipython3

    from IPython.display import Image  # Only needed to display figures here
    Image(filename='../docs/_static/global_structures_of_time.png', width="400")




.. image:: output_7_0.png
   :width: 400px



Point Structure
~~~~~~~~~~~~~~~

According to [van Benthem, 1983] a Point Structure is an ordered pair,
:math:`(\mathcal{T},\prec)`, where :math:`\mathcal{T}` is a non-empty
set and :math:`\prec` is a transitive binary relation on
:math:`\mathcal{T}`. Equality is denoted by :math:`=`, and the converse
of :math:`\prec` is :math:`\succ`.

Linear Point Structure
~~~~~~~~~~~~~~~~~~~~~~

A Linear Point Structure is a Point Structure,
:math:`(\mathcal{T},\prec)`, such that for any two points,
:math:`x,y \in \mathcal{T}`, one and only one of the following three
relationships holds:

.. raw:: html

   <p>

:math:`(x \prec y) \vee (x = y) \vee (x \succ y)`

.. raw:: html

   </p>

Example: If :math:`\mathbb{R}` is the set of real numbers, then both
:math:`(\mathbb{R},<)` and :math:`(\mathbb{R},\le)` are Linear Point
Structures.

Branching Point Structure
~~~~~~~~~~~~~~~~~~~~~~~~~

A Branching Point Structure is an ordered triple,
:math:`(\mathcal{T},\prec,\sim)`, where :math:`(\mathcal{T},\prec)` is a
Point Structure and :math:`\sim` is an irreflexive, symmetric binary
relation on :math:`\mathcal{T}`, called incomparable, such that for any
:math:`x,y \in \mathcal{T}`, one and only one of the following four
relationships holds:

.. raw:: html

   <p>

:math:`(x \prec y) \vee (x = y) \vee (x \succ y) \vee (x \sim y)`

.. raw:: html

   </p>

Basically, if :math:`x` and :math:`y` are on two different branches,
then :math:`x \sim y`.

Binary-Branching vs. Poly-Branching
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a subtle difference in the composition of the incomparable
relation with itself (:math:`\sim;\sim`) depending on whether only two
branches are allowed at a branch point (binary-branching) or more than
two branches are allowed (poly-branching).

-  binary-branching: :math:`(\sim ; \sim) = \{\prec, =, \succ\}`
-  poly-branching: :math:`(\sim ; \sim) = \{\prec, =, \succ, \sim\}`

Right-Branching Point Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Right-Branching Point Structure is a Branching Point Structure that
has the property of Left Linearity:

.. raw:: html

   <p>

:math:`x,y,z \in \mathcal{T}` and
:math:`(x < z) \wedge (y < z) \implies (x < y) \vee (x = y) \vee (x > y)`

.. raw:: html

   </p>

.. code:: ipython3

    Image(filename='../docs/_static/left_linearity_in_right_branching_time.png', width="300")




.. image:: output_18_0.png
   :width: 300px



Left-Branching Point Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Left-Branching Point Structure is a Branching Point Structure that has
the property of Right Linearity:

.. raw:: html

   <p>

:math:`x,y,z \in \mathcal{T}` and
:math:`(x > z) \wedge (y > z) \implies (x < y) \vee (x = y) \vee (x > y)`

.. raw:: html

   </p>

NOTE: In the branching point algebras defined in qualreas, we
distinguish between the right & left incomparable (:math:`\sim`)
relations by putting an “r” or an “l” in front of :math:`\sim` (i.e.,
“r~”, “l~”). This is not really necessary, since right and left
branching point structures cannot be mixed together, but this is how
things got started in qualreas, so it remains that way, for now. In the
discussion, below, the left and right branching incomparable relations
are denoted by :math:`\underset{L}{\sim}` and
:math:`\underset{R}{\sim}`, respectively.

Linear Point Algebra
--------------------

This algebra is based on the Linear Point Structure,
:math:`(\mathbb{R},<)`, and is used to derive Allen’s algebra of proper
time intervals [Allen, 1983]–known in qualreas as the “Linear Interval
Algebra”. (See the Jupyter Notebook,
“Notebooks/derive_allens_algebra.ipynb”)

An extension to Allen’s algebra, the “Extended Linear Interval Algebra”
[Reich, 1994], integrates proper time intervals with time points by
using the Linear Point Structure, :math:`(\mathbb{R},\le)`. (See the
Jupyter Notebook, “Notebooks/derive_extended_interval_algebra.ipynb”)

.. code:: ipython3

    >>> pt_alg = qr.Algebra(os.path.join(path, "Algebras/Linear_Point_Algebra.json"))
    
    >>> pt_alg.summary()


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


-  EDITORS NOTE: The function call to
   print_point_algebra_composition_table, below, causes issues with the
   automated documentation system used here (Sphinx) because the
   specific elements printed out (equality & inequality symbols)
   “confuse” the system that parses reST (restructured text).
   Consequently, the next cell is set to be “Raw NBConvert” instead of
   “Code”, and then an image of its proper output (from a version of
   this Jupyter notebook) is shown below it, to depict how the output
   should look. The same trick is applied to all 5 of the calls to
   print_point_algebra_composition_table in this document. (Sorry for
   the interruption.)

>>> qr.print_point_algebra_composition_table(pt_alg) # SEE EDITOR'S NOTE, ABOVE

.. code:: ipython3

    Image(filename='../docs/_static/Linear_Pt_Alg_Elements.png')




.. image:: output_57_0.png



Right-Branching Point Algebra
-----------------------------

An extension to Allen’s algebra, the “Right-Branching Interval Algebra”
[Reich, 1994], integrates proper time intervals with time points in a
poly-branching, right-branching time structure, by using the
Right-Branching Point Structure,
:math:`(\mathbb{R},\le, \underset{R}{\sim})`, below. (See the Jupyter
Notebook, “Notebooks/derive_right_branching_interval_algebra.ipynb”)

.. code:: ipython3

    >>> rb_pt_alg = qr.Algebra(os.path.join(path, "Algebras/Right_Branching_Point_Algebra.json"))
    
    >>> rb_pt_alg.summary()


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


>>> qr.print_point_algebra_composition_table(rb_pt_alg) # SEE EDITOR'S NOTE, ABOVE

.. code:: ipython3

    Image(filename='../docs/_static/Rt_Branching_Pt_Alg_Elements.png')




.. image:: output_82_0.png



Left-Branching Point Algebra
----------------------------

An extension to Allen’s algebra, the “Left-Branching Interval Algebra”
[Reich, 1994], integrates proper time intervals with time points in a
poly-branching, left-branching time structure, by using the
Left-Branching Point Structure,
:math:`(\mathbb{R},\le, \underset{L}{\sim})`, below. (See the Jupyter
Notebook, “Notebooks/derive_right_branching_interval_algebra.ipynb”)

.. code:: ipython3

    >>> lb_pt_alg = qr.Algebra(os.path.join(path, "Algebras/Left_Branching_Point_Algebra.json"))
    
    >>> lb_pt_alg.summary()


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


>>> qr.print_point_algebra_composition_table(lb_pt_alg) # SEE EDITOR'S NOTE, ABOVE

.. code:: ipython3

    Image(filename='../docs/_static/Lf_Branching_Pt_Alg_Elements.png')




.. image:: output_37_0.png



Right-Binary-Branching Point Algebra
------------------------------------

The “Right-Binary-Branching Interval Algebra”, is Allen’s algebra of
proper intervals, situated in a binary-branching, right-branching time
structure, and is derived using the Right-Binary-Branching Point
Structure, :math:`(\mathbb{R},\le, \underset{L}{\sim})`, below. (See the
Jupyter Notebook,
“Notebooks/derive_right_binary_branching_interval_algebra.ipynb”)

.. code:: ipython3

    >>> rbb_pt_alg = qr.Algebra(os.path.join(path, "Algebras/Right_Binary_Branching_Point_Algebra.json"))
    
    >>> rbb_pt_alg.summary()


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


>>> qr.print_point_algebra_composition_table(rbb_pt_alg) # SEE EDITOR'S NOTE, ABOVE

.. code:: ipython3

    Image(filename='../docs/_static/Rt_Bin_Branching_Pt_Alg_Elements.png')




.. image:: output_42_0.png



Left-Binary-Branching Point Algebra
-----------------------------------

The “Left-Binary-Branching Interval Algebra”, is Allen’s algebra of
proper intervals, situated in a binary-branching, left-branching time
structure, and is derived using the Left-Binary-Branching Point
Structure, :math:`(\mathbb{R},\le, \underset{L}{\sim})`, below. (See the
Jupyter Notebook,
“Notebooks/derive_left_binary_branching_interval_algebra.ipynb”)

.. code:: ipython3

    >>> lbb_pt_alg = qr.Algebra(os.path.join(path, "Algebras/Left_Binary_Branching_Point_Algebra.json"))
    
    >>> lbb_pt_alg.summary()


.. parsed-literal::

      Algebra Name: Left_Binary_Branching_Point_Algebra
       Description: Left-Binary-Branching Point Algebra
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


>>> qr.print_point_algebra_composition_table(lbb_pt_alg) # SEE EDITOR'S NOTE, ABOVE

.. code:: ipython3

    Image(filename='../docs/_static/Lf_Bin_Branching_Pt_Alg_Elements.png')




.. image:: output_47_0.png


