puzzle_input = [int(n) for n in open("input.txt").read().splitlines()]


def find_sum_of(sum_to_find, serie):
    for i, n1 in enumerate(serie):
        for n2 in serie[i + 1:]:
            if n1 + n2 == sum_to_find:
                return True
    return False


def check_serie(serie):
    return find_sum_of(serie[-1], serie[:-1])


def find_weakness_number(serie, preamble_size):
    i = 0
    while check_serie(serie[i:preamble_size + i + 1]):
        i += 1
    return serie[preamble_size + i]


def can_sum_contiguous_sums_to(serie, target_sum, start_index):
    current_sum = 0
    for i, value in enumerate(serie[start_index:]):
        current_sum += value
        if current_sum == target_sum:
            return start_index + i
        if current_sum > target_sum:
            return -1


def find_contiguous_sums_to(serie, target_sum):
    for i in range(len(serie)):
        result = can_sum_contiguous_sums_to(serie, target_sum, i)
        if result > 0:
            return max(serie[i:result]) + min(serie[i:result])
        i += 1


def main():
    weakness_number = find_weakness_number(puzzle_input, 25)
    print(f"Part one : the first number that does not have this property is {weakness_number}")
    encryption_weakness = find_contiguous_sums_to(puzzle_input, weakness_number)
    print(f"Part two : the encryption weakness in my XMAS-encrypted list of numbers is {encryption_weakness}")

main()
