import game.puzzle as puzzle
import game.logic as logic

class PY2048:
    def __init__(self):
        # Initialize board
        self.gameGrid = puzzle.GameGrid()

    def action(self, action):
        # take one of four moves based on q table
        match action:
            case "up":
                logic.up
            case "down":
                logic.down
            case "left":
                logic.left
            case "right":
                logic.right
    
    def win(self):
        for row in self.gameGrid.matrix:
            for cell in row:
                if cell >= 2048:
                    return True
        return False


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

    def is_done(self):
        # board has no possible moves or reaches 2048
        return self.gameGrid.game_state(self.gameGrid.matrix) != 'not over'

    def observe(self):
        # return current state of board
        return self.gameGrid.matrix

    def view(self):
        # render the board
        self.gameGrid.update_grid_cells()
