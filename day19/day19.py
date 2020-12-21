import functools

puzzle_input = open("input.txt").read()
global respects_any_rule_cache
global respects_all_rules_cache


def main():
    result_part_one = count_matching_messages(puzzle_input)
    print(f"Part one : {result_part_one} messages completely match rule 0")
    result_part_two = count_matching_messages(puzzle_input, True)
    print(f"Part two : {result_part_two} messages completely match rule 0")


def count_matching_messages(p_input, part_two=False):
    raw_rules, messages = extract_rules_messages(p_input)
    global respects_any_rule_cache, respects_all_rules_cache
    respects_any_rule_cache, respects_all_rules_cache = dict(), dict()
    rules = parse_raw_rules(raw_rules)
    rule_0 = rules['0'][0]
    if part_two:
        rules["8"] = [["42"], ["42", "8"]]
        rules["11"] = [["42", "31"], ["42", "11", "31"]]
    return functools.reduce(lambda acc, message: acc + 1 if respects_all_rules(message, rule_0, rules) else acc,
                            messages, 0)


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


def respects_any_rule(message_part, rule_number, rules):
    if message_part + rule_number in respects_any_rule_cache:
        return respects_any_rule_cache[message_part + rule_number]
    any_rule_respected = False
    if is_a_b_rule(rule_number, rules):
        any_rule_respected = message_part == rules[rule_number][0][0].replace('"', '')
    elif len(message_part) == 1 and is_a_b_rule(rule_number, rules):
        any_rule_respected = False
    else:
        for sub_rule_numbers in rules[rule_number]:  # [1, 2] or [4, 1, 5]
            any_rule_respected = any_rule_respected or respects_all_rules(message_part, sub_rule_numbers, rules)
    respects_any_rule_cache[message_part + rule_number] = any_rule_respected
    return any_rule_respected


def is_a_b_rule(rule_number, rules):
    return rules[rule_number][0] in [['"a"'], ['"b"']]


def respects_all_rules(message_part, sub_rule_numbers, rules):
    if message_part + "_".join(sub_rule_numbers) in respects_all_rules_cache:
        return respects_all_rules_cache[message_part + "_".join(sub_rule_numbers)]
    if len(sub_rule_numbers) == 1:  # Single rule number, must match this rule only
        return respects_any_rule(message_part, sub_rule_numbers[0], rules)
    sub_rules_respected = False
    message_sub_part_index = 1
    while not sub_rules_respected and message_sub_part_index != len(message_part):
        left, right = message_part[:message_sub_part_index], message_part[message_sub_part_index:]
        left_respected = respects_any_rule(left, sub_rule_numbers[0], rules)
        sub_rules_respected = left_respected and respects_all_rules(right, sub_rule_numbers[1:], rules)
        message_sub_part_index += 1
    respects_all_rules_cache[message_part + "_".join(sub_rule_numbers)] = sub_rules_respected
    return sub_rules_respected


main()
