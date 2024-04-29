from .game import logic as logic
from .game import constants as c
from tkinter import Frame, Label, CENTER

class PY2048:
    def __init__(self):
        # Initialize board
        self.matrix = logic.new_game(c.GRID_LEN)

    def action(self, action):
        # take one of four moves based on q table
        match action:
            case "up":
                self.matrix, done = logic.up(self.matrix)
            case "down":
                self.matrix, done = logic.down(self.matrix)
            case "left":
                self.matrix, done = logic.left(self.matrix)
            case "right":
                self.matrix, done = logic.right(self.matrix)

    def evaluate(self):
        # calculate reward based on current state
        # 10 * highest block + sum of rest of blocks
        max_block = 0
        total_sum = 0
        for row in self.matrix:
            for cell in row:
                total_sum += cell
                if cell > max_block:
                    max_block = cell
        return 10 * max_block + total_sum

    def is_over(self):
        # board has no possible moves or reaches 2048
        return logic.game_state(self.matrix) != 'not over'

    def observe(self):
        # return current state of board
        return self.matrix

    def view(self):
        # render the board
        print(self.matrix)
