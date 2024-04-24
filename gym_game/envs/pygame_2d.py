import pygame
import math

screen_width = 1500
screen_height = 800
check_point = ((1200, 660), (1250, 120), (190, 200), (1030, 270), (250, 475), (650, 690))

class PyGame2D:
    def __init__(self):
        # Initialize board

    def action(self, action):
        # take one of four moves based on q table

    def evaluate(self):
        # calculate reward based on current state
        # 10 * highest block + sum of rest of blocks
       
    def is_done(self):
        #board has no possible moves or reaches 2048

    def observe(self):
        # return current state of board
        
    def view(self):
        # render the board
