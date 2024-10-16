import numpy as np
import random

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.grid[i, j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i, j] = 2 if random.random() < 0.9 else 4

    def slide_left(self):
        moved, merged = False, False
        for row in range(4):
            tiles = self.grid[row][self.grid[row] != 0]  # Remove zeros
            merged_row = self.merge(tiles)
            if not np.array_equal(self.grid[row], merged_row):
                self.grid[row] = merged_row
                moved = True
        if moved:
            self.add_random_tile()
        return moved

    def slide_right(self):
        self.grid = np.fliplr(self.grid)
        moved = self.slide_left()
        self.grid = np.fliplr(self.grid)
        return moved

    def slide_up(self):
        self.grid = np.rot90(self.grid, 1)
        moved = self.slide_left()
        self.grid = np.rot90(self.grid, -1)
        return moved

    def slide_down(self):
        self.grid = np.rot90(self.grid, -1)
        moved = self.slide_left()
        self.grid = np.rot90(self.grid, 1)
        return moved

    def merge(self, row):
        merged = []
        skip = False
        for i in range(len(row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(row) and row[i] == row[i + 1]:
                merged.append(2 * row[i])
                self.score += 2 * row[i]
                skip = True
            else:
                merged.append(row[i])
        return np.array(merged + [0] * (4 - len(merged)))

    def is_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for row in self.grid:
            if any(row[i] == row[i + 1] for i in range(3)):
                return False
        for col in self.grid.T:
            if any(col[i] == col[i + 1] for i in range(3)):
                return False
        return True

    def has_won(self):
        return 2048 in self.grid
