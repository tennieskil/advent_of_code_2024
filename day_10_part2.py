import argparse
import collections

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def get_value(hiking_map: list[str], pos: tuple[int, int]) -> int:
    return int(hiking_map[pos[0]][pos[1]])


def is_valid_position(hiking_map: list[str], pos: tuple[int, int]) -> bool:
    pos_0_valid = 0 <= pos[0] < len(hiking_map)
    pos_1_valid = 0 <= pos[1] < len(hiking_map[0])
    return pos_0_valid and pos_1_valid


def get_trailhead_rating(hiking_map: list[str], trailhead: tuple[int,
                                                                 int]) -> int:
    dp = {trailhead: 1}
    queue = collections.deque([trailhead])
    while queue:
        loc = queue.popleft()
        loc_value = get_value(hiking_map, loc)
        for direction in DIRECTIONS:
            new_loc = (loc[0] + direction[0], loc[1] + direction[1])
            if not is_valid_position(hiking_map, new_loc):
                continue
            new_loc_value = get_value(hiking_map, new_loc)
            if loc_value + 1 == new_loc_value:
                if not new_loc in dp:
                    dp[new_loc] = 0
                    queue.append(new_loc)
                dp[new_loc] += dp[loc]

    trailhead_rating = 0
    for loc, count in dp.items():
        if get_value(hiking_map, loc) == 9:
            trailhead_rating += count
    return trailhead_rating


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    hiking_map = []
    with open(args.filename, "r") as file:
        hiking_map = [line.strip() for line in file]

    total_rating = 0
    for i in range(len(hiking_map)):
        for j in range(len(hiking_map[0])):
            if int(hiking_map[i][j]) != 0:
                continue
            total_rating += get_trailhead_rating(hiking_map, (i, j))

    print(total_rating)
