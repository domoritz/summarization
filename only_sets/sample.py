from pprint import pprint
from collections import namedtuple


simple = """x, y
a, b"""

one_attr = """x
{a b c}
{a b c}
{a b d}
{a d}"""

three_attr_null = """x, y, z
a, b, c
a, b, c
a, b, d
a, d"""

two_attr = """x, y
a, b
a, b
a, b
a, c
d, c
e, c"""

larger_example = """x, y, z
a, b, {l m n}
a, b, {l m n}
a, b, {l m n}
a, b, {l n}
a, b, {l n}
a, b, {l n}
c, d, {l n o}
c, d, {n o p}
c, e, {n o p}
c, e, {n o p}
c, e, {n o p}
"""


Cell = namedtuple('Cell', 'attribute, sequence, value')


def parse_value(s):
    s = s.strip()
    if s.startswith('{'):
        return frozenset(s.strip('{').strip('}').split())
    if s.startswith('['):
        return tuple(s.strip('[').strip(']').split())
    if len(s) == 0:
        return None
    return s


def build_tuple(s, sort):
    p = map(parse_value, s.split(','))

    t = set()  # tuple
    for attribute, value in zip(sort, p):
        if value is not None:
            if isinstance(value, frozenset):
                for v in value:
                    t.add(Cell(attribute, 0, v))
            elif isinstance(value, tuple):
                for i, v in enumerate(value):
                    t.add(Cell(attribute, i, v))
            else:
                t.add(Cell(attribute, 0, value))
    return frozenset(t)


def read_sample(s):
    relation = []

    rows = s.split('\n')

    sort = map(str.strip, rows[0].split(','))

    for row in rows[1:]:
        relation.append(build_tuple(row, sort))

    return relation


if __name__ == '__main__':
    from utils import relation_rep

    print(build_tuple('{a b}, c', ['x', 'y']))

    pprint(read_sample(three_attr_null))
