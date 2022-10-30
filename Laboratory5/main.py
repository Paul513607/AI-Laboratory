import re

from player import Player
from game import Game

if __name__ == '__main__':
    with open("game.txt", "r") as fd:
        line1 = fd.readline()
        line1 = re.sub(r"\s+", '-', line1.strip())
        arr1 = line1.split('-')
        player1 = Player(arr1[1:])

        line2 = fd.readline()
        line2 = re.sub(r"\s+", '-', line2.strip())
        arr2 = line2.split('-')
        player2 = Player(arr2[1:])

        size = len(arr1) - 1
        line = line2
        game = Game((size, size), player1, player2)
        for i in range(0, size):
            line = fd.readline()
            line = re.sub(r"\s+", '-', line.strip())
            line = line.split('-')
            for j in range(0, size):
                game.game_states[i, j] = (int(line[j][0]), int(line[j][2]))
        print(player1.possible_moves)
        print(player2.possible_moves)
        print(game.game_states)

        print(game.get_b_scores_for_a_move('Left'))
        print(game.get_a_scores_for_a_move('Left'))
        print(game.get_a_scores_for_b_move('Down'))
        print(game.get_b_scores_for_b_move('Down'))

