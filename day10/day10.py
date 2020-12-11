puzzle_input = [int(n) for n in open("input.txt").read().splitlines()]


def find_differences_in_jolts(adapters):
    number_of_1, number_of_3 = 1, 0
    adapter_jolts = sorted(adapters) + [max(adapters) + 3]
    for i, adapter_jolt in enumerate(adapter_jolts[:-1]):
        diff = adapter_jolts[i + 1] - adapter_jolt
        if diff == 1:
            number_of_1 += 1
        else:
            number_of_3 += 1
    return number_of_1 * number_of_3


sum_of_possibilities = dict()


def get_possibilies(adapter_jolts, possibilies, i):
    if i in sum_of_possibilities:
        return sum_of_possibilities[i]
    if i == len(adapter_jolts):
        return 1
    sum_of_possibilities[i] = sum(get_possibilies(adapter_jolts, possibilies, p_i) for p_i in possibilies[i])
    return sum_of_possibilities[i]


def find_distinct_combinations_rec(adapters):
    adapter_jolts = [0] + sorted(adapters)
    possibilies = dict()
    for i, jolt in enumerate(adapter_jolts):
        possibilies[i] = [i + 1]
        if i + 2 < len(adapter_jolts) and adapter_jolts[i + 2] == jolt + 2:
            possibilies[i] += [i + 2]
        if i + 3 < len(adapter_jolts) and adapter_jolts[i + 3] == jolt + 3:
            possibilies[i] += [i + 3]
    return get_possibilies(adapter_jolts, possibilies, 0)


def main():
    result_part_one = find_differences_in_jolts(puzzle_input)
    result_part_two = find_distinct_combinations_rec(puzzle_input)
    print(f"Part one : the number of 1-jolt differences multiplied by the number of 3-jolt differences is {result_part_one}")
    print(f"Part two : the total number of distinct ways to arrange the adapters is {result_part_two}")


main()
