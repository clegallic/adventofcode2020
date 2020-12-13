from functools import reduce
puzzle_input = [line.split(",") if line.count(",") > 0 else int(line) for line in open("input.txt").read().splitlines()]


def main():
    result_part_one = find_bus(puzzle_input[0], puzzle_input[1])
    print(f"Part one : the ID of the earliest bus I can take to the airport multiplied by the number of minutes you'll need to wait for that bus is {result_part_one}")
    result_part_two = find_earliest_timestamp(puzzle_input[1])
    print(f"Part two : the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list is {result_part_two}")


def find_bus(earliest_ts, departs):
    bus_id = int(departs[
        sorted(
            [(i, (earliest_ts / (int(depart) % 60)) % 1) for i, depart in enumerate(departs) if depart != "x"],
            key=lambda x: x[1], reverse=True
        )[0][0]])
    return bus_id * (bus_id - earliest_ts % bus_id)


# Chinese remainder, many thanks JF (https://github.com/Alleton) !
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem
def find_earliest_timestamp(departs):
    remainders_modulos = [(int(modulo) - int(remainder) if remainder != 0 else 0, int(modulo)) for remainder, modulo in enumerate(departs) if modulo != "x"]
    prod_of_modulos = reduce(lambda acc, modulo: acc * modulo, [modulo for _, modulo in remainders_modulos])
    prod_per_modulos = [int(prod_of_modulos / modulo) for _, modulo in remainders_modulos]
    inverse_modulos = [pow(prod_per_modulos[i], -1, modulo) for i, (_, modulo) in enumerate(remainders_modulos)]
    return sum([remainder * prod_per_modulos[i] * inverse_modulos[i] for i, (remainder, _) in enumerate(remainders_modulos)]) % prod_of_modulos


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

main()
