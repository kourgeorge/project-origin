__author__ = 'gkour'
import numpy as np
import contextlib
import tensorflow as tf
from scipy.signal import lfilter
import csv
import os


def discount_rewards(r, gamma):
    discounted_r = np.zeros_like(r).astype(float)
    running_add = 0
    for t in reversed(range(0, len(r))):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


def extract_episode_history(ep_history):
    episode_states = [inter_data[0] for inter_data in ep_history]
    episode_actions = [inter_data[1] for inter_data in ep_history]
    episode_rewards = [inter_data[2] for inter_data in ep_history]
    episode_length = len(episode_rewards)

    return episode_states, episode_actions, episode_rewards, episode_length


def print_episode_dynamics(env, episode_actions, episode_rewards, episode_discounted_rewards, action_dist):
    with _printoptions(formatter={'float': '{: 0.3f}'.format}, precision=3, suppress=True, linewidth=300):
        print("-----------------------------------")
        print("images:\t", [str(item) for item in env._labels], '. answer: ', env._answer)
        print("actions:\t", [str(action) for action in episode_actions])
        print("rewards:\t", episode_rewards)
        print("discounted:\t", episode_discounted_rewards)
        print("Actions Dist:", action_dist)


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


# Values is an nparray of reals and relevant_values is an nparray of zeros and ones
def avg_null(all_values, relevant_values):
    if np.sum(relevant_values) == 0: return None
    sum = np.sum(all_values * relevant_values)
    return sum / np.sum(relevant_values)


# Pred is an nparray of predicted values (reals) and label is an nparray of true values
def precision_recall_f1(pred, label):
    if not isinstance(pred, np.ndarray):
        pred = [pred]
    if not isinstance(label, np.ndarray):
        label = [label]
    if len(pred) == 0 or len(label) == 0: return 0, 0, 0
    if np.array_equal(label, pred): return 1.0, 1.0, 1.0
    predset = set(pred)
    predset.intersection_update(set(label))
    right_pred = len(predset)
    precision = right_pred / len(pred)
    recall = right_pred / len(label)
    if (precision + recall) == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


@contextlib.contextmanager
def _printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    try:
        yield
    finally:
        np.set_printoptions(**original)


def moving_average(data, window_width):
    cumsum_vec = np.cumsum(np.insert(data, 0, 0))
    return (cumsum_vec[window_width:] - cumsum_vec[:-window_width]) / window_width


def print_accumulative_stats(episode, config, total_reward, successful, interaction_length, updates_counter, steps_accuracy):
    print("Episode: ", episode, " Mean reward: ", np.mean(total_reward[-config.num_episodes_stats:]),
          ". Success Rate",
          np.mean(successful[-config.num_episodes_stats:]), ". Mean interaction Length: ",
          np.mean(interaction_length[-config.num_episodes_stats:]), ". Updates count: ",
          np.sum(updates_counter[-config.num_episodes_stats:]),
          ". Mean accuracy", np.mean(steps_accuracy[-config.num_episodes_stats:]))

def update_target_graph(from_scope, to_scope):
    from_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, from_scope)
    to_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, to_scope)

    if len(from_vars)!=len(to_vars):
        print("unequal number of variables of source and target networks.")

    op_holder = []
    for from_var, to_var in zip(from_vars, to_vars):
        op_holder.append(to_var.assign(from_var))
    return op_holder


def discount(x, gamma):
    x = np.asarray(x, dtype=np.float32)
    return lfilter([1], [1, -gamma], x[::-1], axis=0)[::-1]


def log(logdir, episode, accuracy, training_reward, episode_length, update_frequency, time):
    file_path = os.path.join(logdir, 'log4_EL{}_UF{}_DT{}.csv'.format(episode_length, update_frequency, time))
    with open(file_path, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([episode, accuracy, training_reward])
        myfile.close()