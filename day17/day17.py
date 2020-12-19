import itertools
import functools
import operator

puzzle_input = open("input.txt").read()


def main():
    nb_cycles = 6
    result_part_one = count_active_cubes_after_n_cycles(puzzle_input, 3, nb_cycles)
    print(f"Part one : there are {result_part_one} cubes left in the active state after {nb_cycles} cycles")
    result_part_two = count_active_cubes_after_n_cycles(puzzle_input, 4, nb_cycles)
    print(f"Part one : there are {result_part_two} cubes left in the active state after {nb_cycles} cycles")


def count_active_cubes_after_n_cycles(p_input, dimension, last_cycle):
    current_matrix = build_initial_matrix(p_input, dimension)
    for _ in range(last_cycle):
        current_matrix = run_cycle(current_matrix, dimension)
    return sum(current_matrix.values())


def build_initial_matrix(p_input, dimension):
    states_matrix = dict()
    for y, line in enumerate(p_input.splitlines()):
        for x, state in enumerate(line):
            position = tuple([x, y] + list(itertools.repeat(0, dimension - 2)))
            states_matrix[position] = 1 if state == "#" else 0
    return states_matrix


def run_cycle(current_matrix, dimension):
    new_matrix = dict()
    for position, state in current_matrix.items():
        for adjacent_p in [p for p in adjacent_cubes_positions(position, dimension) if p not in new_matrix]:
            nb_adjacent = count_adjacent_active_cubes(adjacent_p, current_matrix, dimension)
            if is_active(adjacent_p, current_matrix):
                new_matrix[adjacent_p] = 1 if nb_adjacent in [2, 3] else 0
            else:
                new_matrix[adjacent_p] = 1 if nb_adjacent == 3 else 0
    return new_matrix


def count_adjacent_active_cubes(position, matrix, dimension):
    adjacents = adjacent_cubes_positions(position, dimension)
    nb_active = functools.reduce(lambda acc, p: acc + 1 if is_active(p, matrix) else acc, adjacents, 0)
    return nb_active


def adjacent_cubes_positions(position, dimension):
    return [tuple(map(operator.add, position, offset))
            for offset in itertools.product(*itertools.repeat(list(range(-1, 2)), dimension))
            if offset != tuple(itertools.repeat(0, dimension))]


def is_active(position, matrix):
    return position in matrix and matrix[position] == 1


main()
