__author__ = 'gkour'

import numpy as np
from config import Config
from collections import OrderedDict
import aiq


class Stats:
    action_dist = np.zeros(Config.ConfigBrain.ACTION_SIZE)  # [Left Right Eat Mate Fight]
    death_cause = [0, 0, 0]  # [Fatigue Fight Elderly]

    @staticmethod
    def collect_step_stats(universe):
        return OrderedDict([
            ('Time', universe.get_time()),
            ('Population', universe.num_creatures()),
            ('IDs', universe.get_creatures_counter()),
            ('Age', np.round(np.nanmean([creature.age() for creature in universe.get_all_creatures()]))),
            ('MaxAge', np.round(np.nanmean([creature.max_age() for creature in universe.get_all_creatures()]), 2)),
            ('HLayer',
             np.round(np.mean([creature.brain_hidden_layer() for creature in universe.get_all_creatures()]), 2)),
            ('LFreq',
             np.round(np.mean([creature.learning_frequency() for creature in universe.get_all_creatures()]), 2)),
            ('LRate', np.round(np.mean([creature.learning_rate() for creature in universe.get_all_creatures()]) *
                               (1 / Config.ConfigBrain.BASE_LEARNING_RATE), 2)),
            ('gamma', np.round(np.mean([creature.gamma() for creature in universe.get_all_creatures()]), 2)),
            ('VRange', np.round(np.mean([creature.vision_range() for creature in universe.get_all_creatures()]), 2)),
            ('AIQ', aiq.population_aiq_dist(universe.get_all_creatures()))
        ])

    @staticmethod
    def collect_epoch_states(universe):
        return OrderedDict([
            ('Time', universe.get_time()),
            ('Population dist', np.histogram([creature.age() for creature in universe.get_all_creatures()],
                                             bins=[0, Config.ConfigBiology.MATURITY_AGE,
                                                   2 * Config.ConfigBiology.MATURITY_AGE, 200])[0]),
            ('Death Cause [FVE]', Stats.death_cause),
            ('Food Supply', universe.get_food_distribution()),
            ('Creatures', universe.get_creatures_distribution()),
            ('Action Dist [LREMF]', np.round(np.array(Stats.action_dist) / sum(Stats.action_dist), 2))
        ])
