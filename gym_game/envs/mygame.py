from .game import puzzle as puzzle
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
                logic.up(self.matrix)
            case "down":
                logic.down(self.matrix)
            case "left":
                logic.left(self.matrix)
            case "right":
                logic.right(self.matrix)

    def evaluate(self):
        # calculate reward based on current state
        # 10 * highest block + sum of rest of blocks
        max_block = 0
        total_sum = 0
        for row in self.gameGrid.matrix:
            for cell in row:
                total_sum += cell
                if cell > max_block:
                    max_block = cell
        return 10 * max_block + total_sum

    def is_over(self):
        # board has no possible moves or reaches 2048
        return logic.game_state(self.gameGrid.matrix) != 'not over'

    def observe(self):
        # return current state of board
        return self.gameGrid.matrix

    def view(self):
        # render the board
        self.gameGrid.update_grid_cells()
