import re

puzzle_input = open("input.txt").read()

MANDATORY_PASSPORT_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
BYR_RULE = r"byr:(19[2-9]\d|200[0-2])(\s|$)"  # at least 1920 and at most 2002
IYR_RULE = r"iyr:(20(1\d|20))(\s|$)"  # at least 2010 and at most 2020
EYR_RULE = r"eyr:(20(2\d|30))(\s|$)"  # at least 2020 and at most 2030
HGT_RULE = r"hgt:(1([5-8]\d|9[0-3])cm|(59|6\d|7[0-6])in)(\s|$)"  # cm : 150=<hgt>=193, in: 59=<hgt>=76
HCL_RULE = r"hcl:#[a-z0-9]{6}(\s|$)"  # a # followed by exactly six characters 0-9 or a-f
ECL_RULE = r"ecl:(amb|blu|brn|gry|grn|hzl|oth)(\s|$)"  # exactly one of: amb blu brn gry grn hzl oth
PID_RULE = r"pid:[0-9]{9}(\s|$)"  # a nine-digit number, including leading zeroes
ALL_RULES = [BYR_RULE, IYR_RULE, EYR_RULE, HGT_RULE, HCL_RULE, ECL_RULE, PID_RULE]


def extract_passports():
    return re.split(r"\n\s*\n", puzzle_input)


def has_all_fields(passport_fields):
    return all(field in passport_fields for field in MANDATORY_PASSPORT_FIELDS)


def all_fields_matches(passport_fields):
    return all(re.search(rule, passport_fields) for rule in ALL_RULES)


def count_valid_passports(validation_function):
    return len(list(filter(lambda fields: validation_function(fields), extract_passports())))


def count_valid_passports_part_one():
    return count_valid_passports(has_all_fields)


def count_valid_passports_part_two():
    return count_valid_passports(all_fields_matches)


print(f"Part one : there are {count_valid_passports_part_one()} valid passports")
print(f"Part two : there are {count_valid_passports_part_two()} valid passports")
