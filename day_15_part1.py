import argparse

DIRECTIONS = {
    "<": (0, -1),
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
}

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
            room[(i, j)] = initial_room[i][j]
            if initial_room[i][j] == "@":
                robot_loc = (i, j)

    for move in moves:
        direction = DIRECTIONS[move]
        loc = (robot_loc[0] + direction[0], robot_loc[1] + direction[1])
        boxes = []
        while room[loc] == "O":
            boxes.append(loc)
            loc = (loc[0] + direction[0], loc[1] + direction[1])

        if room[loc] == ".":
            room[loc] = "O"
            room[robot_loc] = "."
            robot_loc = (robot_loc[0] + direction[0],
                         robot_loc[1] + direction[1])
            room[robot_loc] = "@"

    gps_sum = 0
    for i in range(len(initial_room)):
        for j in range(len(initial_room[0])):
            if room[(i, j)] == "O":
                gps_sum += 100 * i + j
    print(gps_sum)
