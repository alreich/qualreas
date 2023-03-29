Temporal Reasoning about Time Intervals and Time Points
=======================================================

.. code:: ipython3

    import qualreas as qr
    import os
    
    qr_path = os.path.join(os.getenv('PYPROJ'), 'qualreas')
    alg_dir = os.path.join(qr_path, "Algebras")

An Example of Temporal Reasoning 
---------------------------------

Here we’ll use the temporal interval & point algebra,
Extended_Linear_Interval_Algebra, defined by Reich in `“Intervals,
Points, and Branching Time”,
1994 <https://www.researchgate.net/publication/220810644_Intervals_Points_and_Branching_Time>`__

This algebra extends Allen’s algebra of Proper Time Intervals to include
Time Points, so those two different ontology classes are permitted.

The relation, “PF”, is “PointFinishes”, “PS” is “PointStarts”, and “PE”
is “PointEquals”. “PFI” & “PSI” are the converses of “PF” and “PS”,
respectively.

For example, \* MondayMidnight PF Monday \* MondayMidnight PS Tuesday \*
MondayMidnight PE MondayMidnight

In the following constraint network (in dictionary form) we create four
temporal entities. We’ve also specified the ontology classes the
entities are allowed to belong to: \* Monday a ProperInterval \*
MondayMidnight a ProperInterval or Point \* Tuesday a ProperInterval \*
MondayPM a ProperInterval

And we create three constraints between the temporal entities: \* Monday
M Tuesday \* MondayMidnight PF Monday \* MondayPM F Monday

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

Now we’ll use the dictionary to instantiate a Constraint Network Object

.. code:: ipython3

    time_net = qr.Network(algebra_path=alg_dir, network_dict=time_net_dict)
    
    print(time_net.description)
    
    time_net.summary()


.. parsed-literal::

    A simple example of a Network of Time Points integrated with Time Intervals
    
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


And now, we’ll propagate the network’s constraints and summarize the
result, showing all edges.

.. code:: ipython3

    ok = time_net.propagate()
    
    if ok:
        print("The network is consistent.  Here's a summary:")
        time_net.summary(show_all=True)
    else:
        print("The network is inconsistent.")


.. parsed-literal::

    The network is consistent.  Here's a summary:
    
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


Note that with regard to the point, MondayMidnight as defined in
time_net_dict, above, we only specified:

   MondayMidnight PF Monday

That is, MondayMidnight is the end point (PointFinishes) of the
interval, Monday.

After propagation, we’ve inferred that:

   MondayMidnight PS Tuesday

That is, MondayMidnight is the begin point (PointStarts) of the
interval, Tuesday.

We’ve also inferred the corresponding converses of these statements
(i.e., using the relations PFI and PSI).

Finally, although we defined MondayMidnight as being either a
ProperInterval or a Point, after propagation it is determined that it
can only be a Point.
