__author__ = 'gkour'

from universe import Universe
import numpy as np
from stats import Stats
import printing


def run(msg_queue=None):
    statistics = Stats()
    universe = Universe(statistics)

    while universe.pass_time():
        step_stats = statistics.collect_step_stats(universe)
        statistics.accumulate_step_stats(step_stats)
        printing.print_step_stats(step_stats)
        msg_queue.put(statistics)

        if universe.get_time() % 10 == 0:
            epoch_stats = statistics.collect_epoch_states(universe)
            statistics.accumulate_epoch_stats(epoch_stats)
            #printing.print_epoch_stats(statistics)
            statistics.action_dist = np.zeros_like(statistics.action_dist)
            statistics.death_cause = np.zeros_like(statistics.death_cause)


if __name__ == '__main__':
    run()
