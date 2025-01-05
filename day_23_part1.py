import argparse


def maybe_initialize_computer(connections: dict[str, set[str]],
                              computer: str) -> None:
    if not computer in connections:
        connections[computer] = set()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    connections: dict[str, set[str]] = {}
    with open(args.filename, "r") as file:
        for line in file:
            computer1, computer2 = line.strip().split("-")
            maybe_initialize_computer(connections, computer1)
            maybe_initialize_computer(connections, computer2)
            connections[computer1].add(computer2)
            connections[computer2].add(computer1)

    t_triplets = set()
    for computer1 in connections:
        for computer2 in connections[computer1]:
            if computer1 > computer2:
                continue  # only count triplets in lexographical order
            for computer3 in connections[computer1].intersection(
                    connections[computer2]):
                if computer2 > computer3:
                    continue
                if computer1.startswith("t") or computer2.startswith(
                        "t") or computer3.startswith("t"):
                    t_triplets.add((computer1, computer2, computer3))

    print(len(t_triplets))
