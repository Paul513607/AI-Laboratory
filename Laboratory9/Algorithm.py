import numpy as np


class QLearning:
    reward_table: np.ndarray
    q_table: np.ndarray
    start_state: tuple

    def __init__(self, start_state: tuple = (3, 0)):
        self.reward_table = np.ones((4, 12), dtype=int) * -1
        for i in range(1, 11):
            self.reward_table[3, i] = -100
        self.start_state = start_state

    def print_reward_table(self):
        print(self.reward_table)
