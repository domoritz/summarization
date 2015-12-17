from sample import read_sample, three_attr_null, larger_example
from utils import relation_rep, cost, get_cells, potential
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)


def find_incremental(relation, k):
    summary = []

    all_cells = []
    for c in get_cells(relation):
        all_cells.append((potential({c}, set(), relation), c))

    all_cells = [x for x in all_cells if x[0] > 0]
    all_cells.sort()
    all_cells.reverse()

    summary = set()
    best_cost = float("inf")

    while True:
        improved_summary = None
        improved_cost = best_cost

        for i, (p, c) in enumerate(all_cells):
            # potential check
            d = best_cost - improved_cost
            if p < d:
                # can't get better any more so let's abort
                break

            is_better = False

            # try to add new formula
            if len(summary) < k:
                s = summary | {frozenset({c})}
                co = cost(s, relation)
                if co < improved_cost:
                    improved_summary = s
                    improved_cost = co
                    is_better = True

            # try to add cell to existing formula
            for f in summary:
                s = summary - {f}
                s.add(f | {c})
                co = cost(s, relation)
                if co < improved_cost:
                    improved_summary = s
                    improved_cost = co
                    is_better = True

            # update potential
            if is_better and best_cost != float("inf"):
                n = best_cost - improved_cost

                if n != potential({c}, summary, relation):
                    print best_cost, improved_cost, n, potential({c}, summary, relation)
                    print relation_rep(summary)
                    print c
                    assert False
            else:
                n = potential({c}, summary, relation)
            print "update from {} to {}".format(p, n)

            all_cells[i] = (n, c)

        # nothing to improve, stop
        if improved_summary is None:
            break

        summary = improved_summary
        best_cost = improved_cost

        # resort cells
        all_cells = [x for x in all_cells if x[0] > 0]
        all_cells.sort()
        all_cells.reverse()

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

    best_cost, best = run()
    print('Best cost:', best_cost)
    print(relation_rep(best))

    import timeit
    start_time = timeit.default_timer()
    for x in range(1000):
        run()
    elapsed = timeit.default_timer() - start_time
    print(elapsed)
