import math
import random
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


def eval(state):
    return abs(state[0] - k) + abs(state[1] - k)


def get_neighbours(curr_state, prev_state):
    neighbours = []
    for choice in transition_choices:
        next_state = transition(prev_state, choice)
        if is_valid(next_state) and next_state != curr_state:
            neighbours.append(next_state)
    return neighbours


def mutate(curr_state, counter=0):
    index = random.randint(0, len(transition_choices) - 1)
    next_state = transition(curr_state, transition_choices[index])
    if is_valid(next_state):
        return next_state
    elif counter < len(transition_choices) * 2:
        return mutate(curr_state, counter + 1)


def hill_climbing(starting_state):
    global found_solution
    prev_state = starting_state
    has_improved = True
    max_state = starting_state
    while has_improved and not found_solution:
        has_improved = False
        max_state = mutate(prev_state)
        fitness = eval(max_state)
        for candidate in get_neighbours(max_state, prev_state):
            if candidate in old_states:
                continue
            candidate_fitness = eval(candidate)
            if candidate_fitness <= fitness:
                max_state = candidate
                fitness = candidate_fitness
                has_improved = True
            old_states.append(candidate)
            if is_final_state(candidate):
                found_solution = True
                break
        prev_state = max_state
    print(old_states)
    return max_state


def distance(curr_state, next_state):
    return abs(curr_state[0] - next_state[0]) + abs(curr_state[1] - next_state[1])


def get_lowest_scoring_node(open_set, f_score):
    minimum_value = 2 << 32
    minima = None
    for item in open_set:
        if f_score[item] < minimum_value:
            minimum_value = f_score[item]
            minima = item
    return minima


def get_next_states(curr_state):
    next_states = []
    for choice in transition_choices:
        next_state = transition(curr_state, choice)
        if is_valid(next_state):
            next_states.append(next_state)
    return next_states


def rebuild_path(came_from, curr_state):
    path = [curr_state]
    while curr_state in came_from:
        curr_state = came_from[curr_state]
        path.append(curr_state)
    return path[::-1]


def a_star(start_state):
    global found_solution, old_states

    open_set = {start_state}
    came_from = {}
    g_score = {start_state: 0}
    f_score = {start_state: eval(start_state)}
    old_states = []

    while len(open_set) > 0:
        curr_state = get_lowest_scoring_node(open_set, f_score)
        old_states.append(curr_state)
        if is_final_state(curr_state):
            found_solution = True
            print(rebuild_path(came_from, curr_state))
            print(old_states)
            break

        open_set.remove(curr_state)
        for neighbor in get_next_states(curr_state):
            if neighbor in old_states:
                continue

            if neighbor not in g_score:
                g_score[neighbor] = 2 << 32
                f_score[neighbor] = 2 << 32

            tentative_g_score = g_score[curr_state] + distance(curr_state, neighbor)
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = curr_state
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + eval(neighbor)
                if neighbor not in open_set:
                    open_set.add(neighbor)


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
          3 - Hillclimbing
          4 - A*
          """))
    if selected_alg_value == 1:
        bkt(initial_state)
    elif selected_alg_value == 2:
        bfs(initial_state)
    elif selected_alg_value == 3:
        hill_climbing(initial_state)
    elif selected_alg_value == 4:
        a_star(initial_state)
    else:
        print('No option selected!')
        exit(1)

    if not found_solution:
        print("Could not find the solution for the current parameters.")
