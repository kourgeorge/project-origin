__author__ = 'gkour'

import numpy as np
from config import Config
from collections import OrderedDict
import aiq

action_log = np.zeros(Config.ConfigBrain.ACTION_SIZE)  #[Left Right Eat Mate Fight]
death_cause = [0, 0, 0]  #[Fatigue Fight Elderly]


def collect_step_stats(universe):
    return OrderedDict([
        ('Time', universe.get_time()),
        ('Population', universe.num_creatures()),
        ('IDs', universe.get_creatures_counter()),
        ('Age', np.round(np.nanmean([creature.age() for creature in universe.get_all_creatures()]))),
        ('MaxAge', np.round(np.nanmean([creature.max_age() for creature in universe.get_all_creatures()]), 2)),
        ('Hidden Layer',
            np.round(np.mean([creature.brain_hidden_layer() for creature in universe.get_all_creatures()]), 2)),
        ('Learn Freq',
            np.round(np.mean([creature.learning_frequency() for creature in universe.get_all_creatures()]), 2)),
        ('Learn Rate', np.round(np.mean([creature.learning_rate() for creature in universe.get_all_creatures()]) *
                                (1 / Config.ConfigBrain.BASE_LEARNING_RATE), 2)),
        ('Vision Range', np.round(np.mean([creature.vision_range() for creature in universe.get_all_creatures()]), 2)),
        ('Artificial IQ', aiq.population_aiq_dist(universe.get_all_creatures()))
    ])