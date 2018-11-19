import numpy as np

__author__ = 'gkour'


def population_aiq_dist(creatures):
    repetitions = 18
    young = [test_aiq(creature, repetitions) for creature in creatures if creature.age() <= 10]
    adult = [test_aiq(creature, repetitions) for creature in creatures if 10 < creature.age() < 20]
    old = [test_aiq(creature, repetitions) for creature in creatures if 20 < creature.age()]

    return np.round([np.nanmean(young), np.nanmean(adult), np.nanmean(old)], 2)


def test_aiq(creature, test_size=3):
    score = 0
    scenarios = [food_left, food_right, food_inplace]
    for i in range(test_size):
        test_state, optimal_action = scenarios[i%3](creature.vision_range())
        decision = creature.brain().act(test_state)
        score += 1 if decision == optimal_action else 0
    return score / test_size


def food_left(vision_range):
    energy = 3
    age = 3
    internal_state = [energy, age]

    #       (f c) (f c) (f c)
    #       (5 0) (0 0) (0 5)
    left_state = [0] * (vision_range * 2)
    left_state[-2] = 5
    left_state[-1] = 0

    right_state = [0] * (vision_range * 2)
    right_state[0] = 0
    right_state[1] = 0

    current_cell = [0, 0]

    return left_state + current_cell + right_state + internal_state, 0


def food_right(vision_range):
    energy = 3
    age = 3
    internal_state = [energy, age]

    #       (f c) (f c) (f c)
    #       (0 5) (0 0) (5 0)
    left_state = [0] * (vision_range * 2)
    left_state[-2] = 0
    left_state[-1] = 0

    right_state = [0] * (vision_range * 2)
    right_state[0] = 5
    right_state[1] = 0

    current_cell = [0, 0]

    return left_state + current_cell + right_state + internal_state, 1


def food_inplace(vision_range):
    energy = 3
    age = 3
    internal_state = [energy, age]

    #       (f c) (f c) (f c)
    #       (0 0) (0 0) (0 0)
    left_state = [0] * (vision_range * 2)
    left_state[-2] = 0
    left_state[-1] = 5

    right_state = [0] * (vision_range * 2)
    right_state[0] = 0
    right_state[1] = 5

    current_cell = [10, 0]

    return left_state + current_cell + right_state + internal_state, 2
