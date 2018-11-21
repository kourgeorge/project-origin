__author__ = 'gkour'

from universe import Universe
import numpy as np
import stats
import utils
from dashboard import Dashborad
import config


def main():
    #dash = Dashborad(config.Config.LOG_FILE_PATH)
    universe = Universe()
    step_stats = stats.collect_step_stats(universe)
    utils.print_step_stats(step_stats)
    utils.print_epoch_stats(universe)
    utils.log_step_stats(config.Config.LOG_FILE_PATH, step_stats)

    while universe.pass_time():
        if universe.num_creatures() == 0:
            # step_stats = stats.collect_step_stats(universe)
            # utils.print_step_stats(step_stats)
            # utils.log_step_stats(config.Config.LOG_FILE_PATH, step_stats)
            # utils.print_epoch_stats(universe)
            return

        universe.give_food(round(universe.num_creatures() * 0.7))
        step_stats = stats.collect_step_stats(universe)
        utils.print_step_stats(step_stats)
        utils.log_step_stats(config.Config.LOG_FILE_PATH, step_stats)
        #dash.update(universe.get_time())

        if universe.get_time() % 10 == 0:
            utils.print_epoch_stats(universe)

        stats.action_log = np.zeros_like(stats.action_log)


if __name__ == '__main__':
    main()
