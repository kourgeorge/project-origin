__author__ = 'gkour'

from universe import Universe
from statistics import Stats
import printing


def run(msg_queue=None):
    stats = Stats()
    universe = Universe(stats)

    while universe.pass_time():
        step_stats = stats.collect_step_stats(universe)
        stats.accumulate_step_stats(step_stats)
        printing.print_step_stats(step_stats)
        msg_queue.put(stats)

        if universe.get_time() % 10 == 0:
            epoch_stats = stats.collect_epoch_states(universe)
            stats.accumulate_epoch_stats(epoch_stats)
            #printing.print_epoch_stats(statistics)
            stats.initialize_inter_epoch_stats()


if __name__ == '__main__':
    run()
