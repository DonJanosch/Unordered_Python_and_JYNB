import numpy as np

import gym
from gym import wrappers

env_name = 'MountainCar-v0'
env = gym.make(env_name)
env.seed(30)
np.random.seed(0)
env.render()
