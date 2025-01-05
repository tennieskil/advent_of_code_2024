import argparse

DIRECTION_CHANGES = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def change_direction(direction: tuple[int, int]) -> tuple[int, int]:
    return DIRECTION_CHANGES[direction]


def is_valid_position(room: list[str], pos: tuple[int, int]) -> bool:
    pos_0_valid = 0 <= pos[0] < len(room)
    pos_1_valid = 0 <= pos[1] < len(room[0])
    return pos_0_valid and pos_1_valid


def is_loop(room, pos, direction, obstacle_pos) -> bool:
    visited = {pos + direction}
    while True:
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if not is_valid_position(room, next_pos):
            break
        if room[next_pos[0]][next_pos[1]] == '#' or next_pos == obstacle_pos:
            direction = change_direction(direction)
            continue
        if next_pos + direction in visited:
            return True
        visited.add(next_pos + direction)
        pos = next_pos
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    room = []
    with open(args.filename, "r") as file:
        room = [line.strip() for line in file]

    starting_position = None
    for i in range(len(room)):
        for j in range(len(room[0])):
            if room[i][j] == "^":
                starting_position = (i, j)
                break

    pos = starting_position
    direction = (-1, 0)
    n_loops = 0
    visited = {pos}
    while True:  # expecting a break
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if not is_valid_position(room, next_pos):
            break
        if room[next_pos[0]][next_pos[1]] == '#':
            direction = change_direction(direction)
            continue
        if next_pos != starting_position and next_pos not in visited:
            if is_loop(room, pos, direction, obstacle_pos=next_pos):
                n_loops += 1
        pos = next_pos
        visited.add(pos)

    print(n_loops)
