__author__ = 'gkour'

from universe import Universe
import numpy as np
from stats import Stats
from dashboard import Dashboard
import printing


def main():
    dash = Dashboard()
    universe = Universe()

    while universe.pass_time():
        step_stats = Stats.collect_step_stats(universe)
        Stats.accumulate_step_stats(step_stats)
        printing.print_step_stats(step_stats)
        dash.update_step_dash(Stats.step_stats_df)

        if universe.get_time() % 10 == 0:
            epoch_stats = Stats.collect_epoch_states(universe)
            Stats.accumulate_epoch_stats(epoch_stats)
            dash.update_epoch_dash(Stats.epoch_stats_df)
            printing.print_epoch_stats(universe)
            Stats.action_dist = np.zeros_like(Stats.action_dist)
            Stats.death_cause = np.zeros_like(Stats.death_cause)



if __name__ == '__main__':
    main()
