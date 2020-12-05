from functools import reduce


def compute_part_id(pass_part, start, upper_letter):
    return reduce(lambda acc, c: acc + pow(2, start - c[0]) if c[1] == upper_letter else acc, enumerate(pass_part), 0)


def compute_id(b_pass):
    return compute_part_id(b_pass[0:7], 6, 'B') * 8 + compute_part_id(b_pass[7:10], 2, 'R')


def find_highest_id(boarding_passes):
    return max(map(compute_id, boarding_passes))


def find_my_seat(boarding_passes):
    ids = sorted(map(compute_id, boarding_passes))
    for c in enumerate(ids):
        if c[1] != ids[c[0] + 1] - 1:
            return c[1] + 1


def find_my_seat_one_line(boarding_passes):
    return reduce(lambda acc, c: (c, acc[1]) if c == acc[0] + 1 else (c, c - 1), sorted(map(compute_id, boarding_passes)), (0, 0))[1]


puzzle_input = [list(line) for line in open("input.txt").read().splitlines()]
highest_id = find_highest_id(puzzle_input)
my_seat_id = find_my_seat_one_line(puzzle_input)
print(f"Part one : the highest seat ID on a boarding pass is {highest_id}")
print(f"Part two : my seat ID is {my_seat_id}")
