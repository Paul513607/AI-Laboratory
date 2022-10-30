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

    def find_pure_nash_equilibrium(self):
        best_moves_p1 = {}
        best_moves_p2 = {}
        for idx, move in enumerate(self.player2.possible_moves):
            best_player_1_move = max(self.player1.possible_moves, key=lambda x: self.get_a_scores_for_a_move(x)[idx])
            best_moves_p1[move] = list(filter(
                lambda x: self.get_a_scores_for_a_move(x)[idx] == self.get_a_scores_for_a_move(best_player_1_move)[idx],
                self.player1.possible_moves))

        for idx, move in enumerate(self.player1.possible_moves):
            best_player_2_move = max(self.player2.possible_moves, key=lambda x: self.get_b_scores_for_b_move(x)[idx])
            best_moves_p2[move] = list(filter(
                lambda x: self.get_b_scores_for_b_move(x)[idx] == self.get_b_scores_for_b_move(best_player_2_move)[idx],
                self.player2.possible_moves))

        equilibrium_states = []

        for p2_move, p1_best_moves in best_moves_p1.items():
            p2_move_index = self.player2.possible_moves.index(p2_move)
            for p1_move in p1_best_moves:
                if p2_move in best_moves_p2[p1_move]:
                    p1_move_index = self.player1.possible_moves.index(p1_move)
                    strat_score = self.game_states[p1_move_index][p2_move_index]
                    equilibrium_states += [(p1_move, p2_move, strat_score)]

        return equilibrium_states

