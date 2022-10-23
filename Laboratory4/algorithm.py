from board import PlayingBoard

has_solution = False


def is_solution(board):
    return len(board.solution) == board.size


# Verificam daca urmatoarea mutare este valida, adica daca putem plasa o piesa la pozitia curenta si daca este o
# mutare posibila pentru urmatoarea regina dupa plasarea la pozitia curenta
def is_valid(queen_no, position, board):
    is_available_pos = position in board.variables[queen_no]

    if not is_available_pos:
        return False
    # in last row
    if queen_no + 1 == board.size:
        return is_available_pos
    # check that there are available positions on the next row
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


# Plasam regina la tuple-ul position pe board
def place_queen(position, board):
    # Plasarea reginei
    board.solution.append(position)
    board.board[position[0], position[1]] = 1
    board.variables[position[1]].remove(position)

    # Invalidam celelalte pozitii de pe coloana pe care am plasat regina
    for i in range(0, board.size):
        if i == position[0]:
            continue

        board.board[i, position[1]] -= 1
        # Stergem pozitia din lista variables
        if (i, position[1]) in board.variables[position[1]]:
            board.variables[position[1]].remove((i, position[1]))

    # Invalidam celelalte pozitii de pe rindul pe care am plasat regina
    for j in range(position[1], board.size):
        if j == position[1]:
            continue

        board.board[position[0], j] -= 1
        # Stergem pozitia din lista variables
        if (position[0], j) in board.variables[j]:
            board.variables[j].remove((position[0], j))

    # Invalidam pozitiile de pe diagonalele de deasupra pozitiei reginei
    i, j = position
    while i >= 0 and j < board.size:
        if (i, j) != position:
            board.board[i, j] -= 1
            if (i, j) in board.variables[j]:
                board.variables[j].remove((i, j))
        i -= 1
        j += 1

    # Invalidam pozitiile de pe diagonalele de desupt pozitia reginei
    i, j = position
    while i < board.size and j < board.size:
        if (i, j) != position:
            board.board[i, j] -= 1
            if (i, j) in board.variables[j]:
                board.variables[j].remove((i, j))
        i += 1
        j += 1

    return board


# Stergem regina de la tuple-ul position pe board
def remove_queen(position, board):
    board.board[position[0], position[1]] = 0
    board.solution.remove(position)
    board.variables[position[1]] += [position]

    # Eliberam pozitiile de pe coloana pe care am plasat regina
    for i in range(0, board.size):
        if i == position[0]:
            continue

        board.board[i, position[1]] += 1
        if (i, position[1]) not in board.variables[position[1]] and board.board[i, position[1]] == 0:
            board.variables[position[1]].append((i, position[1]))

    # Eliberam pozitiile de pe rindul pe care am plasat regina
    for j in range(position[1], board.size):
        if j == position[1]:
            continue

        board.board[position[0], j] += 1
        if (position[0], j) not in board.variables[j] and board.board[position[0], j] == 0:
            board.variables[j].append((position[0], j))

    # Eliberam pozitiile de pe diagonala deasupra reginei
    i, j = position
    while i >= 0 and j < board.size:
        if (i, j) != position:
            board.board[i, j] += 1
            if (i, j) not in board.variables[j] and board.board[i, j] == 0:
                board.variables[j].append((i, j))
        i -= 1
        j += 1

    # Eliberam pozitiile de pe diagonala de desupt regina
    i, j = position
    while i < board.size and j < board.size:
        if (i, j) != position:
            board.board[i, j] += 1
            if (i, j) not in board.variables[j] and board.board[i, j] == 0:
                board.variables[j].append((i, j))
        i += 1
        j += 1

    return board


# Find the column with the least amount of free spaces
def minimum_remaining_values_variable(board):
    free_columns = [i for i in range(0, board.size) if len(board.variables[i]) > 0]
    min_column = min(free_columns, key=lambda col: len(board.variables[col]))
    return min_column


def forward_check(board, column):
    global has_solution
    for i in range(0, board.size):
        if has_solution:
            return

        if is_valid(column, (i, column), board):
            board = place_queen((i, column), board)
            if is_solution(board):
                board.print_solution()
                has_solution = True
            else:
                next_column = minimum_remaining_values_variable(board)
                forward_check(board, next_column)
            board = remove_queen((i, column), board)
