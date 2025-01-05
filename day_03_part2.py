import argparse
import re


def get_nonempty_group(group_match: tuple[str, ...]) -> str:
    for match in group_match:
        if match:
            return match
    raise ValueError("Invalid group match")


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

    group_matches = re.findall(
        r"(mul\(\d\d?\d?,\d\d?\d?\))|(do\(\))|(don't\(\))", memory)
    matches = [
        get_nonempty_group(group_match) for group_match in group_matches
    ]

    result = 0
    do = True
    for match in matches:
        if match == "do()":
            do = True
        elif match == "don't()":
            do = False
        elif do:
            result += multiply(match)
    print(result)
