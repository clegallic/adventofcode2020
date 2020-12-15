puzzle_input = [line.split(",") for line in open("input.txt").read().splitlines()]


def main():
    result_part_one = number_spoken_at(puzzle_input[0], 2020)
    print(f"Part one : the 2020th number spoken is {result_part_one}")
    result_part_two = number_spoken_at(puzzle_input[0], 30000000)
    print(f"Part two : the 30000000th number spoken is {result_part_two} (with brute force :))")


def number_spoken_at(p_input, target_turn):
    spoken_numbers = [0] + [int(starting_number) for starting_number in p_input]
    history = dict([(int(starting_number), [turn]) for turn, starting_number in enumerate(p_input, 1)])
    for turn in range(len(spoken_numbers), target_turn + 1):
        last_number = spoken_numbers[turn - 1]
        last_number_history = history[last_number]
        if last_number_history is None or len(last_number_history) == 1:
            spoken_numbers.append(0)
        else:
            spoken_numbers.append(last_number_history[1] - last_number_history[0])
            last_number_history.pop(0)
        if spoken_numbers[turn] in history:
            history[spoken_numbers[turn]].append(turn)
        else:
            history[spoken_numbers[turn]] = [turn]
    return spoken_numbers[-1]


main()
