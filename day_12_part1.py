import argparse
import collections

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def get_plant_type(garden: list[str], pos: tuple[int, int]) -> str:
    return garden[pos[0]][pos[1]]


def is_valid_position(garden: list[str], pos: tuple[int, int]) -> bool:
    pos_0_valid = 0 <= pos[0] < len(garden)
    pos_1_valid = 0 <= pos[1] < len(garden[0])
    return pos_0_valid and pos_1_valid


def get_region(garden: list[str],
               start_pos: tuple[int, int]) -> set[tuple[int, int]]:
    region_plant_type = get_plant_type(garden, start_pos)
    queue = collections.deque([start_pos])
    region = set([start_pos])
    while queue:
        curr_pos = queue.popleft()
        for direction in DIRECTIONS:
            new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
            if not is_valid_position(garden, new_pos):
                continue
            if new_pos in region:
                continue
            if get_plant_type(garden, new_pos) != region_plant_type:
                continue
            queue.append(new_pos)
            region.add(new_pos)
    return region


def get_region_cost(region: set[tuple[int, int]]) -> int:
    perimiter = 0
    for pos in region:
        for direction in DIRECTIONS:
            neighbor_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if neighbor_pos not in region:
                perimiter += 1
    return perimiter * len(region)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    garden = []
    with open(args.filename, "r") as file:
        garden = [line.strip() for line in file]

    total_cost = 0
    visited = set()
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if (i, j) in visited:
                continue
            region = get_region(garden, (i, j))
            visited = visited.union(region)
            region_cost = get_region_cost(region)
            total_cost += region_cost

    print(total_cost)
