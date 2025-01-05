import argparse


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
                antinode_1 = (2 * i - x, 2 * j - y)
                antinode_2 = (-i + 2 * x, -j + 2 * y)
                if is_valid_position(city_map, antinode_1):
                    antinodes.add(antinode_1)
                if is_valid_position(city_map, antinode_2):
                    antinodes.add(antinode_2)
            antennas[frequency].append((i, j))

    print(len(antinodes))
