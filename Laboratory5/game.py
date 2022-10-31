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

    def find_dominant_strats_for_a(self):
        scores = {}
        for idx, move in enumerate(self.player1.possible_moves):
            curr_move_values = list(map(lambda tup: tup[0], self.game_states[idx]))
            scores[move] = sum(curr_move_values)
        max_key = max(scores, key=scores.get)
        return [(x, y) for x, y in scores.items() if y == scores.get(max_key)]

    def find_dominant_strats_for_b(self):
        scores = {}
        game_states_transpose = self.game_states.T
        for idx, move in enumerate(self.player1.possible_moves):
            curr_move_values = list(map(lambda tup: tup[1], game_states_transpose[idx]))
            scores[move] = sum(curr_move_values)
        max_key = max(scores, key=scores.get)
        return [(x, y) for x, y in scores.items() if y == scores.get(max_key)]

    def find_pure_nash_equilibrium(self):
        best_moves_p1 = {}
        best_moves_p2 = {}
        for idx, move in enumerate(self.player2.possible_moves):
            # find the best move for Player 1 based on Player 2's move
            best_player_1_move = max(self.player1.possible_moves, key=lambda x: self.get_a_scores_for_a_move(x)[idx])
            # add the best moves for Player 1 to the current of Player 2's key
            best_moves_p1[move] = list(filter(
                lambda x: self.get_a_scores_for_a_move(x)[idx] == self.get_a_scores_for_a_move(best_player_1_move)[idx],
                self.player1.possible_moves))

        for idx, move in enumerate(self.player1.possible_moves):
            # find the best move for Player 2 based on Player 1's move
            best_player_2_move = max(self.player2.possible_moves, key=lambda x: self.get_b_scores_for_b_move(x)[idx])
            # add the best moves for Player 1 to the current of Player 2's key
            best_moves_p2[move] = list(filter(
                lambda x: self.get_b_scores_for_b_move(x)[idx] == self.get_b_scores_for_b_move(best_player_2_move)[idx],
                self.player2.possible_moves))

        equilibrium_states = []

        # iterate through the best_moves for Player 1 (based on Player 2's move)
        for p2_move, p1_best_moves in best_moves_p1.items():
            p2_move_index = self.player2.possible_moves.index(p2_move)
            # iterate through the best moves for Player 1 and check if Player 2's move is the best move for him
            for p1_move in p1_best_moves:
                if p2_move in best_moves_p2[p1_move]:
                    p1_move_index = self.player1.possible_moves.index(p1_move)
                    strat_score = self.game_states[p1_move_index, p2_move_index]
                    equilibrium_states += [(p1_move, p2_move, strat_score)]

        return equilibrium_states

