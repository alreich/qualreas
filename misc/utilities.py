# Some utilities:

from itertools import combinations, chain

def flatten(list_of_lists):
    """Flatten one level of nesting"""
    return chain.from_iterable(list_of_lists)


# TODO: Make the function list_of_combinations produce an iterator, rather than a list
def list_of_combinations(items, make_sequence):
    """Given a list of items, return a list of all possible combinations of the items.
    Each combination is expressed in the form of whatever sequence building function
    is passed in for make_sequence (e.g., list, set, tuple).  The empty combination is not
    included in the returned result.  If there are n items in the input list, then
    the number of combinations in the result will be 2^n - 1, so becareful not too include
    too many items in the input list of items.

    Example:
    > n = 4
    > items = list(range(4))
    > list_of_combinations(items, set)
     [{0}, {1}, {2}, {3}, {0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}, {0, 1, 2},
      {0, 1, 3}, {0, 2, 3}, {1, 2, 3}, {0, 1, 2, 3}]

    """
    x = []
    for i in items[1:]:
        c = combinations(items, i)
        x.append(list(c))
    combos = list(map(make_sequence, list(flatten(x))))
    combos.append(make_sequence(items))
    return combos
