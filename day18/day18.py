import re
import functools

puzzle_input = [line for line in open("input.txt").read().splitlines()]


def main():
    result_part_one = sum_of_all_values(puzzle_input, eval_formula_part_one)
    print(f"Part one : the sum of the resulting values is {result_part_one}")
    result_part_two = sum_of_all_values(puzzle_input, eval_formula_part_two)
    print(f"Part two : the sum of the resulting values is {result_part_two}")


def sum_of_all_values(p_input, eval_formula_function):
    return sum([sum_of_values(line, eval_formula_function) for line in p_input])


def sum_of_values(input_formula, eval_formula_function):
    pattern = r"\([^\(\)]+\)"
    formula = input_formula
    while re.search(pattern, formula):
        formula = re.sub(pattern, lambda formula_match: eval_formula_match(formula_match, eval_formula_function), formula)
    result = int(eval_formula_function(formula))
    return result


def eval_formula_match(formula_match, eval_formula_function):
    return eval_formula_function(formula_match.group()[1:-1])


def eval_formula_part_one(formula):
    first_term = re.match(r"\d+", formula).group()
    other_terms = re.findall(r"\s[+*]\s\d+", formula[len(first_term):])
    return str(functools.reduce(lambda left, right: str(eval(left + right)), other_terms, first_term))


def eval_formula_part_two(formula):
    while "+" in formula:
        formula = re.sub(r"(\d+\s\+\s\d+)", lambda match: str(eval(match.group())), formula)
    return str(eval(formula))


main()
