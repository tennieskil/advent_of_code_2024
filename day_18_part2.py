import argparse
import collections
import copy

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
GRID_SIZE = (71, 71)
KB = 1024


def is_valid_position(memory: list[list[bool]], pos: tuple[int, int]) -> bool:
    pos_0_valid = 0 <= pos[0] < len(memory)
    pos_1_valid = 0 <= pos[1] < len(memory[0])
    return pos_0_valid and pos_1_valid


def is_ok(memory: list[list[bool]], pos: tuple[int, int]) -> bool:
    return memory[pos[0]][pos[1]]


def exists_path(memory: list[list[bool]], start_pos: tuple[int, int]) -> bool:
    queue = collections.deque([start_pos])
    visited = {start_pos: 0}
    while queue:
        curr_pos = queue.popleft()
        for direction in DIRECTIONS:
            new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
            if not is_valid_position(memory, new_pos):
                continue
            if not is_ok(memory, new_pos):
                continue
            if new_pos in visited:
                continue
            queue.append(new_pos)
            visited[new_pos] = visited[curr_pos] + 1
    return (70, 70) in visited


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    falling_bytes = []
    with open(args.filename, "r") as file:
        falling_bytes = [
            tuple(map(int,
                      line.strip().split(","))) for line in file
        ]

    memory = [[True for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
    for byte_number in range(KB):
        byte = falling_bytes[byte_number]
        memory[byte[0]][byte[1]] = False

    low = KB
    high = len(falling_bytes) - 1
    mid = None
    while low < high:
        tmp_memory = copy.deepcopy(memory)
        mid = int((low + high) / 2) + 1
        for byte_number in range(KB, mid):
            byte = falling_bytes[byte_number]
            tmp_memory[byte[0]][byte[1]] = False
        if exists_path(tmp_memory, (0, 0)):
            low = mid
        else:
            high = mid - 1
    print(mid)
    print(falling_bytes[mid])
