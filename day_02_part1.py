import argparse

MIN_DIFF = 1
MAX_DIFF = 3


def is_safe(line_numbers) -> bool:
    if len(line_numbers) == 1:
        return True
    numbers = list(map(int, line_numbers))
    differences = [
        numbers[i] - numbers[i + 1] for i in range(len(numbers) - 1)
    ]
    all_increasing = all(
        [MIN_DIFF <= diff <= MAX_DIFF for diff in differences])
    all_decreasing = all(
        [MIN_DIFF <= -diff <= MAX_DIFF for diff in differences])
    return all_increasing or all_decreasing


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    n_safe_levels = 0
    with open(args.filename, "r") as file:
        for line in file:
            line_numbers = line.strip().split(" ")
            if is_safe(line_numbers):
                n_safe_levels += 1
    print(n_safe_levels)
