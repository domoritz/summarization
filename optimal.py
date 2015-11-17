import logging
from utils import get_all_formulas, relation_rep, subsets, cost
from pprint import pprint
from sample import read_sample, three_attr_null, larger_example


logging.basicConfig()
logger = logging.getLogger(__name__)


def find_optimum(relation, k):
    """ Finds the optimum set of formulas and its cost.
    This method generates all formulas, all subsets of formulas and
    then calculates the cost for every one of them. This can be very slow."""

    formulas = get_all_formulas(relation, True)

    logger.info('# formulas: %s', len(formulas))

    logger.debug('possible formulas: %s', relation_rep(formulas))

    all_subsets = list(subsets(formulas, k))

    logger.info('# subsets: %s', len(all_subsets))

    subset_costs = map(lambda x: cost(x, relation), all_subsets)

    ordered = [x for x in sorted(zip(subset_costs, all_subsets), key=lambda x: x[0])]

    best_cost = ordered[0][0]
    best = filter(lambda x: x[0] == best_cost, ordered)

    return best_cost, best


if __name__ == '__main__':
    logger.setLevel(logging.INFO)

    relation = read_sample(three_attr_null)
    best_cost, best = find_optimum(relation, 2)

    print('Best cost:', best_cost)
    for s in map(relation_rep, [x[1] for x in best]):
        print(s)

    # def run():
    #     relation = read_sample(larger_example)
    #     best_cost, best = find_optimum(relation, 4)

    # import timeit
    # start_time = timeit.default_timer()
    # for x in range(10):
    #     run()
    # elapsed = timeit.default_timer() - start_time
    # print(elapsed)
