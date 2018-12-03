__author__ = 'gkour'

from universe import Universe
from statistics import Stats
import printing
from configsimulator import ConfigSimulator
import time


def run(msg_queue=None):
    stats = Stats()
    universe = Universe(ConfigSimulator.RACES, stats)

    while universe.pass_time():
        stats.accumulate_step_stats(universe)
        printing.print_step_stats(stats)
        if msg_queue is not None:
            msg_queue.put(stats)
        stats.initialize_inter_step_stats()

        if universe.get_time() % ConfigSimulator.BATCH_SIZE == 0:
            stats.accumulate_epoch_stats(universe)
            printing.print_epoch_stats(stats)

    if ConfigSimulator.CSV_LOGGING:
        printing.dataframe2csv(stats.step_stats_df, ConfigSimulator.CSV_FILE_PATH.format(time.strftime("%Y%m%d-%H%M%S")))


if __name__ == '__main__':
    run()
