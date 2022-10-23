import numpy as np


class PlayingBoard:
    size = 0
    blocked_positions = []
    board = np.zeros((size, size), dtype=int)
    variables = {}
    solution = []

    def __init__(self, size, blocked_positions):
        self.size = size
        self.blocked_positions = blocked_positions
        self.board = np.zeros((size, size), dtype=int)
        for position in blocked_positions:
            self.board[position[0], position[1]] = -1
        for j in range(0, size):
            self.variables[j] = [(i, j) for i in range(0, size) if self.board[i, j] != -1]

    def print_solution(self):
        for position in sorted(self.solution, key=lambda pos: pos[1]):
            print(f"Q{position[1]}", position, " ")
