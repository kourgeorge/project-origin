__author__ = 'gkour'

import os

import numpy as np
import pfrl
import torch
import torch.nn as nn
import torch.nn.functional as F

import utils
from config import ConfigBiology, ConfigBrain
from creatures.human import Human
from evolution import DNA


class HumanPRLF(Human):
    Fitrah = [0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanPRLF, self).__init__(universe, id, dna, age, energy, parents)

    @staticmethod
    def get_race():
        return HumanPRLF

    @staticmethod
    def race_name():
        return 'HumanPRLF'

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_BRAIN_STRUCTURE_PARAM,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_REWARD_DISCOUNT,
                   HumanPRLF.race_fitrah())

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(HumanPRLF.Fitrah)

    # @staticmethod
    # def self_race_enemy():
    #     return True

    def initialize_brain(self):
        # self._brain = BrainPRLF(observation_shape=tuple(self.observation_shape()),
        #                        num_actions=self.num_actions(), reward_discount=self.reward_discount())
        self._brain = initialize_PRLF_agent(self.observation_shape(), self.num_actions())

    def decide(self, state):
        action = self._brain.act(state)
        return action

    def add_experience(self, experience):
        self._brain.observe(experience[3], experience[2], experience[4], -1)

    def smarten(self):
        pass


class HumanPRLFUnifiedBrain(HumanPRLF):
    _master_brain = None

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanPRLFUnifiedBrain, self).__init__(universe, id, dna, age, energy, parents)

    def initialize_brain(self):
        self._brain = self.get_master_brain()

    def get_master_brain(self):
        if HumanPRLFUnifiedBrain._master_brain is None:
            HumanPRLFUnifiedBrain._master_brain = initialize_PRLF_agent(self.observation_shape(), self.num_actions())
            if self.model_path() is not None and os.path.exists(self.model_path()):
                HumanPRLFUnifiedBrain._master_brain.load_model(self.model_path())
        return HumanPRLFUnifiedBrain._master_brain

    @staticmethod
    def get_race():
        return HumanPRLFUnifiedBrain

    @staticmethod
    def race_name():
        return 'HumanPRLFUnifiedBrain'

    def new_born(self):
        pass


def initialize_PRLF_agent(obs_size, n_actions):
    class DQN(nn.Module):
        def __init__(self, num_channels, num_actions):
            super(DQN, self).__init__()
            self.conv1 = nn.Conv2d(num_channels, 4, kernel_size=2)
            self.bn1 = nn.BatchNorm2d(4)
            self.conv2 = nn.Conv2d(4, 5, kernel_size=2)
            self.bn2 = nn.BatchNorm2d(5)
            self.head = nn.Linear(45, num_actions)

        def forward(self, x):
            x = self.bn1(F.relu(self.conv1(x)))
            x = self.bn2(F.relu(self.conv2(x)))
            return pfrl.action_value.DiscreteActionValue(self.head(x.view(x.size(0), -1)))

    # obs_size = env.observation_space.low.size
    # obs_size = self.observation_shape()
    # n_actions = self.num_actions()
    q_func = DQN(obs_size[0], n_actions)

    # Use Adam to optimize q_func. eps=1e-2 is for stability.
    optimizer = torch.optim.Adam(q_func.parameters(), eps=1e-2)

    # Set the discount factor that discounts future rewards.
    gamma = 0.99

    def random_action_func():
        return np.random.randint(0, n_actions)

    # Use epsilon-greedy for exploration
    explorer = pfrl.explorers.ConstantEpsilonGreedy(
        epsilon=0.3, random_action_func=random_action_func)

    # DQN uses Experience Replay.
    # Specify a replay buffer and its capacity.
    replay_buffer = pfrl.replay_buffers.ReplayBuffer(capacity=10 ** 6)

    # Since observations from CartPole-v0 is numpy.float64 while
    # As PyTorch only accepts numpy.float32 by default, specify
    # a converter as a feature extractor function phi.
    phi = lambda x: x.astype(np.float32, copy=False)

    # Set the device id to use GPU. To use CPU only, set it to -1.
    gpu = -1

    # Now create an agent that will interact with the environment.
    agent = pfrl.agents.DoubleDQN(
        q_func,
        optimizer,
        replay_buffer,
        gamma,
        explorer,
        replay_start_size=500,
        update_interval=1,
        target_update_interval=100,
        phi=phi,
        gpu=gpu,
    )

    return agent
