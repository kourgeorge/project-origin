__author__ = 'gkour'

from universe import Universe
import numpy as np
from stats import Stats
import utils
from dashboard import Dashborad
import config


def main():
    #dash = Dashborad(config.Config.LOG_FILE_PATH)
    universe = Universe()
    utils.print_step_stats(universe)
    utils.print_epoch_stats(universe)
    utils.log_step_stats(config.Config.LOG_FILE_PATH, universe)

    while universe.pass_time():
        if universe.num_creatures() == 0:
            # step_stats = stats.collect_step_stats(universe)
            # utils.print_step_stats(step_stats)
            # utils.log_step_stats(config.Config.LOG_FILE_PATH, step_stats)
            # utils.print_epoch_stats(universe)
            return

        universe.give_food(round(universe.num_creatures() * 0.7))
        utils.print_step_stats(universe)
        utils.log_step_stats(config.Config.LOG_FILE_PATH, universe)
        #dash.update(universe.get_time())

        if universe.get_time() % 10 == 0:
            utils.print_epoch_stats(universe)

        Stats.action_dist = np.zeros_like(Stats.action_dist)
        Stats.death_cause = np.zeros_like(Stats.death_cause)


if __name__ == '__main__':
    main()
