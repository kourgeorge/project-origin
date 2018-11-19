import numpy as np

__author__ = 'gkour'


def test_iq(creature, test_size=3):
    score = 0
    scenarios = [scenario1, scenario2, scenario3]
    for i in range(test_size):
        test_state, optimal_action = scenarios[i](creature.vision_range())
        decision = creature.brain().act(test_state)
        score += 1 if decision == optimal_action else 0
    return score / test_size


def scenario1(vision_range):
    #food on left creature on right
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
    right_state[1] = 5

    current_cell = [0, 0]

    return left_state + current_cell + right_state + internal_state, 0


def scenario2(vision_range):
    ### food on right, creature on left
    energy = 3
    age = 3
    internal_state = [energy, age]

    #       (f c) (f c) (f c)
    #       (0 5) (0 0) (5 0)
    left_state = [0] * (vision_range * 2)
    left_state[-2] = 0
    left_state[-1] = 5

    right_state = [0] * (vision_range * 2)
    right_state[0] = 5
    right_state[1] = 0

    current_cell = [0, 0]

    return left_state + current_cell + right_state + internal_state, 1


def scenario3(vision_range):
    ### creatures around and food in place.
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
