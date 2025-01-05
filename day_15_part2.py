import argparse

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRECTIONS = {
    "<": LEFT,
    "^": UP,
    ">": RIGHT,
    "v": DOWN,
}


def add(pos1: tuple[int, int], pos2: tuple[int, int]) -> tuple[int, int]:
    return tuple(p1 + p2 for p1, p2 in zip(pos1, pos2))


def get_vertically_movable_box_locs(
    room: dict[tuple[int, int],
               str], locs: list[tuple[int, int]], direction: tuple[int, int],
    movable_box_locs: dict[tuple[int, int],
                           str]) -> dict[tuple[int, int], str]:
    if not locs:
        return movable_box_locs

    new_locs = []
    for loc in locs:
        new_loc = add(loc, direction)
        if room[new_loc] == "#":
            return {}
        if room[new_loc] == "[":
            movable_box_locs[new_loc] = "["
            movable_box_locs[add(new_loc, RIGHT)] = "]"
            new_locs.append(new_loc)
            new_locs.append(add(new_loc, RIGHT))
        if room[new_loc] == "]":
            movable_box_locs[new_loc] = "]"
            movable_box_locs[add(new_loc, LEFT)] = "["
            new_locs.append(new_loc)
            new_locs.append(add(new_loc, LEFT))

    return get_vertically_movable_box_locs(room, new_locs, direction,
                                           movable_box_locs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    initial_room = []
    move_list = []
    with open(args.filename, "r") as file:
        is_room = True
        for line in file:
            if not line.strip():
                is_room = False
            elif is_room:
                initial_room.append(line.strip())
            else:
                move_list.append(line.strip())

    moves = "".join(move_list)
    room = {}
    robot_loc = None
    for i in range(len(initial_room)):
        for j in range(len(initial_room[0])):
            if initial_room[i][j] in (".", "#"):
                room[(i, 2 * j)] = initial_room[i][j]
                room[(i, 2 * j + 1)] = initial_room[i][j]
            if initial_room[i][j] == "@":
                robot_loc = (i, 2 * j)
                room[(i, 2 * j)] = "@"
                room[(i, 2 * j + 1)] = "."
            if initial_room[i][j] == "O":
                room[(i, 2 * j)] = "["
                room[(i, 2 * j + 1)] = "]"

    for move in moves:
        direction = DIRECTIONS[move]
        loc = add(robot_loc, direction)
        if room[loc] == "#":
            continue
        if room[loc] == ".":
            room[robot_loc] = "."
            robot_loc = loc
            room[robot_loc] = "@"
            continue

        movable_box_locs = {}
        if direction in (UP, DOWN):
            locs = [loc, add(loc, LEFT)]
            if room[loc] == "[":
                locs = [loc, add(loc, RIGHT)]
            movable_box_locs = get_vertically_movable_box_locs(
                room, locs, direction, {l: room[l]
                                        for l in locs})
        else:
            while room[loc] in ("[", "]"):
                movable_box_locs[loc] = room[loc]
                loc = add(loc, direction)
            if room[loc] != ".":
                movable_box_locs = {}

        if not movable_box_locs:
            continue
        for loc in movable_box_locs:
            room[loc] = "."
        for loc in movable_box_locs:
            new_loc = add(loc, direction)
            room[new_loc] = movable_box_locs[loc]

        room[robot_loc] = "."
        robot_loc = add(robot_loc, direction)
        room[robot_loc] = "@"

    gps_sum = 0
    for i in range(len(initial_room)):
        # print()
        for j in range(len(2 * initial_room[0])):
            if room[(i, j)] == "[":
                gps_sum += 100 * i + j
            # print(room[(i, j)], end="")
    print(gps_sum)
