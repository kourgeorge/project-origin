__author__ = 'gkour'

import numpy as np
from config import Config
from collections import OrderedDict
import aiq
import pandas as pd
import utils


class Stats:
    action_dist = np.zeros(Config.ConfigBrain.ACTION_SIZE)  # [Left Right Eat Mate Fight]
    death_cause = [0, 0, 0]  # [Fatigue Fight Elderly]
    step_stats_df = pd.DataFrame()
    epoch_stats_df = pd.DataFrame()
    step_ready_for_ui = False
    epoch_ready_for_ui = False

    @staticmethod
    def accumulate_step_stats(step_stats_dict):
        temp_df = pd.DataFrame([step_stats_dict], columns=step_stats_dict.keys())
        Stats.step_stats_df = pd.concat([Stats.step_stats_df, temp_df], axis=0).reset_index(drop=True)
        Stats.step_ready_for_ui = True

    @staticmethod
    def collect_step_stats(universe):
        return OrderedDict([
            ('Time', universe.get_time()),
            ('Population', universe.num_creatures()),
            ('IDs', universe.get_creatures_counter()),
            ('Age', np.round(utils.emptynanmean([creature.age() for creature in universe.get_all_creatures()]))),
            ('MaxAge',
             np.round(utils.emptynanmean([creature.max_age() for creature in universe.get_all_creatures()]), 2)),
            ('HLayer',
             np.round(utils.emptynanmean([creature.brain_hidden_layer() for creature in universe.get_all_creatures()]), 2)),
            ('LFreq',
             np.round(utils.emptynanmean([creature.learning_frequency() for creature in universe.get_all_creatures()]), 2)),
            ('LRate', np.round(utils.emptynanmean([creature.learning_rate() for creature in universe.get_all_creatures()]) *
                               (1 / Config.ConfigBrain.BASE_LEARNING_RATE), 2)),
            ('gamma', np.round(utils.emptynanmean([creature.gamma() for creature in universe.get_all_creatures()]), 2)),
            ('VRange', np.round(utils.emptynanmean([creature.vision_range() for creature in universe.get_all_creatures()]), 2)),
            ('AIQ', aiq.population_aiq(universe.get_all_creatures()))
        ])

    @staticmethod
    def accumulate_epoch_stats(epoch_stats_dict):
        temp_df = pd.DataFrame([epoch_stats_dict], columns=epoch_stats_dict.keys())
        Stats.epoch_stats_df = pd.concat([Stats.epoch_stats_df, temp_df], axis=0).reset_index(drop=True)
        Stats.epoch_ready_for_ui = True

    @staticmethod
    def collect_epoch_states(universe):
        return OrderedDict([
            ('Time', universe.get_time()),
            ('Population dist', np.histogram([creature.age() for creature in universe.get_all_creatures()],
                                             bins=[0, Config.ConfigBiology.MATURITY_AGE,
                                                   2 * Config.ConfigBiology.MATURITY_AGE, 200])[0]),
            ('Population aiq dist', aiq.population_aiq_dist(universe.get_all_creatures())),
            ('Death Cause [FVE]', Stats.death_cause),
            ('Food Supply', universe.get_food_distribution()),
            ('Creatures', universe.get_creatures_distribution()),
            ('Action Dist [LREMF]', np.round(np.array(Stats.action_dist) / sum(Stats.action_dist), 2))
        ])
