Temporal Reasoning about Time Intervals and Time Points
=======================================================

This notebook presents a very simple example of a ``qualreas.Network``,
including its format as a Python dictionary or JSON file.

.. code:: ipython3

    import qualreas as qr
    import os

--------------

Algebra 
--------

This example uses the temporal interval & point algebra,
Extended_Linear_Interval_Algebra, defined by Reich in `“Intervals,
Points, and Branching Time”,
1994 <https://www.researchgate.net/publication/220810644_Intervals_Points_and_Branching_Time>`__,
that extends Allen’s algebra of *proper time intervals* to include *time
points*.

The extension is accomplished in two ways:

1. Five additional relations involving *time points*\ ”: **PE**, **PF**,
   **PFI**, **PS**, **PSI**
2. Extension of the domains and/or ranges of existing relations from
   Allen’s algebra (see the last two columns in the table below)

.. code:: ipython3

    algX = qr.Algebra(os.path.join(qr.ALGEBRA_DIR, "Extended_Linear_Interval_Algebra.json"))
    algX.summary()


.. parsed-literal::

      Algebra Name: Extended_Linear_Interval_Algebra
       Description: Extension of Allen's algebra to include points and intervals
     Equality Rels: E|PE
         Relations:
                NAME (SYMBOL)         CONVERSE (ABBREV)  REFLEXIVE  SYMMETRIC TRANSITIVE   DOMAIN        RANGE
                 Before (  B)               After ( BI)    False      False       True    Pt|PInt       Pt|PInt
                  After ( BI)              Before (  B)    False      False       True    Pt|PInt       Pt|PInt
                 During (  D)            Contains ( DI)    False      False       True    Pt|PInt          PInt
               Contains ( DI)              During (  D)    False      False       True       PInt       Pt|PInt
                 Equals (  E)              Equals (  E)     True       True       True       PInt          PInt
               Finishes (  F)         Finished-by ( FI)    False      False       True       PInt          PInt
            Finished-by ( FI)            Finishes (  F)    False      False       True       PInt          PInt
                  Meets (  M)              Met-By ( MI)    False      False      False       PInt          PInt
                 Met-By ( MI)               Meets (  M)    False      False      False       PInt          PInt
               Overlaps (  O)       Overlapped-By ( OI)    False      False      False       PInt          PInt
          Overlapped-By ( OI)            Overlaps (  O)    False      False      False       PInt          PInt
           Point-Equals ( PE)        Point-Equals ( PE)     True       True       True         Pt            Pt
         Point-Finishes ( PF)   Point-Finished-By (PFI)    False      False      False         Pt          PInt
      Point-Finished-By (PFI)      Point-Finishes ( PF)    False      False      False       PInt            Pt
           Point-Starts ( PS)    Point-Started-By (PSI)    False      False      False         Pt          PInt
       Point-Started-By (PSI)        Point-Starts ( PS)    False      False      False       PInt            Pt
                 Starts (  S)          Started-By ( SI)    False      False       True       PInt          PInt
             Started-By ( SI)              Starts (  S)    False      False       True       PInt          PInt
    
    Domain & Range Abbreviations:
       Pt = Point
     PInt = Proper Interval


--------------

Network
-------

A *constraint network* can be created from (or saved to) a Python
dictionary or JSON file.

The dictionary below defines four entities (*nodes*) using the two
available classes/types in the extension of Allen’s algebra: *Point* and
*ProperInterval*. \* *Monday*, *MondayPM*, and *Tuesday* are defined to
be of type *ProperInterval* \* For demonstration purposes,
*MondayMidnight*\ ’s type is left ambiquous, it is a *Point* or a
*ProperInterval*

Three temporal constraints (*edges*) are also defined: \* *Monday* M
*Tuesday* \* *MondayMidnight* PF *Monday* \* *MondayPM* F *Monday*

The second constraint, above, implies that *MondayMidnight* is *Point*,
but once contraint propagation is applied to the network this fact will
become explicit.

Here’s the network.

Note the following: \* Constraints (*edges*) are written as triples,
[Tail, Head, Constraint], where *Tail* is the “from node” and *Head* is
the “to node”. \* The value of the ‘algebra’ key must be the exact
string name of the JSON file used by the network, but without the
‘.json’ extension.

