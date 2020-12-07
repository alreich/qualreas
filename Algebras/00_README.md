# Algebras README

This README is a brief description of the algebras and subdirectories in this directory.

## Time Interval Algebras

File Name | Description
--------- | -----------
Linear_Interval_Algebra.json | Allen's algebra of proper time intervals
Extended_Linear_Interval_Algebra.json | Linear_Interval_Algebra integrated with Time Points
Left_Branching_Interval_Algebra.json | Extended_Linear_Interval_Algebra in Left-Branching Time
Right_Branching_Interval_Algebra.json | Extended_Linear_Interval_Algebra in Right-Branching Time

## Time Point Algebras

File Name | Description
--------- | -----------
Linear_Point_Algebra.json | Algebra of Time Points using relations: <, =, >
Left_Branching_Point_Algebra.json | Linear_Point_Algebra + "left-incomparable" (l~)
Right_Branching_Point_Algebra.json | Linear_Point_Algebra + "right-incomparable" (r~)
Left_Binary_Branching_Point_Algebra.json | Left-branching pt alg, with only binary branches
Right_Binary_Branching_Point_Algebra.json | Right-branching pt alg, with only binary branches

## Spatial Algebras

File Name | Description
--------- | -----------
RCC8_Algebra.json | Region Connection Calculus with 8 spatial relations

## Interval Algebras Derived from Point Algebras

The following 4 algebras were generated as tests, and are the same as the 4 Time Interval Algebras, above.

File Name | Description
--------- | -----------
test_derived_allen_algebra.json | for testing; same as Linear_Interval_Algebra, above
test_derived_extended_interval_algebra.json | for testing; same as Extended_Linear_Interval_Algebra
test_derived_left_branching_interval_algebra.json | for testing; same as Left_Branching_Interval_Algebra
test_derived_right_branching_interval_algebra.json | for testing; same as Right_Branching_Interval_Algebra

The following 4 algebra were generated as experiments.

The 2 "binary" branching interval algebras are similar to the 2 branching interval algebras, above, except that they assume that all branches are binary.  They were derived using the 2 branching point algebras, above.

The 2 "proper" interval algebras are similar to the 2 branching interval algebras, above, except that they assume that all intervals are proper.  That is, no Time Points are allowed.  So, essentially, they are similar to Allen's original algebra of proper intervals except that they allow for right or left branches in time.

File Name | Description
--------- | -----------
test_derived_left_binary_branching_interval_algebra.json | LB interval alg; only binary branches allowed
test_derived_right_binary_branching_interval_algebra.json | RB interval alg; only binary branches allowed
test_derived_left_branching_proper_interval_algebra.json | Left-branching algebra of proper intervals; no pts.
test_derived_right_branching_proper_interval_algebra.json | Right-branching algebra of proper intervals; no pts.

## Work in Progress

File Name | Description
--------- | -----------
2DPointAlgebra.json | NOT FINISHED; An algebra of rectangles (generalized intervals)

## Older Files

* Older_Formats
  * CSV
  * OriginalFormat
  * Text

