from functools import reduce


def sum_anyone_yes(p_input):
    parsed_input = p_input.replace("\n\n", "|").replace("\n", "").split("|")
    return sum(len(dict.fromkeys(answers)) for answers in parsed_input)


def count_everyone_yes(answers):
    return len(reduce(lambda acc, answer: set(answer) & acc, answers[1:], set(answers[0])))


def sum_everyone_yes(p_input):
    parsed_input = [group.splitlines() for group in p_input.split("\n\n")]
    return sum(count_everyone_yes(answers) for answers in parsed_input)


puzzle_input = open("input.txt").read()
print(sum_anyone_yes(puzzle_input))
print(sum_everyone_yes(puzzle_input))
