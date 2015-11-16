from pprint import pprint
from collections import namedtuple

Cell = namedtuple('Cell', 'attr, val')

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


def parse_value(s):
    s = s.strip()
    if s.startswith('{'):
        return frozenset(s.strip('{').strip('}').split())
    if s.startswith('['):
        return tuple(s.strip('[').strip(']').split())
    if len(s) == 0:
        return None
    return s


def read_sample(s):
    relation = []

    rows = s.split('\n')

    sort = map(str.strip, rows[0].split(','))

    for row in rows[1:]:
        p = row.split(',')
        p = map(parse_value, p)

        t = []  # tuple
        for x in zip(sort, p):
            if x[1] is not None:
                t.append(Cell(attr=x[0], val=x[1]))
        relation.append(frozenset(t))

    return sort, relation

if __name__ == '__main__':
    pprint(read_sample(three_attr_null))
