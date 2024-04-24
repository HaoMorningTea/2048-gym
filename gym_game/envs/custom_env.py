import gym
from gym import spaces
import numpy as np
from gym_game.envs.mygame import PY2048

max_tile_value, board_size = 2048, 4

class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = PY2048()
        self.action_space = spaces.Discrete(4)
        self.action_mapping = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
        self.observation_space = spaces.Box(low=0, high=max_tile_value, shape=(board_size, board_size), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = PY2048()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self):
        self.pygame.view()
