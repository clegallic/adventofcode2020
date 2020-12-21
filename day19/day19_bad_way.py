import functools

puzzle_input = open("input.txt").read()


def main():
    result_part_one = count_matching_messages(puzzle_input)
    print(f"Part one : {result_part_one} messages completely match rule 0")


def count_matching_messages(p_input):
    raw_rules, messages = extract_rules_messages(p_input)
    rules = parse_raw_rules(raw_rules)
    all_possibilities = build_all_possibilities(rules)
    return functools.reduce(lambda acc, message: acc + 1 if message in all_possibilities else acc, messages, 0)


def extract_rules_messages(p_input):
    rules, messages = p_input.split("\n\n")
    return rules.splitlines(), messages.splitlines()


def parse_raw_rules(raw_rules):
    rules = dict()
    for raw_rule in raw_rules:
        rule_number, rule_content = raw_rule.split(": ")
        rule_options = rule_content.split(" | ")
        rules[rule_number] = [rule_option.split(" ") for rule_option in rule_options]
    return rules


def build_all_possibilities(rules):
    return build_possibilities('0', rules)


possibilities_cache_per_number = dict()


def build_possibilities(rule_number, rules):
    if rule_number in possibilities_cache_per_number:
        return possibilities_cache_per_number[rule_number]
    else:
        possibilities = list()
        for sub_rules in rules[rule_number]:
            if sub_rules in [['"a"'], ['"b"']]:
                sub_possibilities = [sub_rules[0].replace('"', '')]
            else:
                sub_possibilities = proceed_sub_rules(sub_rules, rules)
            for sub_possibility in sub_possibilities:
                possibilities.append(sub_possibility)
        possibilities_cache_per_number[rule_number] = possibilities
        return possibilities


possibilities_cache_per_rules = dict()


def proceed_sub_rules(sub_rules, rules):
    if "".join(sub_rules) in possibilities_cache_per_rules:
        return possibilities_cache_per_rules["".join(sub_rules)]
    else:
        possibilities = list()
        for sub_rule_number in sub_rules:
            sub_possibilities = build_possibilities(sub_rule_number, rules)
            if len(possibilities) == 0:
                possibilities = sub_possibilities
            else:
                new_possibilities = list()
                for possibility in possibilities:
                    for sub_possibility in sub_possibilities:
                        new_possibilities.append(possibility + sub_possibility)
                possibilities = new_possibilities
        possibilities_cache_per_rules["".join(sub_rules)] = possibilities
        return possibilities


main()
