import argparse
import math


def is_valid_position(city_map: list[str], pos: tuple[int, int]) -> bool:
    pos_0_valid = 0 <= pos[0] < len(city_map)
    pos_1_valid = 0 <= pos[1] < len(city_map[0])
    return pos_0_valid and pos_1_valid


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    city_map = []
    with open(args.filename, "r") as file:
        city_map = [line.strip() for line in file]

    antennas = {}
    antinodes = set()
    for i in range(len(city_map)):
        for j in range(len(city_map[0])):
            if city_map[i][j] == '.':
                continue
            frequency = city_map[i][j]
            if frequency not in antennas:
                antennas[frequency] = []
            for x, y in antennas[frequency]:
                x_step = x - i / math.gcd(abs(x - i), abs(y - j))
                y_step = y - j / math.gcd(abs(x - i), abs(y - j))
                x_pos, y_pos = x, y
                while is_valid_position(city_map,
                                        (x_pos + x_step, y_pos + y_step)):
                    x_pos, y_pos = x_pos + x_step, y_pos + y_step
                while is_valid_position(city_map, (x_pos, y_pos)):
                    antinodes.add((x_pos, y_pos))
                    x_pos, y_pos = x_pos - x_step, y_pos - y_step
            antennas[frequency].append((i, j))

    print(len(antinodes))
