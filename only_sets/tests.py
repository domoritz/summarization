import unittest

from sample import parse_value, read_sample, build_tuple, Cell, three_attr_null
from utils import (powerset, get_all_formulas, subsets,
                   tuple_rep, relation_rep, satisfies, cost)


example = """x, y
{a b}, c
, c
[a d], c"""


class TestParse(unittest.TestCase):
    def test_null(self):
        self.assertEqual(parse_value(' '), None)

    def test_simple(self):
        self.assertEqual(parse_value(' ab '), 'ab')

    def test_set(self):
        self.assertEqual(parse_value(' {foo bar baz } '),
                         frozenset(['foo', 'bar', 'baz']))

    def test_list(self):
        self.assertEqual(parse_value(' [foo bar baz ] '),
                         ('foo', 'bar', 'baz'))


class TestRead(unittest.TestCase):
    def test_relation(self):
        self.assertEqual(
            read_sample(example),
            [frozenset([Cell(attribute='x', sequence=0, value='a'),
                        Cell(attribute='x', sequence=0, value='b'),
                        Cell(attribute='y', sequence=0, value='c')]),
             frozenset([Cell(attribute='y', sequence=0, value='c')]),
             frozenset([Cell(attribute='x', sequence=0, value='a'),
                        Cell(attribute='y', sequence=0, value='c'),
                        Cell(attribute='x', sequence=1, value='d')])])


class TestHelpers(unittest.TestCase):
    def test_subsets(self):
        self.assertEqual(list(subsets([1, 2, 3], 2)),
                         [(1, 2), (1, 3), (2, 3)])

    def test_powerset(self):
        self.assertEqual(list(powerset([1, 2, 3], 1)),
                         [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)])

    def test_all_formulas(self):
        self.assertEqual(
            get_all_formulas(read_sample('x,y\n1,2\n3,4')),
            {frozenset([Cell(attribute='x', sequence=0, value='1')]),
             frozenset([Cell(attribute='x', sequence=0, value='3')]),
             frozenset([Cell(attribute='y', sequence=0, value='4')]),
             frozenset([Cell(attribute='x', sequence=0, value='1'), Cell(attribute='y', sequence=0, value='2')]),
             frozenset([Cell(attribute='y', sequence=0, value='2')]),
             frozenset([Cell(attribute='y', sequence=0, value='4'), Cell(attribute='x', sequence=0, value='3')])})

        self.assertEqual(
            get_all_formulas(read_sample('x\n{1 2}\n{3 4}')),
            {frozenset([Cell(attribute='x', sequence=0, value='3'), Cell(attribute='x', sequence=0, value='4')]),
             frozenset([Cell(attribute='x', sequence=0, value='4')]),
             frozenset([Cell(attribute='x', sequence=0, value='1')]),
             frozenset([Cell(attribute='x', sequence=0, value='1'), Cell(attribute='x', sequence=0, value='2')]),
             frozenset([Cell(attribute='x', sequence=0, value='3')]),
             frozenset([Cell(attribute='x', sequence=0, value='2')])})

    def test_cost(self):
        self.assertEqual(cost(formulas=read_sample('x, y\n1\n, 4'),
                              relation=read_sample('x, y\n1, 2\n1, 4\n1, 4')),
                         3)

        self.assertEqual(cost(formulas=read_sample('x\n{1}\n{4}'),
                              relation=read_sample('x\n{1 2}\n{1 4}\n{1 4}')),
                         3)

        self.assertEqual(cost(formulas=read_sample('x,y,z\na,b,\n,,c'),
                              relation=read_sample(three_attr_null)),
                         6)

    def test_repr(self):
        self.assertEqual(map(tuple_rep, read_sample(example)),
                         ['x[0]:a x[0]:b y[0]:c', 'y[0]:c', 'x[0]:a x[1]:d y[0]:c'])

        self.assertEqual(relation_rep(read_sample(example)),
                         'x[0]:a x[0]:b y[0]:c\ny[0]:c\nx[0]:a x[1]:d y[0]:c')

    def test_satisfies(self):
        # simple tuples
        self.assertEqual(satisfies(t=build_tuple('a,b', ['x', 'y']),
                                   f=build_tuple('a,b', ['x', 'y'])), True)
        self.assertEqual(satisfies(t=build_tuple('a,b', ['x', 'y']),
                                   f=build_tuple('a,', ['x', 'y'])), True)
        self.assertEqual(satisfies(t=build_tuple('a,c', ['x', 'y']),
                                   f=build_tuple('a,b', ['x', 'y'])), False)

        # set tuples
        self.assertEqual(satisfies(t=build_tuple('{a}', ['x']),
                                   f=build_tuple('{}', ['x'])), True)

        self.assertEqual(satisfies(t=build_tuple('{a b}', ['x']),
                                   f=build_tuple('{a b}', ['x'])), True)

        self.assertEqual(satisfies(t=build_tuple('{a b c}', ['x']),
                                   f=build_tuple('{a b}', ['x'])), True)

        self.assertEqual(satisfies(t=build_tuple('{a b}', ['x']),
                                   f=build_tuple('{a b c}', ['x'])), False)

        # prefix tuples
        self.assertEqual(satisfies(t=build_tuple('[a]', ['x']),
                                   f=build_tuple('[]', ['x'])), True)

        self.assertEqual(satisfies(t=build_tuple('[a b]', ['x']),
                                   f=build_tuple('[a]', ['x'])), True)

        self.assertEqual(satisfies(t=build_tuple('[a b]', ['x']),
                                   f=build_tuple('[a b]', ['x'])), True)

        self.assertEqual(satisfies(t=build_tuple('[a b c]', ['x']),
                                   f=build_tuple('[a b]', ['x'])), True)

        self.assertEqual(satisfies(t=build_tuple('[a b]', ['x']),
                                   f=build_tuple('[a c b]', ['x'])), False)

if __name__ == '__main__':
    unittest.main()
