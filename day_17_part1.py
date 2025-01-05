import argparse

REGISTER_A_PREFIX = "Register A:"
REGISTER_B_PREFIX = "Register B:"
REGISTER_C_PREFIX = "Register C:"
PROGRAM_PREFIX = "Program:"


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


def execute(opcode: int, operand: int, memory: dict[str, int]) -> int:
    if opcode == 0:
        memory["A"] = int(memory["A"] /
                          (2**get_operand_value(operand, memory)))
    if opcode == 1:
        memory["B"] = operand ^ memory["B"]
    if opcode == 2:
        memory["B"] = get_operand_value(operand, memory) % 8
    if opcode == 3:
        if memory["A"] != 0:
            return operand
    if opcode == 4:
        memory["B"] = memory["B"] ^ memory["C"]
    if opcode == 5:
        print(get_operand_value(operand, memory) % 8, end=",")
    if opcode == 6:
        memory["B"] = int(memory["A"] /
                          (2**get_operand_value(operand, memory)))
    if opcode == 7:
        memory["C"] = int(memory["A"] /
                          (2**get_operand_value(operand, memory)))
    return -1


def run_program(program: tuple[int], memory: dict[str, int]) -> None:
    it = 0
    while it < len(program) - 1:
        opcode = program[it]
        operand = program[it + 1]
        # print(opcode, operand, memory)
        new_it = execute(opcode, operand, memory)
        if new_it == -1:
            it += 2
        else:
            it = new_it


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

    run_program(program, memory)
    print()
