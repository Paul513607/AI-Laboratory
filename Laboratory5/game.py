import numpy as np


class Game:
    game_states = []

    def __init__(self, shape, player1, player2):
        self.game_states = np.zeros(shape, dtype=tuple)
        self.player1 = player1
        self.player2 = player2

    def get_b_scores_for_a_move(self, a_move):
        index = self.player1.possible_moves.index(a_move)
        return [tup[1] for tup in self.game_states[index]]

    def get_a_scores_for_b_move(self, b_move):
        index = self.player2.possible_moves.index(b_move)
        return [tup[0] for tup in self.game_states.T[index]]

    def get_a_scores_for_a_move(self, a_move):
        index = self.player1.possible_moves.index(a_move)
        return [tup[0] for tup in self.game_states[index]]

    def get_b_scores_for_b_move(self, b_move):
        index = self.player2.possible_moves.index(b_move)
        return [tup[1] for tup in self.game_states.T[index]]
