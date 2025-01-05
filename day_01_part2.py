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

    right_occurrances = {}
    for right in right_numbers:
        if not right in right_occurrances:
            right_occurrances[right] = 0
        right_occurrances[right] += 1

    similarity_score = sum(
        [left * right_occurrances.get(left, 0) for left in left_numbers])
    print(similarity_score)