.. code:: ipython3

    time_net_dict = {
        'name': 'Simple Temporal Constraint Network',
        'algebra': 'Extended_Linear_Interval_Algebra',
        'description': 'A simple example of a Network of Time Points integrated with Time Intervals',
        'nodes': [
            ['Monday', ['ProperInterval']],
            ['MondayMidnight', ['ProperInterval', 'Point']],
            ['Tuesday', ['ProperInterval']],
            ['MondayPM', ['ProperInterval']]
        ],
        'edges': [
            ['Monday', 'Tuesday', 'M'],
            ['MondayMidnight', 'Monday', 'PF'],
            ['MondayPM', 'Monday', 'F']
        ]
    }

Here’s the ``Network`` constructor and a summary of the network:

.. code:: ipython3

    time_net = qr.Network(algebra_path=qr.ALGEBRA_DIR, network_dict=time_net_dict)
    
    time_net.summary()


.. parsed-literal::

    
    Description: A simple example of a Network of Time Points integrated with Time Intervals
    
    Simple Temporal Constraint Network: 4 nodes, 10 edges
      Algebra: Extended_Linear_Interval_Algebra
      Monday:['ProperInterval']
        => Monday: E
        => Tuesday: M
        => MondayMidnight: PFI
        => MondayPM: FI
      Tuesday:['ProperInterval']
        => Tuesday: E
      MondayMidnight:['ProperInterval', 'Point']
        => MondayMidnight: E|PE
      MondayPM:['ProperInterval']
        => MondayPM: E


--------------

Propagation
-----------

.. code:: ipython3

    ok = time_net.propagate()
    
    if ok:
        print("The network is consistent.  Here's a summary:")
        # time_net.summary(show_all=True)
        time_net.summary()
    else:
        print("The network is inconsistent.")


.. parsed-literal::

    The network is consistent.  Here's a summary:
    
    Description: A simple example of a Network of Time Points integrated with Time Intervals
    
    Simple Temporal Constraint Network: 4 nodes, 16 edges
      Algebra: Extended_Linear_Interval_Algebra
      Monday:['ProperInterval']
        => Monday: E
        => Tuesday: M
        => MondayMidnight: PFI
        => MondayPM: FI
      Tuesday:['ProperInterval']
        => Tuesday: E
        => MondayMidnight: PSI
        => MondayPM: MI
      MondayMidnight:['Point']
        => MondayMidnight: PE
        => MondayPM: PF
      MondayPM:['ProperInterval']
        => MondayPM: E


--------------

Summary
-------

Note that, in **time_net_dict**, *MondayMidnight*\ ’s relation to
*Monday* is specified as:

   *MondayMidnight PF Monday*

This of course implies that *MondayMidnight* is a *Point*, but it
doesn’t make that explicit.

In *time_net_dict*, the line *‘MondayMidnight’, [‘ProperInterval’,
‘Point’]]* allows for the possibility that *MondayMidnight* is a
*ProperInterval*.

But, after propagation the network shows that *MondayMidnight* is a
*Point*, and only a *Point*, and it is the end point (*Point-Finishes*)
of the interval, *Monday*.

The following was also inferred:

   *Tuesday PSI MondayMidnight*

That is, *Tuesday* is started by (*Point-Started-By*) the point
*MondayMidnight*

We’ve also inferred the corresponding converses of these statements
(i.e., using the relations *PFI* and *PSI*).

Here’s a summary of the propagated network showing all constraints:

.. code:: ipython3

    time_net.summary(show_all=True)


.. parsed-literal::

    
    Description: A simple example of a Network of Time Points integrated with Time Intervals
    
    Simple Temporal Constraint Network: 4 nodes, 16 edges
      Algebra: Extended_Linear_Interval_Algebra
      Monday:['ProperInterval']
        => Monday: E
        => Tuesday: M
        => MondayMidnight: PFI
        => MondayPM: FI
      Tuesday:['ProperInterval']
        => Tuesday: E
        => Monday: MI
        => MondayMidnight: PSI
        => MondayPM: MI
      MondayMidnight:['Point']
        => MondayMidnight: PE
        => Monday: PF
        => Tuesday: PS
        => MondayPM: PF
      MondayPM:['ProperInterval']
        => MondayPM: E
        => Monday: F
        => Tuesday: M
        => MondayMidnight: PFI

