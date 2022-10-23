import algorithm
import board
import parser


if __name__ == '__main__':
    size, blocked_positions = 0, []

    option = int(input("Enter the number of the option you want to run (0 - read from console / 1 - read from file): "))
    if option == 0:
        size = int(input("Enter the size of the board: "))
        blocked_positions = []
        print("Enter the blocked positions: (-1, -1) to stop.")
        while True:
            i, j = int(input("Enter the i coordinate: ")), int(input("Enter the j coordinate: "))
            if i == -1 and j == -1:
                break
            if 0 <= i < size and 0 <= j < size:
                blocked_positions.append((i, j))
    elif option == 1:
        filename = input("Enter the path of the file: ")
        size, blocked_positions = parser.parse(filename)

    my_board = board.PlayingBoard(size, blocked_positions)
    # print(my_board.board)
    # for key, value in my_board.variables.items():
    #     print(f"{key}: ", value)

    algorithm.forward_check(my_board, 0)
