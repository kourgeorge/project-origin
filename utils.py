__author__ = 'gkour'

import numpy as np
from scipy.signal import lfilter


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


def softmax(x, temprature=1):
    """
    Compute softmax values for each sets of scores in x.

    Rows are scores for each class.
    Columns are predictions (samples).
    """
    # x = normalize(np.reshape(x, (1, -1)), norm='l2')[0]
    ex_x = np.exp(temprature * np.subtract(x, max(x)))
    if np.isinf(np.sum(ex_x)):
        raise Exception('Inf in softmax')
    return ex_x / ex_x.sum(0)


def roll_fight(energy1, energy2):
    dist = normalize_dist([energy1, energy2])
    return np.random.choice(a=[-1, 1], p=dist)


def emptynanmean(array):
    if array is not None and len(array) > 0:
        return np.nanmean(array)
    return 0


def safe_log2(number):
    if number <= np.e:
        return 0
    return int(number/10)


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def normalize_dist(p):
    return softmax(p)


def linear_dist_normalization(p):
    p = np.asarray(p)
    p += abs(min(p))
    norm = sum(p)
    if norm == 0:
        norm = 1e-16
    res = p / norm
    return res
