import argparse


def count_stones(stone: int, blinks: int, stone_cache: dict[tuple[int, int],
                                                            int]) -> int:
    if blinks == 0:
        return 1
    if (stone, blinks) in stone_cache:
        return stone_cache[(stone, blinks)]
    if stone == 0:
        result = count_stones(1, blinks - 1, stone_cache)
        stone_cache[(stone, blinks)] = result
        return result
    if len(str(stone)) % 2 == 0:
        stone1 = int(str(stone)[:int(len(str(stone)) / 2)])
        stone2 = int(str(stone)[int(len(str(stone)) / 2):])
        result = count_stones(stone1, blinks - 1, stone_cache) + count_stones(
            stone2, blinks - 1, stone_cache)
        stone_cache[(stone, blinks)] = result
        return result
    result = count_stones(stone * 2024, blinks - 1, stone_cache)
    stone_cache[(stone, blinks)] = result
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    unparsed_stones = []
    with open(args.filename, "r") as file:
        unparsed_stones = [line.strip() for line in file][0]

    stones = [int(stone) for stone in unparsed_stones.split()]
    stone_cache = {}
    n_stones = sum([count_stones(stone, 75, stone_cache) for stone in stones])
    print(n_stones)
