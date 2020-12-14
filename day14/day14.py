import re

puzzle_input = [line for line in open("input.txt").read().splitlines()]


def main():
    result_part_one = sum_of_all_values_in_memory_part_one(puzzle_input)
    print(f"Part one : the sum of all values left in memory after it completes is {result_part_one}")
    result_part_two = sum_of_all_values_in_memory_part_two(puzzle_input)
    print(f"Part two : the sum of all values left in memory after it completes is {result_part_two}")


def sum_of_all_values_in_memory_part_one(program_lines):
    memory = dict()
    mask = None
    for line in program_lines:
        instruction, value = line.split(" = ")
        if instruction == "mask":
            mask = list(value)
        else:
            memory_address = int(re.search(r"mem\[(\d+)]", instruction).group(1))
            binary_value = list(format(int(value), "036b"))
            binary_with_mask = "".join([mask_value if mask_value != "X" else binary_value[i] for i, mask_value in
                                        enumerate(mask)])
            memory[memory_address] = int(binary_with_mask, 2)
    return sum(value for value in memory.values())


def sum_of_all_values_in_memory_part_two(program_lines):
    memory = dict()
    mask = None
    for line in program_lines:
        instruction, value = line.split(" = ")
        if instruction == "mask":
            mask = ["X" if i == "X" else int(i) for i in value]
        else:
            memory_address = int(re.search(r"mem\[(\d+)]", instruction).group(1))
            binary_value = [int(i) for i in list(format(int(memory_address), "036b"))]
            binary_with_mask = ["X" if m_value == "X" else binary_value[i] | m_value for i, m_value in enumerate(mask)]
            for address in get_permutations(binary_with_mask):
                memory[address] = int(value)
    return sum(value for value in memory.values())


def get_permutations(masked_address):
    x_index = masked_address.index("X") if "X" in masked_address else -1
    if x_index == -1:
        return [int("".join([str(i) for i in masked_address]), 2)]
    perm_0, perm_1 = masked_address.copy(), masked_address.copy()
    perm_0[x_index] = 0
    perm_1[x_index] = 1
    return get_permutations(perm_0) + get_permutations(perm_1)


main()
