puzzle_input = [int(n) for n in open("input.txt").read().splitlines()]


def find_2020_with_two_entries():
    for i, n1 in enumerate(puzzle_input):
        for n2 in puzzle_input[i + 1:]:
            if n1 + n2 == 2020:
                return n1 * n2


def find_2020_with_three_entries():
    for i, n1 in enumerate(puzzle_input):
        for n2 in puzzle_input[i + 1:]:
            for n3 in puzzle_input[i + 2:]:
                if n1 + n2 + n3 == 2020:
                    return n1 * n2 * n3


result_two_entries = find_2020_with_two_entries()
print("The product of the two entries that sum to 2020 is '{}'".format(result_two_entries))

result_three_entries = find_2020_with_three_entries()
print("The product of the three entries that sum to 2020 is '{}'".format(result_three_entries))
