import numpy as np


class QLearning:
    q_table: np.ndarray
    start_state: tuple

    def __init__(self, start_state: tuple = (3, 0)):
        self.q_table = np.ones((4, 12), dtype=int) * -1
        for i in range(1, 11):
            self.q_table[3, i] = -100
        self.start_state = start_state

    def print_q_table(self):
        print(self.q_table)
