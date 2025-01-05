import argparse
import collections

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
CHEATS = [(i, j) for i in range(-20, 21) for j in range(-20, 21)
          if abs(i) + abs(j) <= 20]


def is_valid_position(race_track: list[str], pos: tuple[int, int]) -> bool:
    pos_0_valid = 0 <= pos[0] < len(race_track)
    pos_1_valid = 0 <= pos[1] < len(race_track[0])
    return pos_0_valid and pos_1_valid


def get_value(race_track: list[str], pos: tuple[int, int]) -> str:
    return race_track[pos[0]][pos[1]]


def get_cheats(race_track: list[str], start_pos: tuple[int,
                                                       int]) -> dict[int, int]:
    queue = collections.deque([start_pos])
    visited = {start_pos: 0}
    while queue:
        curr_pos = queue.popleft()
        for direction in DIRECTIONS:
            new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
            if get_value(race_track, new_pos) not in ('E', '.'):
                continue
            if new_pos in visited:
                continue
            queue.append(new_pos)
            visited[new_pos] = visited[curr_pos] + 1

    cheats = {}
    for curr_pos in visited.keys():
        for cheat in CHEATS:
            new_pos = (curr_pos[0] + cheat[0], curr_pos[1] + cheat[1])
            cheat_time = abs(cheat[0]) + abs(cheat[1])
            if not is_valid_position(race_track, new_pos):
                continue
            if get_value(race_track, new_pos) not in ('E', '.'):
                continue
            saves_picos = visited[new_pos] - visited[curr_pos] - cheat_time
            if saves_picos <= 0:
                continue
            if not saves_picos in cheats:
                cheats[saves_picos] = 0
            cheats[saves_picos] += 1
    return cheats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    race_track = []
    with open(args.filename, "r") as file:
        race_track = [line.strip() for line in file]

    start_pos = None
    for i in range(len(race_track)):
        for j in range(len(race_track[0])):
            if get_value(race_track, (i, j)) == 'S':
                start_pos = (i, j)
                break

    cheats = get_cheats(race_track, start_pos)
    n_big_cheats = sum(
        [count for picos, count in cheats.items() if picos >= 100])
    print(n_big_cheats)
