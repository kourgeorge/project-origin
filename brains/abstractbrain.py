__author__ = 'gkour'


class AbstractBrain:

    def __init__(self, state_dims, action_size):
        self._state_dims = state_dims
        self._action_size = action_size

    def think(self, obs, eps):
        raise NotImplementedError()

    def train(self, experience):
        raise NotImplementedError()

    def state_dims(self):
        return self._state_dims

    def action_size(self):
        return self._action_size

    def save_model(self, path):
        raise NotImplementedError()

    def load_model(self, path):
        raise NotImplementedError()
