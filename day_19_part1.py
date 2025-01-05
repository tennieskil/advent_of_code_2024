import argparse


def is_design_possible(towels: list[str], design: str) -> bool:
    partial_design_lens = (len(design) + 1) * [False]
    partial_design_lens[0] = True
    for i in range(len(design) + 1):
        if not partial_design_lens[i]:
            continue
        for towel in towels:
            if len(towel) + i > len(design):
                continue
            if partial_design_lens[i + len(towel)]:
                continue
            if towel != design[i:i + len(towel)]:
                continue
            partial_design_lens[i + len(towel)] = True
    return partial_design_lens[len(design)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    towels = []
    designs = []
    with open(args.filename, "r") as file:
        for i, line in enumerate(file):
            if i == 0:
                towels = line.strip().split(", ")
                continue
            if not line.strip():
                continue
            designs.append(line.strip())

    possible_count = sum(
        [is_design_possible(towels, design) for design in designs])
    print(possible_count)
