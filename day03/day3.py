from functools import reduce

puzzle_input = [list(line) for line in open("input.txt").read().splitlines()]


class Offset:
    def __init__(self, x, y):
        self.x = x
        self.y = y


OFFSETS = [Offset(3, 1), Offset(1, 1), Offset(5, 1), Offset(7, 1), Offset(1, 2)]
map_len = len(puzzle_input[0])


def count_number_of_trees(offset):
    (pos_x, pos_y) = (0, 0)
    number_of_trees = 0
    while pos_y < len(puzzle_input):
        number_of_trees += 1 if puzzle_input[pos_y][pos_x] == "#" else 0
        (pos_x, pos_y) = ((pos_x + offset.x) % map_len, pos_y + offset.y)
    return number_of_trees


part_one_result = count_number_of_trees(OFFSETS[0])
part_two_result = reduce(lambda a, b: a * count_number_of_trees(b), OFFSETS, 1)
print(f"Part one : i will encounter {part_one_result} trees")
print(f"Part two : result is {part_two_result} ")
