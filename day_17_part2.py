import argparse
import dataclasses

REGISTER_A_PREFIX = "Register A:"
REGISTER_B_PREFIX = "Register B:"
REGISTER_C_PREFIX = "Register C:"
PROGRAM_PREFIX = "Program:"


@dataclasses.dataclass
class ProgramState:
    output: list[int]
    it: int
    memory: dict[str, int]


def get_operand_value(operand: int, memory: dict[str, int]) -> int:
    if 0 <= operand < 4:
        return operand
    if operand == 4:
        return memory["A"]
    if operand == 5:
        return memory["B"]
    if operand == 6:
        return memory["C"]
    raise ValueError(f"Invalid operand {operand}")


def execute(opcode: int, operand: int, state: ProgramState) -> None:
    if opcode == 0:
        state.memory["A"] = int(state.memory["A"] /
                                (2**get_operand_value(operand, state.memory)))
    if opcode == 1:
        state.memory["B"] = operand ^ state.memory["B"]
    if opcode == 2:
        state.memory["B"] = get_operand_value(operand, state.memory) % 8
    if opcode == 3:
        if state.memory["A"] != 0:
            state.it = operand
            return
    if opcode == 4:
        state.memory["B"] = state.memory["B"] ^ state.memory["C"]
    if opcode == 5:
        state.output.append(get_operand_value(operand, state.memory) % 8)
    if opcode == 6:
        state.memory["B"] = int(state.memory["A"] /
                                (2**get_operand_value(operand, state.memory)))
    if opcode == 7:
        state.memory["C"] = int(state.memory["A"] /
                                (2**get_operand_value(operand, state.memory)))
    state.it += 2


def run_program(program: tuple[int], memory: dict[str, int]) -> list[int]:
    state = ProgramState([], 0, memory)
    while state.it < len(program) - 1:
        opcode = program[state.it]
        operand = program[state.it + 1]
        execute(opcode, operand, state)
    return state.output


def find_a(program: tuple[int]) -> int:
    valid_a = [0]
    for number in program[::-1]:
        new_valid_a = []
        for a in valid_a:
            for three_bit_combination in range(8):
                new_a = a * 8 + three_bit_combination
                printed_number = (5 ^ 6 ^ (new_a % 8) ^
                                  (new_a >> (5 ^ (new_a % 8)))) % 8
                if number == printed_number:
                    new_valid_a.append(new_a)
        valid_a = new_valid_a
    return valid_a


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    memory = {}
    program = None
    with open(args.filename, "r") as file:
        for line in file:
            if line.startswith(REGISTER_A_PREFIX):
                memory["A"] = int(line[len(REGISTER_A_PREFIX):].strip())
            if line.startswith(REGISTER_B_PREFIX):
                memory["B"] = int(line[len(REGISTER_B_PREFIX):].strip())
            if line.startswith(REGISTER_C_PREFIX):
                memory["C"] = int(line[len(REGISTER_C_PREFIX):].strip())
            if line.startswith(PROGRAM_PREFIX):
                program = tuple(
                    map(int, line[len(PROGRAM_PREFIX):].strip().split(",")))

    valid_a = find_a(program)
    options = sorted(valid_a)
    print(options[0])
