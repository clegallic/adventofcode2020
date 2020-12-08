from copy import deepcopy

puzzle_input = open("input.txt").read().splitlines()
debug = False


class CodeInterpreter:
    def __init__(self, code_input, show_debug=False):
        self.instructions = code_input if isinstance(code_input[0], Instruction) else self.parse_instructions(code_input)
        self.current_instruction_index = 0
        self.already_processes_indices = set()
        self.accumulator = 0
        self.debug = show_debug
        self.is_valid = False

    @staticmethod
    def parse_instructions(instructions_input):
        return [Instruction(instruction_input) for instruction_input in instructions_input]

    def proceed_instructions(self):
        while not self.__proceed_next_instruction():
            pass
        return InterpreterResult(self.accumulator, self.is_valid)

    def __proceed_next_instruction(self):
        instruction = self.instructions[self.current_instruction_index]
        self.__debug(f"{self.current_instruction_index} (Acc = {self.accumulator}) : {instruction}")
        self.already_processes_indices.add(self.current_instruction_index)
        if instruction.operation == Instruction.ACCUMULATOR:
            self.accumulator += instruction.argument
            self.current_instruction_index += 1
        elif instruction.operation == Instruction.JUMP:
            self.current_instruction_index += instruction.argument
        else:
            self.current_instruction_index += 1
        self.is_valid = self.current_instruction_index not in self.already_processes_indices and self.current_instruction_index <= len(self.instructions)
        return not self.is_valid or self.current_instruction_index == len(self.instructions)

    def __debug(self, message):
        if self.debug:
            print(message)


class InterpreterResult:
    def __init__(self, accumulator, is_valid):
        self.accumulator = accumulator
        self.is_valid = is_valid


class Instruction:
    NOOP = "nop"
    ACCUMULATOR = "acc"
    JUMP = "jmp"

    def __init__(self, as_string):
        splitted = as_string.split(" ")
        self.operation, self.argument = splitted[0], int(splitted[1])

    def __str__(self):
        return f"{self.operation} -> {'+' if self.argument > 0 else ''}{self.argument}"


def find_corrupted_instruction(instructions_input):
    instructions = CodeInterpreter.parse_instructions(instructions_input)
    for i, instruction in enumerate(instructions):
        if instruction.operation == Instruction.NOOP or instruction.operation == Instruction.JUMP:
            new_instructions = deepcopy(instructions)
            new_instructions[i].operation = Instruction.NOOP if instruction.operation == Instruction.JUMP else Instruction.NOOP
            result = CodeInterpreter(new_instructions, debug).proceed_instructions()
            if result.is_valid:
                return result.accumulator


def main():
    boot_code_interpreter = CodeInterpreter(puzzle_input, debug)
    print(f"Part 1 : the accumulator is {boot_code_interpreter.proceed_instructions().accumulator}")
    print(f"Part 2 : the accumulator with fixed instructions is {find_corrupted_instruction(puzzle_input)}")


main()
