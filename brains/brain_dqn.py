__author__ = 'gkour'

import tensorflow as tf
import utils as utils
import numpy as np
import tensorflow.contrib.slim as slim
import random
from brains.abstractbrain import AbstractBrain


class BrainDQN(AbstractBrain):
    BATCH_SIZE = 20
    sess = None
    EPSILON = 0.1

    @staticmethod
    def init_session():
        if BrainDQN.sess is None:
            tf.reset_default_graph()
            BrainDQN.sess = tf.Session()

    def __init__(self, lr, observation_shape, num_actions, h_size, scope, gamma, copy_from_scope=None):
        super(BrainDQN, self).__init__(observation_shape, num_actions)
        self._h_size = h_size
        self._regularization_param = 0.001
        self.lr = lr
        self._gamma = gamma

        BrainDQN.init_session()

        # Implementing F(state)=action
        self.state_in = tf.placeholder(shape=[None]+self.observation_shape(), dtype=tf.float32)
        self.reward_holder = tf.placeholder(shape=[None], dtype=tf.float32)
        self.action_holder = tf.placeholder(shape=[None], dtype=tf.int32)

        # init Q network
        self.QValue = self._create_qnetwork(scope, self.state_in)

        # init Target Q Network
        self.state_inT = tf.placeholder(shape=[None]+self.observation_shape(), dtype=tf.float32)
        self.QValueT = self._create_qnetwork('T' + scope, self.state_inT)

        self.copyTargetQNetworkOperation = utils.update_target_graph(scope, 'T' + scope)

        # Initialize Variables
        self._create_training_method()
        BrainDQN.sess.run(tf.variables_initializer(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'T' + scope)))
        BrainDQN.sess.run(tf.variables_initializer(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope)))

        self.saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope))

    def think(self, obs):
        q_value = BrainDQN.sess.run(self.QValue, feed_dict={self.state_in: [obs]})[0]
        return q_value

    def train(self, memory):
        minibatch_size = min(BrainDQN.BATCH_SIZE, len(memory))
        if minibatch_size == 0:
            return

        minibatch = random.sample(memory, minibatch_size)
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        nextstate_batch = [data[3] for data in minibatch]

        y_batch = []
        qvalue_batch = BrainDQN.sess.run(self.QValueT, feed_dict={self.state_inT: np.stack(nextstate_batch)})

        for i in range(0, minibatch_size):
            terminal = minibatch[i][4]
            if terminal:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + self._gamma * np.max(qvalue_batch[i]))

        BrainDQN.sess.run(self.trainStep, feed_dict={
            self.y_input: y_batch,
            self.action_in: action_batch,
            self.state_in: state_batch
        })

        self._copy_target_qnetwork()

    def save_model(self, path):
        self.saver.save(BrainDQN.sess, path)

    def load_model(self, path):
        self.saver.restore(BrainDQN.sess, path)

    def _create_qnetwork(self, scope, input_ph):
        with tf.variable_scope(scope):
            state = slim.convolution2d(input_ph, 10, [2, 2], scope='conv2_1', padding='VALID')
            state = slim.max_pool2d(state, [2, 2])
            state = slim.flatten(state)
            state = slim.stack(state, slim.fully_connected, [self._h_size], activation_fn=tf.nn.relu)
            action_output = slim.fully_connected(state, self.num_actions(), activation_fn=tf.nn.softmax,
                                                 weights_regularizer=slim.l2_regularizer(
                                                     self._regularization_param))

        return action_output

    def _create_training_method(self):
        self.action_in = tf.placeholder(tf.float32, [None, self.num_actions()])
        self.y_input = tf.placeholder(tf.float32, [None])
        q_action = tf.reduce_sum(tf.multiply(self.QValue, self.action_in), reduction_indices=1)
        cost = tf.reduce_mean(tf.square(self.y_input - q_action))
        self.trainStep = tf.train.RMSPropOptimizer(self.lr, 0.99, 0.0, 1e-6).minimize(cost)

    def _copy_target_qnetwork(self):
        BrainDQN.sess.run(self.copyTargetQNetworkOperation)
