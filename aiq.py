__author__ = 'gkour'

import numpy as np
from config import Config
import utils
from creature_actions import Actions
from itertools import chain
import random

repetitions = 3


def population_aiq(creatures):
    sample_creatures = random.sample(creatures, utils.safe_log(len(creatures)))
    all_aiq = [test_aiq(creature, repetitions) for creature in sample_creatures]
    return np.round(utils.emptynanmean(all_aiq), 2)


def population_aiq_dist(creatures):
    bounds = [Config.ConfigBiology.BASE_DYING_AGE / 3, 2 * Config.ConfigBiology.BASE_DYING_AGE / 3]
    young = [test_aiq(creature, repetitions) for creature in creatures if creature.age() <= bounds[0]]
    adult = [test_aiq(creature, repetitions) for creature in creatures if bounds[0] < creature.age() <= bounds[1]]
    old = [test_aiq(creature, repetitions) for creature in creatures if bounds[1] < creature.age()]

    return np.round([utils.emptynanmean(young), utils.emptynanmean(adult), utils.emptynanmean(old)], 2)


def test_aiq(creature, test_size=3):
    score = 0
    scenarios = [haven_left, haven_right, haven_inplace, haven_up, haven_down]
    for i in range(test_size):
        test_state, optimal_action = scenarios[i % 3](creature.vision_range())
        decision = Actions.index_to_enum(creature.brain().act(test_state))
        score += 1 if decision == optimal_action else 0
    return score / test_size


def haven_inplace(vision_range):
    ''' Haven cell in current location.'''
    energy = 3
    age = 3
    internal_state = [energy, age]

    food = np.zeros(shape=(2*vision_range + 1, 2*vision_range + 1))
    creatures = np.ones(shape=(2*vision_range + 1, 2*vision_range + 1)) * 20

    food[vision_range][vision_range] = 20
    creatures[vision_range][vision_range] = 0

    return list(chain.from_iterable(creatures)) + list(chain.from_iterable(food)) + internal_state, Actions.EAT


def haven_right(vision_range):
    ''' Haven cell on the right'''
    energy = 3
    age = 3
    internal_state = [energy, age]

    food = np.zeros(shape=(2*vision_range + 1, 2*vision_range + 1))
    creatures = np.ones(shape=(2*vision_range + 1, 2*vision_range + 1)) * 20

    food[vision_range][vision_range + 1] = 20
    creatures[vision_range][vision_range + 1] = 0

    return list(chain.from_iterable(creatures)) + list(chain.from_iterable(food)) + internal_state, Actions.RIGHT


def haven_left(vision_range):
    ''' Haven cell in current location.'''
    energy = 3
    age = 3
    internal_state = [energy, age]

    food = np.zeros(shape=(2*vision_range + 1, 2*vision_range + 1))
    creatures = np.ones(shape=(2*vision_range + 1, 2*vision_range + 1)) * 20

    food[vision_range][vision_range - 1] = 20
    creatures[vision_range][vision_range - 1] = 0

    return list(chain.from_iterable(creatures)) + list(chain.from_iterable(food)) + internal_state, Actions.LEFT


def haven_up(vision_range):
    ''' Haven cell up.'''
    energy = 3
    age = 3
    internal_state = [energy, age]

    food = np.zeros(shape=(2*vision_range + 1, 2*vision_range + 1))
    creatures = np.ones(shape=(2*vision_range + 1, 2*vision_range + 1)) * 20

    food[vision_range - 1][vision_range] = 20
    creatures[vision_range - 1][vision_range] = 0

    return list(chain.from_iterable(creatures)) + list(chain.from_iterable(food)) + internal_state, Actions.UP


def haven_down(vision_range):
    ''' Haven cell down.'''
    energy = 3
    age = 3
    internal_state = [energy, age]

    food = np.zeros(shape=(2*vision_range + 1, 2*vision_range + 1))
    creatures = np.ones(shape=(2*vision_range + 1, 2*vision_range + 1)) * 20

    food[vision_range + 1][vision_range] = 20
    creatures[vision_range + 1][vision_range] = 0

    return list(chain.from_iterable(creatures)) + list(chain.from_iterable(food)) + internal_state, Actions.DOWN