has_solution = False

def is_solution(board, column):
    return column == board.size


def is_valid(queen_no, position, board):
    if board.board[position[0], position[1]] == -1:
        return False

    for i in range(position[1]):
        if board.board[position[0], i] == 1:
            return False

        # Check upper diagonal on left side
    for i, j in zip(range(position[0], -1, -1),
                    range(position[1], -1, -1)):
        if board.board[i, j] == 1:
            return False

        # Check lower diagonal on left side
    for i, j in zip(range(position[0], board.size, 1),
                    range(position[1], -1, -1)):
        if board.board[i, j] == 1:
            return False

    return True


def solveNQUtil(board, col):
    global has_solution
    if col >= board.size:
        has_solution = True

    for i in range(board.size):
        if has_solution:
            return

        if is_valid(col, (i, col), board):
            board.board[i, col] = 1
            if solveNQUtil(board, col + 1):
                print(board.board)
                has_solution = True
            board.board[i, col] = 0
