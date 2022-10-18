import numpy as np


class PlayingBoard:
    size = 0
    blocked_positions = []
    board = np.zeros((size, size), dtype=int)
    variables = {}

    def __init__(self, size, blocked_positions):
        self.size = size
        self.blocked_positions = blocked_positions
        self.board = np.zeros((size, size), dtype=int)
        for position in blocked_positions:
            self.board[position[0], position[1]] = -1
        for i in range(0, size):
            self.variables[i] = [(i, j) for j in range(size) if self.board[j, i] != -1]
