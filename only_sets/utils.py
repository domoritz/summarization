import itertools
import copy


def tuple_rep(t):
    r = []
    for attr, seq, val in sorted(t):
        r.append('{}[{}]:{}'.format(attr, seq, val))
    return ' '.join(r)


def relation_rep(r):
    return '\n'.join(map(tuple_rep, r))


def powerset(iterable, min_size=0):
    """ Get the powerset of any iterator (all possible subsets).
    Returns an iterator. """
    xs = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(xs, n) for n in range(min_size, len(xs)+1))


def powerset_set(iterable, min_size):
    return map(frozenset, powerset(iterable, min_size))


def subsets(iterable, m):
    """ Get all subsets of size m """
    return itertools.combinations(iterable, m)


def get_all_formulas(relation, filter_support=False):
    formulas = set()

    for t in relation:
        for possible in powerset_set(t, 1):
            if not filter_support or satisfies_two(possible, relation):
                formulas.add(possible)

    return formulas


def satisfies(t, f):
    return f.issubset(t)


def satisfies_two(formula, relation):
    """ Returns true if the formula satisfies at least two tuples"""
    count = 0
    for t in relation:
        if satisfies(t, formula):
            count += 1
            if count == 2:
                return True
    return False


def cost(formulas, relation):
    c = 0

    # cost of all tuples
    for t in relation:
        tc = set(t)
        for f in formulas:
            if satisfies(t, f):
                tc.difference_update(f)
        c += len(tc)

    # regularization
    c += sum(map(len, formulas))

    return c
