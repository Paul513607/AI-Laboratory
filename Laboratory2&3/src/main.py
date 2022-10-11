import math
from collections import deque

n, m, k = 0, 0, 0
old_states = []
applied_operations = []
initial_state = (0, 0)
transition_choices = ['emptyA', 'emptyB', 'fillA', 'fillB', 'transferAB', 'transferBA']
found_solution = False


# Initialization function
def init():
    global n, m, k, initial_state
    n = int(input("Enter first bowl size: "))
    m = int(input("Enter second bowl size: "))
    k = int(input("Enter target size: "))
    initial_state = (0, 0)
    old_states.append(initial_state)


# Check if a state is final state
def is_final_state(state):
    if state[0] == k or state[1] == k:
        return True
    return False


# Transitions
def empty(state, vase):
    if vase == 0:
        return 0, state[1]
    if vase == 1:
        return state[0], 0


def fill(state, vase):
    if vase == 0:
        return n, state[1]
    if vase == 1:
        return state[0], m


def transfer(state, vase):
    if vase == 0:
        diff = min(n - state[0], state[1])
        return state[0] + diff, state[1] - diff
    if vase == 1:
        diff = min(m - state[1], state[0])
        return state[0] - diff, state[1] + diff


def transition(state, choice):
    if choice == 'fillA':
        return fill(state, 0)
    if choice == 'fillB':
        return fill(state, 1)
    if choice == 'emptyA':
        return empty(state, 0)
    if choice == 'emptyB':
        return empty(state, 1)
    if choice == 'transferBA':
        return transfer(state, 0)
    if choice == 'transferAB':
        return transfer(state, 1)
    raise Exception('Invalid transfer choice!')


# Check if a state is valid
def is_valid(state):
    return 0 <= state[0] <= n and 0 <= state[1] <= m


def print_solution(path):
    print("Transitions:")
    for i in range(0, len(path) - 1):
        print(path[i], " ", applied_operations[i], " ", path[i + 1])
    print("Final state: ", path[len(path) - 1])


def bkt(curr_state):
    global found_solution, count
    for choice in transition_choices:
        if not found_solution:
            new_state = transition(curr_state, choice)
            if is_valid(new_state):
                if new_state not in old_states:
                    old_states.append(new_state)
                    applied_operations.append(choice)
                    if is_final_state(new_state):
                        found_solution = True
                        print_solution(old_states)
                    bkt(new_state)
                    old_states.remove(new_state)
                    applied_operations.remove(choice)


def print_solution_bfs(path):
    global applied_operations
    new_path = []
    new_ops = []
    curr_index = len(path) - 1
    curr_state = path[curr_index]
    prev_state = None

    while curr_state != (0, 0):
        if prev_state is not None:
            curr_state = prev_state
        op = applied_operations[curr_index - 1]
        new_path.append(curr_state)
        new_ops.append(op)
        if op == 'emptyA':
            op = 'fillA'
        elif op == 'emptyB':
            op = 'fillB'
        elif op == 'fillA':
            op = 'emptyA'
        elif op == 'fillB':
            op = 'emptyB'
        elif op == 'transferAB':
            op = 'transferBA'
        elif op == 'transferBA':
            op = 'transferAB'
        prev_state = transition(curr_state, op)
        curr_index = path.index(prev_state)
    new_ops.pop()
    applied_operations = new_ops[::-1]
    print_solution(new_path[::-1])


def bfs(starting_state):
    global old_states, applied_operations, found_solution

    queue = deque()
    operation_queue = deque()
    old_states = []
    applied_operations = []
    path = []
    curr_operation = ''
    queue.append(starting_state)

    iteration = 0
    while len(queue) > 0:
        curr_state = queue.popleft()
        if iteration != 0:
            curr_operation = operation_queue.popleft()

        if curr_state in old_states:
            continue
        if not is_valid(curr_state):
            continue

        path.append(curr_state)
        if iteration != 0:
            applied_operations.append(curr_operation)
        old_states.append(curr_state)

        if is_final_state(curr_state):
            found_solution = True
            print(path)
            print_solution_bfs(path)
            break

        queue.append(transition(curr_state, 'fillA'))
        operation_queue.append('fillA')
        queue.append(transition(curr_state, 'fillB'))
        operation_queue.append('fillB')

        ba_transfer_state = transition(curr_state, 'transferBA')
        operation_queue.append('transferBA')
        queue.append(ba_transfer_state)
        ab_transfer_state = transition(curr_state, 'transferAB')
        operation_queue.append('transferAB')
        queue.append(ab_transfer_state)

        queue.append(transition(curr_state, 'emptyA'))
        operation_queue.append('emptyA')
        queue.append(transition(curr_state, 'emptyB'))
        operation_queue.append('emptyB')
        iteration += 1


def is_there_solution():
    if n + m < k:
        return False
    if n == 0 and m == 0:
        if k == 0:
            return True
        else:
            return False
    if k % math.gcd(n, m) == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    init()
    if is_there_solution():
        print('There is at least one solution for the current parameters.')
    else:
        print('There is no solution for the current parameters.')

    selected_alg_value = int(input("""Select the number for the algorithm that solves the problem:
          1 - Backtracking
          2 - Breadth First Search
          3 - Hillclimbing (NYI)
          4 - A* (NYI)
          """))
    if selected_alg_value == 1:
        bkt(initial_state)
    elif selected_alg_value == 2:
        bfs(initial_state)
    elif selected_alg_value == 3:
        print('NYI')
    elif selected_alg_value == 4:
        print('NYI')
    else:
        print('No option selected!')
        exit(1)

    if not found_solution:
        print("Could not find the solution for the current parameters.")
