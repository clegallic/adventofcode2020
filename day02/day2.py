import re

puzzle_input = open("input.txt").read().splitlines()

password_policy_re = re.compile(r"(?P<min>[0-9]+)-(?P<max>[0-9]+) (?P<letter>[a-z]): (?P<password>[a-z]+)")


def extract_policy(password_policy):
    groups = password_policy_re.match(password_policy)
    return (
        int(groups.group("min")), int(groups.group("max")), groups.group("letter"), groups.group("password")
    )


def is_valid_password_policy_part_one(password_policy):
    min_letter, max_letter, letter, password = extract_policy(password_policy)
    return min_letter <= password.count(letter) <= max_letter


def is_valid_password_policy_part_two(password_policy):
    first_position, second_position, letter, password = extract_policy(password_policy)
    return (password[first_position - 1] == letter and password[second_position - 1] != letter) or (password[first_position - 1] != letter and password[second_position - 1] == letter)


def count_valid_passwords(is_valid_function):
    return len([valid_password for valid_password in puzzle_input if is_valid_function(valid_password)])


valid_passwords = count_valid_passwords(is_valid_password_policy_part_one)
print("Part one : there are '{}' valid passwords".format(valid_passwords))

valid_passwords = count_valid_passwords(is_valid_password_policy_part_two)
print("Part two : there are '{}' valid passwords".format(valid_passwords))
