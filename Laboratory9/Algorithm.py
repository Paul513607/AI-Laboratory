import numpy
import numpy as np
import gymnasium as gym

env = gym.make('CliffWalking-v0', render_mode='human')


class QLearning:
    reward_table: np.ndarray
    q_table: dict
    start_state: tuple
    episode_ends: list
    episodes: int
    episodes_qtable: list
    epsilon: float
    alpha: float
    gamma: float
    actions: list

    danger_states = {}

    def __init__(self, start_state: tuple = (3, 0), episodes: int = 100,
                 epsilon: float = 0.9, alpha: float = 0.1, gamma: float = 0.9):
        self.reward_table = np.ones((4, 12), dtype=int) * -1
        for i in range(1, 11):
            self.reward_table[3, i] = -100
        self.reward_table[3, 11] = 0
        self.start_state = start_state
        self.episode_ends = [(3, 11)]
        self.episodes = episodes
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.episodes_qtable = []
        self.actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.q_table = {}
        for i in range(4):
            for j in range(12):
                self.q_table[i, j] = np.zeros(4)

        self.danger_states = {(3, j) for j in range(1, 11)}
        self.remove_unreachable_states()

    def print_reward_table(self):
        print(self.reward_table)

    def print_q_table(self):
        print(self.q_table)

    def is_action_valid(self, curr_state: tuple, action: tuple) -> bool:
        new_state = (curr_state[0] + action[0], curr_state[1] + action[1])
        return 0 <= new_state[0] < 4 and 0 <= new_state[1] < 12

    def get_valid_actions(self, curr_state: tuple) -> set:
        valid_actions = set()
        for action in self.actions:
            if self.is_action_valid(curr_state, action):
                valid_actions.add(action)
        return valid_actions

    # This function sets the q_value of unreachable states to -np.inf
    def remove_unreachable_states(self):
        for state in self.q_table.keys():
            valid_actions = self.get_valid_actions(state)
            action_indexes = [self.actions.index(action) for action in valid_actions]
            for i in range(4):
                if i not in action_indexes:
                    self.q_table[state][i] = -np.inf

    def get_next_state(self, curr_state: tuple, action: tuple) -> tuple:
        return curr_state[0] + action[0], curr_state[1] + action[1]

    def update_q_table(self, curr_state: tuple, action: tuple):
        action_index = self.actions.index(action)
        next_state = self.get_next_state(curr_state, action)
        # Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
        new_q_value = self.q_table[curr_state[0], curr_state[1]][action_index] + self.alpha * ( \
                    self.reward_table[next_state[0], next_state[1]] + self.gamma * max( \
                self.q_table[next_state[0], next_state[1]]) - self.q_table[curr_state[0], curr_state[1]][action_index])
        self.q_table[curr_state[0], curr_state[1]][action_index] = new_q_value

    def update_q_table_sarsa(self, curr_state: tuple, action: tuple, next_state: tuple, next_action: tuple):
        action_index = self.actions.index(action)
        next_action_index = self.actions.index(next_action)
        # Q(s, a) = Q(s, a) + alpha * (reward + gamma * Q(s', a') - Q(s, a))
        new_q_value = self.q_table[curr_state[0], curr_state[1]][action_index] + self.alpha * ( \
                    self.reward_table[next_state[0], next_state[1]] + self.gamma * self.q_table[next_state[0],
                    next_state[1]][next_action_index] - self.q_table[curr_state[0], curr_state[1]][action_index])
        self.q_table[curr_state[0], curr_state[1]][action_index] = new_q_value

    # epsilon-greedy choice
    def get_action(self, curr_state: tuple) -> tuple:
        if np.random.uniform() < self.epsilon:
            action_index = np.argmax(self.q_table[curr_state[0], curr_state[1]])
        else:
            action_index = np.random.randint(0, 4)
        return self.actions[action_index]

    def train(self):
        for episode in range(self.episodes):
            curr_state = self.start_state
            while curr_state not in self.episode_ends:
                action = self.get_action(curr_state)
                while action not in self.get_valid_actions(curr_state):
                    action = self.get_action(curr_state)
                self.update_q_table(curr_state, action)
                curr_state = self.get_next_state(curr_state, action)
                if curr_state in self.danger_states:
                    curr_state = self.start_state
            # epsilon decay
            self.epsilon *= 0.9
            print(f"Episode {episode + 1} finished")
            self.episodes_qtable += [self.q_table_to_states_values(self.q_table)]

    def train_sarsa(self):
        for episode in range(self.episodes):
            curr_state = self.start_state
            action = self.get_action(curr_state)
            while curr_state not in self.episode_ends:
                while action not in self.get_valid_actions(curr_state):
                    action = self.get_action(curr_state)
                next_state = self.get_next_state(curr_state, action)
                next_action = self.get_action(next_state)
                while next_action not in self.get_valid_actions(next_state):
                    next_action = self.get_action(next_state)
                self.update_q_table_sarsa(curr_state, action, next_state, next_action)
                curr_state = next_state
                action = next_action
                if curr_state in self.danger_states:
                    curr_state = self.start_state
            # epsilon decay
            self.epsilon *= 0.9
            print(f"Episode {episode + 1} finished")
            self.episodes_qtable += [self.q_table_to_states_values(self.q_table)]

    def get_path(self):
        curr_state = self.start_state
        path = [curr_state]
        while curr_state not in self.episode_ends:
            action = self.actions[np.argmax(self.q_table[curr_state[0], curr_state[1]])]
            curr_state = self.get_next_state(curr_state, action)
            path.append(curr_state)
        return path

    def get_mirrored_action(self, action: tuple) -> tuple:
        return -action[0], -action[1]

    def get_path_sarsa(self):
        curr_state = self.start_state
        path = [curr_state]
        q_table_copy = self.q_table.copy()
        while curr_state not in self.episode_ends:
            action_idx = np.argmax(q_table_copy[curr_state[0], curr_state[1]])
            action = self.actions[action_idx]
            curr_state = self.get_next_state(curr_state, action)
            mirrored_action_idx = self.actions.index(self.get_mirrored_action(action))
            q_table_copy[curr_state[0], curr_state[1]][mirrored_action_idx] = -np.inf
            path.append(curr_state)
        return path

    def render_politic(self):
        env.reset()
        env.render()
        curr_state = self.start_state
        while curr_state not in self.episode_ends:
            action = self.actions[np.argmax(self.q_table[curr_state[0], curr_state[1]])]
            env_action = map_action_to_number(action)
            curr_state = self.get_next_state(curr_state, action)
            env.step(env_action)

    def q_table_to_states_values(self, q_table):
        col_count, row_count = 12, 4
        states_values = [[0 for x in range(col_count)] for y in range(row_count)]
        # up = self.actions.index((-1, 0))
        # right = self.actions.index((0, 1))
        # down = self.actions.index((1, 0))
        # left = self.actions.index((0, -1))
        for i in range(row_count):
            for j in range(col_count):
                # vals = []
                # if i > 0:
                #     vals += [q_table[i - 1, j][down]]
                # if i < row_count - 2:
                #     vals += [q_table[i + 1, j][up]]
                # if j > 0:
                #     vals += [q_table[i, j - 1][right]]
                # if j < col_count - 2:
                #     vals += [q_table[i, j + 1][left]]
                # states_values[i][j] += sum([0 if val is numpy.NINF else val for val in vals])
                states_values[i][j] = np.ma.masked_invalid(q_table[i, j]).sum()
        return states_values


def map_action_to_number(action):
    # There are 4 discrete deterministic actions:
    # 0: move up
    # 1: move right
    # 2: move down
    # 3: move left
    if action == (-1, 0):
        return 0
    elif action == (0, 1):
        return 1
    elif action == (1, 0):
        return 2
    elif action == (0, -1):
        return 3
    else:
        raise Exception('Invalid action: ' + action)
