__author__ = 'gkour'

import numpy as np
import tensorflow as tf
from scipy.signal import lfilter
import csv
import os
import stats


def discount_rewards(r, gamma):
    discounted_r = np.zeros_like(r).astype(float)
    running_add = 0
    for t in reversed(range(0, len(r))):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


def discount(x, gamma):
    x = np.asarray(x, dtype=np.float32)
    return lfilter([1], [1, -gamma], x[::-1], axis=0)[::-1]


def epsilon_greedy(eps, dist):
    p = np.random.rand()
    if p < eps:
        selection = np.random.randint(low=0, high=len(dist))
    else:
        selection = np.argmax(dist)

    return selection


def dist_selection(dist):
    select_prob = np.random.choice(dist, p=dist)
    selection = np.argmax(dist == select_prob)

    return selection


# Arg is an int and size is the len of the returning vector
def one_hot(arg, size):
    result = np.zeros(size)
    if 0 <= arg < size:
        result[arg] = 1
        return result
    else:
        return None


def moving_average(data, window_width):
    cumsum_vec = np.cumsum(np.insert(data, 0, 0))
    return (cumsum_vec[window_width:] - cumsum_vec[:-window_width]) / window_width


def update_target_graph(from_scope, to_scope):
    from_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, from_scope)
    to_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, to_scope)

    if len(from_vars) != len(to_vars):
        print("unequal number of variables of source and target networks.")

    op_holder = []
    for from_var, to_var in zip(from_vars, to_vars):
        op_holder.append(to_var.assign(from_var))
    return op_holder


def softmax(x):
    """
    Compute softmax values for each sets of scores in x.

    Rows are scores for each class.
    Columns are predictions (samples).
    """
    # x = normalize(np.reshape(x, (1, -1)), norm='l2')[0]
    scoreMatExp = np.exp(np.subtract(x, max(x)))
    if np.isinf(np.sum(scoreMatExp)):
        print('Inf in softmax')
    return scoreMatExp / scoreMatExp.sum(0)


def roll_fight(energy1, energy2):
    dist = softmax([energy1, energy2])
    return np.random.choice(a=[-1, 1], p=dist)


def print_step_stats(step_stats):
    for (key, value) in step_stats.items():
        print('{}: {}'.format(key, value), end=' | ')
    print()


def log_step_stats(file_path, step_stats):
    exists = os.path.isfile(file_path)
    if not exists:
        with open(file_path, 'a', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(list(step_stats.keys()))
            myfile.close()

    with open(file_path, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(step_stats.values())
        myfile.close()


def print_epoch_stats(universe):
    # print(universe.space(), end='\t')
    print('Death Cause [Fa Fi E]: ' + str(stats.death_cause))
    stats.death_cause = np.zeros_like(stats.death_cause)

    print('Food Supply: ' + str(universe.get_food_distribution()))
    print('Creatures: ' + str(universe.get_creatures_distribution()))
    print('Action Dist [LREMF]: ' + str(np.round(np.array(stats.action_log) / sum(stats.action_log), 2)))
    # energy = [creature.energy() for creature in universe.get_all_creatures()]
    # print(np.histogram(energy))
