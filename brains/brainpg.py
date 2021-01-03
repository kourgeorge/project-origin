__author__ = 'gkour'

import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from brains.abstractbrain import AbstractBrain
import os.path
import math

#torch.manual_seed(0)

device = "cpu"


def has_err(x):
    return bool(((x != x) | (x == float("inf")) | (x == float("-inf"))).any().item())


class BrainPG(AbstractBrain):
    BATCH_SIZE = 20

    def __init__(self, observation_shape, num_actions, reward_discount, learning_rate=0.01):
        super(BrainPG, self).__init__(observation_shape[0], num_actions)
        self.policy = Policy(observation_shape[0], num_actions).to(device)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=learning_rate)
        self.reward_discount = reward_discount
        self.num_optimizations = 0
        print("Pytorch PG. Num parameters: " + str(self.num_trainable_parameters()))

    def think(self, obs):
        with torch.no_grad():
            action_probs = self.policy(torch.from_numpy(obs).float().unsqueeze_(0))
            if math.isnan(action_probs[0][0].item()):
                raise Exception('nan probability')
        return action_probs[0].tolist()

    def train(self, experience):
        minibatch_size = min(BrainPG.BATCH_SIZE, len(experience))
        if minibatch_size < BrainPG.BATCH_SIZE:
            return
        self.num_optimizations += 1

        minibatch = experience #list(experience)[-5:] # random.sample(experience, minibatch_size)
        state_batch = torch.from_numpy(np.stack([np.stack(data[0]) for data in minibatch])).float()
        action_batch = torch.FloatTensor([data[1] for data in minibatch])
        # removing the discounting from here.
        #reward_batch = torch.FloatTensor(utils.discount_rewards([data[2] for data in minibatch], self.reward_discount))
        reward_batch = torch.FloatTensor([data[2] for data in minibatch])
        nextstate_batch = torch.from_numpy(np.stack([data[3] for data in minibatch])).float()

        # Scale rewards
        #reward_std = 1 if torch.isnan(reward_batch.std()) else reward_batch.std()
        #rewards = (reward_batch - reward_batch.mean()) / (reward_std + np.finfo(np.float32).eps)

        prob_action_batch = self.policy(state_batch)
        prob_actions = torch.max(prob_action_batch.mul(action_batch), dim=1)[0]
        log_prob_actions = torch.log(prob_actions)

        # Calculate loss
        loss = (torch.mean(torch.mul(log_prob_actions, reward_batch).mul(-1), -1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()

        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), max_norm=1)
        # for param in self.policy_net.parameters():
        #     param.grad.data.clamp_(-1, 1)
        self.optimizer.step()
        #print(loss.item())
        if math.isinf(loss.item()):
            raise Exception('INF probability')
        return loss.item()

    def save_model(self, path):
        torch.save(self.policy.state_dict(), path)

    def load_model(self, path):
        if os.path.exists(path):
            self.policy.load_state_dict(torch.load(path))

    def num_trainable_parameters(self):
        return sum(p.numel() for p in self.policy.parameters())


class Policy(nn.Module):
    def __init__(self, num_channels, num_actions):
        super(Policy, self).__init__()
        self.conv1 = nn.Conv2d(num_channels, 4, kernel_size=2)
        self.bn1 = nn.BatchNorm2d(4)
        self.conv2 = nn.Conv2d(4, 5, kernel_size=2)
        self.bn2 = nn.BatchNorm2d(5)
        self.head = nn.Linear(45, num_actions)

        self.model = torch.nn.Sequential(
            self.conv1,
            #nn.ReLU,
            nn.BatchNorm2d(4),
            self.conv2,
            #nn.ReLU,
            nn.BatchNorm2d(5),
            #nn.Dropout(p=0.6),
            nn.Sigmoid(),
            nn.Flatten(),
            self.head,
            nn.Softmax(dim=-1)
        )

        # self.net = nn.Sequential(
        #     nn.Flatten(),
        #     nn.Linear(in_features=num_channels, out_features=8, bias=False),
        #     nn.PReLU(),
        #     nn.Linear(in_features=8, out_features=8, bias=False),
        #     nn.PReLU(),
        #     nn.Linear(in_features=8, out_features=num_actions, bias=False),
        #     nn.Softmax(dim=-1)
        # )

    def forward(self, x):
        return self.model(x)
