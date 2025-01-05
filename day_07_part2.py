import argparse


def is_solvable(partial_result, numbers, next_index, final_result) -> bool:
    if partial_result == final_result and next_index == len(numbers):
        return True
    if next_index >= len(numbers):
        return False
    if partial_result > final_result:
        return False
    if is_solvable(partial_result + numbers[next_index], numbers,
                   next_index + 1, final_result):
        return True
    if is_solvable(partial_result * numbers[next_index], numbers,
                   next_index + 1, final_result):
        return True
    if is_solvable(int(str(partial_result) + str(numbers[next_index])),
                   numbers, next_index + 1, final_result):
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    equations = []
    with open(args.filename, "r") as file:
        equations = [line.strip() for line in file]

    solvable_sum = 0
    for equation in equations:
        parts = [part.strip() for part in equation.split(':')]
        result = int(parts[0])
        numbers = [int(n) for n in parts[1].split(' ')]
        if is_solvable(numbers[0], numbers, 1, result):
            solvable_sum += result

    print(solvable_sum)
