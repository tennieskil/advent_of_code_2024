import argparse

MIN_DIFF = 1
MAX_DIFF = 3


def get_differences(numbers: list[int]) -> list[int]:
    return [numbers[i] - numbers[i + 1] for i in range(len(numbers) - 1)]


def get_differences_with_index_to_skip(numbers: list[int],
                                       index_to_skip: int) -> list[int]:
    new_numbers = [
        numbers[i] for i in range(len(numbers)) if not i == index_to_skip
    ]
    return get_differences(new_numbers)


def is_difference_safe(differences: list[int]) -> bool:
    all_increasing = all(
        [MIN_DIFF <= diff <= MAX_DIFF for diff in differences])
    all_decreasing = all(
        [MIN_DIFF <= -diff <= MAX_DIFF for diff in differences])
    return all_increasing or all_decreasing


def is_safe(line_numbers: list[str]) -> bool:
    if len(line_numbers) == 1:
        return True
    numbers = list(map(int, line_numbers))
    original_differences = [
        numbers[i] - numbers[i + 1] for i in range(len(numbers) - 1)
    ]
    if is_difference_safe(original_differences):
        return True
    for index_to_skip in range(len(numbers)):
        differences = get_differences_with_index_to_skip(
            numbers, index_to_skip)
        if is_difference_safe(differences):
            return True
    return False


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
