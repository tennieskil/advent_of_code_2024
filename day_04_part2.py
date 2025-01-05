import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    lines = []
    with open(args.filename, "r") as file:
        lines = [line.strip() for line in file]

    xmas_count = 0
    for i in range(1, len(lines) - 1):
        for j in range(1, len(lines[0]) - 1):
            if lines[i][j] != 'A':
                continue
            if {lines[i + 1][j + 1], lines[i - 1][j - 1]} == {'M', 'S'} and {
                    lines[i + 1][j - 1], lines[i - 1][j + 1]
            } == {'M', 'S'}:
                xmas_count += 1

    print(xmas_count)
