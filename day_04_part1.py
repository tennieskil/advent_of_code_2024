import argparse
import re


def reverse(string: str) -> str:
    return string[::-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    lines = []
    with open(args.filename, "r") as file:
        lines = [line.strip() for line in file]

    xmas_regex = r"XMAS"
    xmas_count = 0

    # horizontal
    for line in lines:
        xmas_count += len(re.findall(xmas_regex, line))
        xmas_count += len(re.findall(xmas_regex, reverse(line)))

    # vertical
    for i in range(len(lines[0])):
        line = "".join(lines[j][i] for j in range(len(lines)))
        xmas_count += len(re.findall(xmas_regex, line))
        xmas_count += len(re.findall(xmas_regex, reverse(line)))

    # diagonal (top-left to bottom-right)
    start_locations = [(i, 0) for i in range(len(lines))]
    start_locations.extend([(0, j) for j in range(1, len(lines[0]))])
    for i, j in start_locations:
        line = "".join(lines[i + k][j + k] for k in range(len(lines))
                       if i + k < len(lines) and j + k < len(lines[0]))
        xmas_count += len(re.findall(xmas_regex, line))
        xmas_count += len(re.findall(xmas_regex, reverse(line)))

    # diagonal (top-right to bottom-left)
    start_locations = [(i, len(lines[0]) - 1) for i in range(len(lines))]
    start_locations.extend([(0, j) for j in range(len(lines[0]) - 1)])
    for i, j in start_locations:
        line = "".join(lines[i + k][j - k] for k in range(len(lines))
                       if i + k < len(lines) and j - k >= 0)
        xmas_count += len(re.findall(xmas_regex, line))
        xmas_count += len(re.findall(xmas_regex, reverse(line)))

    print(xmas_count)
