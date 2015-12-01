from sample import read_sample, three_attr_null, larger_example
from utils import relation_rep, cost, get_cells
import logging
from copy import copy


logging.basicConfig()
logger = logging.getLogger(__name__)


def find_incremental(relation, k):
    summary = []

    all_cells = get_cells(relation)

    # TODO: calculate potential, sort

    summary = set()
    best_cost = float("inf")

    while True:
        improved_summary = None
        improved_cost = best_cost

        if len(summary) < k:
            for c in all_cells:
                s = summary | {frozenset({c})}
                co = cost(s, relation)
                if co < improved_cost:
                    improved_summary = s
                    improved_cost = co

        for f in summary:
            for c in all_cells:
                s = summary - {f}
                s.add(f | {c})
                co = cost(s, relation)
                if co < improved_cost:
                    improved_summary = s
                    improved_cost = co

        # nothing to improve, stop
        if improved_summary is None:
            break

        summary = improved_summary
        best_cost = improved_cost

    return best_cost, summary


if __name__ == '__main__':
    logger.setLevel(logging.INFO)

    relation = read_sample(three_attr_null)

    print relation_rep(relation)

    print
    best_cost, best = find_incremental(relation, 3)

    print('Best cost:', best_cost)
    print(relation_rep(best))

    # speedtest
    logger.setLevel(logging.WARN)

    def run():
        relation = read_sample(larger_example)
        return find_incremental(relation, 5)

    # best_cost, best = run()
    # print('Best cost:', best_cost)
    # print(relation_rep(best))

    import timeit
    start_time = timeit.default_timer()
    for x in range(1000):
        run()
    elapsed = timeit.default_timer() - start_time
    print(elapsed)
