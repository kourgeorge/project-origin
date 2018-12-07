__author__ = 'gkour'


class AbstractBrain:

    def __init__(self, observation_shape, num_actions):
        self._observation_shape = observation_shape
        self._num_actions = num_actions

    def think(self, obs):
        '''Given an observation should return a distribution over the action set'''
        raise NotImplementedError()

    def train(self, experience):
        raise NotImplementedError()

    def observation_shape(self):
        return self._observation_shape

    def num_actions(self):
        return self._num_actions

    def save_model(self, path):
        raise NotImplementedError()

    def load_model(self, path):
        raise NotImplementedError()
