import gym
from gym import spaces
import numpy as np
from gym_game.envs.pygame_2d import PyGame2D

class CustomEnv(gym.Env):
    # metadata = {'render.modes' : ['human']}
    # How do we set up environment here?
    def __init__(self):
        # The game seems correct..?
        self.pygame = PyGame2D()
        # It should be 4 because there are four actions that can be performed
        # self.action_space = spaces.Discrete(3)
        self.action_space = spaces.Discrete(4)

        ### Observation space is a 4x4 board

        # self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([10, 10, 10, 10, 10]), dtype=np.int)
        # self.observation_space = spaces.Box(np.array([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]), dtype=np.int)
        self.observation_space = spaces.Box(low=0, high=255, shape=(4, 4), dtype=np.int)


    def reset(self):
        del self.pygame
        self.pygame = PyGame2D()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()
