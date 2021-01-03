# I need to build a basic environment that will help me sanity check the brains.
# Make sure there are no serious and dump bugs in the models implementation using gym.


from collections import deque

import gym
import numpy as np
import torch
from torch.distributions import Categorical

import utils
from brains.brainpg import BrainPG

# Building the environment
env = gym.make("FrozenLake-v0")
state_size = env.observation_space.n

def rollout(env, brain):
    episode = []
    observation = env.reset()
    done = False
    while not done:
        # env.render()
        # action = env.action_space.sample()  # your agent here (this takes random actions)
        obs_1hot = np.zeros(state_size)
        obs_1hot[observation] = 1
        brain_actions_prob = brain.think(obs=obs_1hot)
        action = Categorical(probs=torch.tensor(brain_actions_prob)).sample().item()
        new_observation, reward, done, info = env.step(action)

        dec_1hot = np.zeros(env.action_space.n)
        dec_1hot[action] = 1

        newobs_1hot = np.zeros(state_size)
        newobs_1hot[new_observation] = 1

        experience = [obs_1hot, dec_1hot, reward, newobs_1hot, done]
        episode.append(experience)
        observation = new_observation

    return episode



# building the agent
memory = deque(maxlen=1000)
brain = BrainPG(observation_shape=tuple([state_size]), num_actions=env.action_space.n, reward_discount=0.99, learning_rate=0.001)
success = []
for i in range(1, 100000):
    episode = rollout(env, brain)
    discounted_rewards = utils.discount_rewards([data[2] for data in episode], gamma=0.99)
    for step in range(len(episode)):
        episode[step][2] = discounted_rewards[step]
    memory.extend(episode)
    success += [episode[-1][2]]
    if i % 1000 == 0:
        print(np.mean(success[-1000:]))

    loss = brain.train(memory)
    # print(loss)

env.close()
