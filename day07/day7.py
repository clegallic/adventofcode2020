from collections import defaultdict
from functools import reduce
import re

puzzle_input = open("input.txt").read().splitlines()


def main():
    bags_that_may_contains_shiny_gold = count_bags_can_contains("shiny gold")
    number_of_individual_bags = count_bags_in("shiny gold")
    print(f"Part 1: {bags_that_may_contains_shiny_gold} bag colors can eventually contain at least one shiny gold bag")
    print(f"Part 2: {number_of_individual_bags} individual bags are required inside the shiny gold bag")


def count_bags_can_contains(bag_color):
    can_contain = defaultdict(set)
    parse_input(r"\d ([^,]+) bags?", lambda bag, content_of_bag: can_contain[content_of_bag].add(bag))
    return len(reduce(lambda acc, c: acc | rec_can_contain(c, can_contain), can_contain[bag_color], set()))


def parse_input(pattern, extractor):
    for rule in puzzle_input:
        bag, content_raw = list(re.match(r"(.+) bags contain (.+)", rule).groups())
        [extractor(bag, content_parsed) for content_parsed in re.findall(pattern, content_raw)]


def rec_can_contain(container, bags_containing):
    contained = {container}
    [contained.update(rec_can_contain(bag_color, bags_containing)) for bag_color in bags_containing[container]]
    return contained


def count_bags_in(bag_color):
    bags_content = defaultdict(set)
    parse_input(r"(\d+) ([^,]+) bags?", lambda bag, content_of_bag: bags_content[bag].add(content_of_bag))
    return count_bags(bag_color, bags_content)


def count_bags(current_bag, bags_content):
    return sum(int(qty) + int(qty) * count_bags(bag, bags_content) for qty, bag in bags_content[current_bag])


main()
