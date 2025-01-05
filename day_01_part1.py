import argparse

if __name__ == "__main__":
    left_numbers = []
    right_numbers = []
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    with open(args.filename, "r") as file:
        for line in file:
            line_numbers = line.strip().split("   ")
            left_numbers.append(int(line_numbers[0]))
            right_numbers.append(int(line_numbers[1]))

    left_numbers.sort()
    right_numbers.sort()

    total_difference = sum([
        abs(left - right) for left, right in zip(left_numbers, right_numbers)
    ])
    print(total_difference)
