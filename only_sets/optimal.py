from sample import read_sample, three_attr_null, larger_example
from utils import relation_rep, get_all_formulas, subsets, cost
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)


def find_optimum(relation, k):

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

    print relation_rep(relation)

    best_cost, best = find_optimum(relation, 3)

    print('Best cost:', best_cost)
    for s in map(relation_rep, [x[1] for x in best]):
        print(s)

    # speedtest
    # logger.setLevel(logging.WARN)

    # def run():
    #     relation = read_sample(larger_example)
    #     return find_optimum(relation, 5)

    # best_cost, best = run()
    # print('Best cost:', best_cost)
    # for s in map(relation_rep, [x[1] for x in best]):
    #     print(s)
    #     print

    # import timeit
    # start_time = timeit.default_timer()
    # for x in range(1):
    #     run()
    # elapsed = timeit.default_timer() - start_time
    # print(elapsed)
