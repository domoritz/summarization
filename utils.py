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


def satisfies_two(formula, relation):
    """ Returns true if the formula satisfies at least two tuples"""
    count = 0
    for t in relation:
        if satisfies(t, formula):
            count += 1
            if count == 2:
                return True
    return False


def get_all_formulas(relation, filter_support=False):
    """
    Formulas have to be subsets of tuples in the relation.
    """

    formulas = set([frozendict()])
    for t in relation:
        tuple_formulas = set([frozendict()])
        for a, v in t.items():
            new_formulas = set()

            if isinstance(v, frozenset):
                for f in tuple_formulas:
                    # add all possible subsets to all formulas
                    for subset in powerset(v, 1):
                        nf = {x: f[x] for x in f.keys()}
                        nf[a] = frozenset(subset)
                        new_formulas.add(frozendict(nf))
            elif isinstance(v, tuple):
                print("not yet supported")
            else:
                for f in tuple_formulas:
                    # add single value to all formulas
                    nf = {x: f[x] for x in f.keys()}
                    nf[a] = v
                    new_formulas.add(frozendict(nf))
            tuple_formulas.update(new_formulas)
        formulas.update(tuple_formulas)

    # if a formula doesn't satisfy at least two tuples, it is not worth including
    if filter_support:
        formulas = set(filter(lambda f: satisfies_two(f, relation), formulas))

    return formulas


def tuple_rep(t):
    r = []
    for attr, val in sorted(t.items(), key=lambda x: x[0]):
        if isinstance(val, frozenset):
            v = '{' + (' '.join(val)) + '}'
        elif isinstance(val, tuple):
            v = '[' + (' '.join(val)) + ']'
        else:
            v = val
        r.append(attr + ':' + v)
    return ' '.join(r)


def relation_rep(r):
    return map(tuple_rep, r)


def satisfies(t, f):
    for a, v in f.items():
        if a not in t:
            # attribute only in the formula
            return False

        if isinstance(v, frozenset):
            if not v.issubset(t[a]):
                return False
        elif isinstance(v, tuple):
            tv = t[a]
            for i in range(len(v)):
                if v[i] != tv[i]:
                    return False
        else:
            if v != t[a]:
                return False
    return True


def cost(formulas, relation):
    # cost of all tuples
    c = 0

    for t in relation:
        satisfying = filter(lambda f: satisfies(t, f), formulas)
        for a, v in t.iteritems():
            if isinstance(v, frozenset):
                nc = len(v)
                remaining = set(v)
            elif isinstance(v, tuple):
                nc = len(v)
            else:
                nc = 1

            for f in satisfying:
                if a not in f:
                    continue  # this formula does not specify any value for a
                if isinstance(v, frozenset):
                    assert(f[a].issubset(v))
                    remaining.difference_update(f[a])
                    nc = len(remaining)
                elif isinstance(v, tuple):
                    fv = f[a]
                    for i in range(len(v)):
                        if v[i] != fv[i]:
                            if i < nc:
                                nc = i
                else:
                    if f[a] == v:
                        nc = 0

                # early break
                if nc == 0:
                    break

            c += nc

    # regularization
    c += sum(map(len, formulas))

    return c


# from https://code.activestate.com/recipes/414283-frozen-dictionaries/
class frozendict(dict):
    def _blocked_attribute(obj):
        raise AttributeError('A frozendict cannot be modified.')
    _blocked_attribute = property(_blocked_attribute)

    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute

    def __new__(cls, *args, **kw):
        new = dict.__new__(cls)
        dict.__init__(new, *args, **kw)
        return new

    def __init__(self, *args, **kw):
        pass

    def __hash__(self):
        try:
            return self._cached_hash
        except AttributeError:
            h = self._cached_hash = hash(tuple(sorted(self.items())))
            return h

    def __repr__(self):
        return "frozendict(%s)" % dict.__repr__(self)
