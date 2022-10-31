import re

from player import Player
from game import Game

if __name__ == '__main__':
    with open("nash_game.txt", "r") as fd:
        line1 = fd.readline()
        line1 = re.sub(r"\s+", '-', line1.strip())
        arr1 = line1.split('-')
        player1 = Player(arr1[1:])

        line2 = fd.readline()
        line2 = re.sub(r"\s+", '-', line2.strip())
        arr2 = line2.split('-')
        player2 = Player(arr2[1:])

        size = len(arr1) - 1
        game = Game((size, size), player1, player2)
        for i in range(0, size):
            line = fd.readline()
            line = re.sub(r"\s+", '-', line.strip())
            line = line.split('-')
            for j in range(0, size):
                nums = line[j].split('/')
                game.game_states[i, j] = (int(nums[0]), int(nums[1]))
        print(player1.possible_moves)
        print(player2.possible_moves)
        print(game.game_states)

        # print(game.get_b_scores_for_a_move('Left'))
        # print(game.get_a_scores_for_a_move('Left'))
        # print(game.get_a_scores_for_b_move('Down'))
        # print(game.get_b_scores_for_b_move('Down'))
        # print(game.get_b_scores_for_a_move('A'))
        # print(game.get_a_scores_for_a_move('A'))
        # print(game.get_a_scores_for_b_move('V'))
        # print(game.get_b_scores_for_b_move('V'))
        # for idx, move in enumerate(game.player2.possible_moves):
        #     best_player_1_move = max(game.player1.possible_moves, key=lambda x: game.get_a_scores_for_a_move(x)[idx])
        #     best_moves_p1 = list(filter(
        #         lambda x: game.get_a_scores_for_a_move(x)[idx] == game.get_a_scores_for_a_move(best_player_1_move)[idx],
        #         game.player1.possible_moves))
        #     print('For players 2 move ', move, ' the best player1 moves are', best_moves_p1)
        #
        # for idx, move in enumerate(game.player1.possible_moves):
        #     best_player_2_move = max(game.player2.possible_moves, key=lambda x: game.get_b_scores_for_b_move(x)[idx])
        #     best_moves_p2 = list(filter(
        #         lambda x: game.get_b_scores_for_b_move(x)[idx] == game.get_b_scores_for_b_move(best_player_2_move)[idx],
        #         game.player2.possible_moves))
        #     print('For players 1 move ', move, ' the best player2 moves are', best_moves_p2)
        #
        print("Dominant strategies for Player 1: ", game.find_dominant_strats_for_a())
        print("Dominant strategies for Player 2: ", game.find_dominant_strats_for_b())
        print("Nash equilibrium moves: ", game.find_pure_nash_equilibrium())
