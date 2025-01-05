import argparse


def get_n_possible_designs(towels: list[str], design: str) -> int:
    partial_design_lens = (len(design) + 1) * [0]
    partial_design_lens[0] = 1
    for i in range(len(design) + 1):
        if not partial_design_lens[i]:
            continue
        for towel in towels:
            if len(towel) + i > len(design):
                continue
            if towel != design[i:i + len(towel)]:
                continue
            partial_design_lens[i + len(towel)] += partial_design_lens[i]
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
        [get_n_possible_designs(towels, design) for design in designs])
    print(possible_count)
