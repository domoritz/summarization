import unittest

from sample import parse_value, read_sample, Cell
from utils import powerset, get_all_formulas, subsets, tuple_rep


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
    def test_header(self):
        self.assertEqual(read_sample(example)[0], ['x', 'y'])

    def test_relation(self):
        self.assertEqual(
            read_sample(example)[1],
            [frozenset([Cell(attr='x', val=frozenset(['a', 'b'])),
                        Cell(attr='y', val='c')]),
             frozenset([Cell(attr='y', val='c')]),
             frozenset([Cell(attr='y', val='c'),
                        Cell(attr='x', val=('a', 'd'))])]
            )


class TestHelpers(unittest.TestCase):
    def test_subsets(self):
        self.assertEqual(list(subsets([1, 2, 3], 2)),
                         [(1, 2), (1, 3), (2, 3)])

    def test_powerset(self):
        self.assertEqual(list(powerset([1, 2, 3], 1)),
                         [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)])

    def test_all_formuas(self):
        self.assertEqual(get_all_formulas([(1, 2), (2, 3)]),
                         set([frozenset([1, 2]), frozenset([2, 3]),
                              frozenset([2]), frozenset([3]), frozenset([1])]))

    def test_repr(self):
        self.assertEqual(map(tuple_rep, read_sample(example)[1]),
                         ['x:{a b} y:c', 'y:c', 'x:[a d] y:c'])

if __name__ == '__main__':
    unittest.main()
