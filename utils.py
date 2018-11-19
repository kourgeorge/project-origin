__author__ = 'gkour'

import numpy as np
import tensorflow as tf
from scipy.signal import lfilter
from random import randint
import csv
import os
from config import Config


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


def log(logdir, episode, accuracy, training_reward, episode_length, update_frequency, time):
    file_path = os.path.join(logdir, 'log4_EL{}_UF{}_DT{}.csv'.format(episode_length, update_frequency, time))
    with open(file_path, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([episode, accuracy, training_reward])
        myfile.close()


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
