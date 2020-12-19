import re
from functools import reduce
import itertools
import operator

puzzle_input = open("input.txt").read()


def main():
    result_part_one = ticket_scanning_error_rate(puzzle_input)
    print(f"Part one : the ticket scanning error rate is {result_part_one}")
    result_part_two = find_fields(puzzle_input)
    print(f"Part two : if I multiply those six values together, the result is {result_part_two}")


def ticket_scanning_error_rate(p_input):
    parts = extract_parts(p_input)
    rules = [r.split("-") for r in
             reduce(lambda acc, v: acc + v, [rule.split(": ")[1].split(" or ") for rule in parts[0]])]
    nearby_tickets_values = itertools.chain.from_iterable(parse_tickets(parts[2]))
    error_rate = 0
    for nearby_ticket_value in nearby_tickets_values:
        if len([rule for rule in rules if int(rule[0]) <= nearby_ticket_value <= int(rule[1])]) == 0:
            error_rate += nearby_ticket_value
    return error_rate


def extract_parts(p_input):
    return [part.splitlines() for part in re.split(r"\n\s*\n", p_input)]


def parse_tickets(tickets_part):
    return list(map(lambda line: list(map(int, line.split(","))), tickets_part[1:]))


def find_fields(p_input):
    parts = extract_parts(p_input)
    rules = dict([
        (field, list(map(lambda x: list(map(int, x.split("-"))), field_rule.split(" or "))))
        for field, field_rule in [rule.split(": ") for rule in parts[0]]
    ])
    my_ticket = parse_tickets(parts[1])[0]
    all_valid_tickets = exclude_invalid_tickets(rules, parse_tickets(parts[2]))
    impossible_field_post = dict([])
    possible_field_pos = dict([])
    for ticket in all_valid_tickets:
        for pos, ticket_value in enumerate(ticket):
            for field_name, field_rules in rules.items():
                if field_name in impossible_field_post and pos in impossible_field_post[field_name]:
                    continue
                fit_at_least_one_rule = False
                for field_rule in field_rules:
                    if field_rule[0] <= ticket_value <= field_rule[1]:
                        if field_name in possible_field_pos:
                            possible_field_pos[field_name].add(pos)
                        else:
                            possible_field_pos[field_name] = {pos}
                        fit_at_least_one_rule = True
                if not fit_at_least_one_rule:
                    if field_name in possible_field_pos and pos in possible_field_pos[field_name]:
                        possible_field_pos[field_name].remove(pos)
                    if field_name in impossible_field_post:
                        impossible_field_post[field_name].add(pos)
                    else:
                        impossible_field_post[field_name] = {pos}
    remaining_multiple_pos = len(possible_field_pos)
    while remaining_multiple_pos > 0:
        fields_with_unique_pos = {field_name: list(pos)[0] for field_name, pos in possible_field_pos.items() if len(pos) == 1}
        for field_name, pos in possible_field_pos.items():
            if field_name not in fields_with_unique_pos:
                already_taken_pos = list(fields_with_unique_pos.values())
                possible_field_pos[field_name] = pos.difference(already_taken_pos)
                if len(possible_field_pos[field_name]) == 1:
                    fields_with_unique_pos[field_name] = list(possible_field_pos[field_name])[0]
        remaining_multiple_pos = len(possible_field_pos) - len(fields_with_unique_pos)
    departure_fields_pos = [pos for field_name, pos in fields_with_unique_pos.items() if field_name.startswith("departure")]
    my_ticket_departure_values = [value for i, value in enumerate(my_ticket) if i in departure_fields_pos]
    return reduce(operator.mul, my_ticket_departure_values)


def exclude_invalid_tickets(rules, tickets):
    flattened_rules = list(itertools.chain.from_iterable(rules.values()))
    valid_tickets = list()
    for ticket in tickets:
        if len([ticket_value for ticket_value in ticket
                if len([rule for rule in flattened_rules if rule[0] <= ticket_value <= rule[1]])]
               ) == len(ticket):
            valid_tickets.append(ticket)
    return valid_tickets


main()
