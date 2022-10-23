from board import PlayingBoard

has_solution = False


def is_solution(board):
    return len(board.solution) == board.size


def is_valid(queen_no, position, board):
    is_available_pos = position in board.variables[queen_no]

    if not is_available_pos:
        return False
    if queen_no + 1 == board.size:
        return is_available_pos

    next_variables_copy = board.variables[queen_no + 1].copy()
    for next_position in board.variables[queen_no + 1]:
        if position[0] == next_position[0]:
            next_variables_copy.remove(next_position)
        elif position[1] == next_position[1]:
            next_variables_copy.remove(next_position)
        elif abs(position[0] - next_position[0]) == abs(position[1] - next_position[1]):
            next_variables_copy.remove(next_position)

    return is_available_pos and len(next_variables_copy) > 0


def print_solution(board):
    print(board.solution)


def place_queen(queen_no, position, board):
    board.solution.append(position)
    board.board[position[0], position[1]] = 1

    for i in range(0, board.size):
        if i == position[0]:
            continue

        board.board[i, position[1]] -= 1
        if (i, position[1]) in board.variables[position[1]]:
            board.variables[position[1]].remove((i, position[1]))
    for j in range(position[1], board.size):
        if j == position[1]:
            continue

        board.board[position[0], j] -= 1
        if (position[0], j) in board.variables[j]:
            board.variables[j].remove((position[0], j))

    i, j = position
    while i >= 0 and j < board.size:
        if (i, j) != position:
            board.board[i, j] -= 1
            if (i, j) in board.variables[j]:
                board.variables[j].remove((i, j))
        i -= 1
        j += 1

    i, j = position
    while i < board.size and j < board.size:
        if (i, j) != position:
            board.board[i, j] -= 1
            if (i, j) in board.variables[j]:
                board.variables[j].remove((i, j))
        i += 1
        j += 1

    return board


def remove_queen(queen_no, position, board):
    board.board[position[0], position[1]] = 0
    board.solution.remove(position)

    for i in range(0, board.size):
        if i == position[0]:
            continue

        board.board[i, position[1]] += 1
        if (i, position[1]) not in board.variables[position[1]] and board.board[i, position[1]] == 0:
            board.variables[position[1]].append((i, position[1]))
    for j in range(position[1], board.size):
        if j == position[1]:
            continue

        board.board[position[0], j] += 1
        if (position[0], j) not in board.variables[j] and board.board[position[0], j] == 0:
            board.variables[j].append((position[0], j))

    i, j = position
    while i >= 0 and j < board.size:
        if (i, j) != position:
            board.board[i, j] += 1
            if (i, j) not in board.variables[j] and board.board[i, j] == 0:
                board.variables[j].append((i, j))
        i -= 1
        j += 1

    i, j = position
    while i < board.size and j < board.size:
        if (i, j) != position:
            board.board[i, j] += 1
            if (i, j) not in board.variables[j] and board.board[i, j] == 0:
                board.variables[j].append((i, j))
        i += 1
        j += 1

    return board


def forward_check(board, column):
    global has_solution

    for i in range(0, board.size):
        if has_solution:
            return

        if is_valid(column, (i, column), board):
            board = place_queen(column, (i, column), board)
            if is_solution(board):
                board.print_solution()
                has_solution = True
            else:
                forward_check(board, column + 1)
            board = remove_queen(column, (i, column), board)
