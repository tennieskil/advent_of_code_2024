import argparse
import re


def multiply(multiplication: str) -> int:
    numbers = [int(n) for n in re.findall(r"\d\d?\d?", multiplication)]
    return numbers[0] * numbers[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    memory = None
    with open(args.filename, "r") as file:
        memory_parts = [line for line in file]
        memory = "".join(memory_parts)

    multiplications = re.findall(r"mul\(\d\d?\d?,\d\d?\d?\)", memory)
    result = sum(
        [multiply(multiplication) for multiplication in multiplications])
    print(result)
