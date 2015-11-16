import logging
import itertools

logging.basicConfig()
logger = logging.getLogger(__name__)


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


def get_all_formulas(relation):
    """
    Formulas have to be subsets of tuples in the relation.
    """
    formulas = set()
    for t in relation:
        for f in powerset_set(t, 1):
            formulas.add(f)
    return formulas


def tuple_rep(t):
    r = []
    for c in sorted(t, key=lambda x: x.attr):
        if isinstance(c.val, frozenset):
            v = '{' + (' '.join(c.val)) + '}'
        elif isinstance(c.val, tuple):
            v = '[' + (' '.join(c.val)) + ']'
        else:
            v = c.val
        r.append(c.attr + ':' + v)
    return ' '.join(r)


def relation_rep(r):
    return map(tuple_rep, r)


def satisfies(t, f):
    """ TODO: support more than just primitive values """
    return f.issubset(t)


def cost(formulas, relation):
    # cost of all tuples
    c = 0
    for t in relation:
        remaining = t  # not yet covered cells
        for f in formulas:
            if satisfies(t, f):
                remaining = remaining - f
                if len(remaining) == 0:
                    break  # everything is covered
        c += len(remaining)

    # regularization

    c += sum(map(len, formulas))

    return c
