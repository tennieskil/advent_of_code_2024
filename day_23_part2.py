import argparse
import dataclasses


@dataclasses.dataclass(frozen=True)
class Clique:
    computers: set[str]

    def __hash__(self) -> int:
        return self.get_password().__hash__()

    def __eq__(self, other) -> bool:
        return self.computers == other.computers

    def get_password(self) -> str:
        computers_list = list(self.computers)
        computers_list.sort()
        return ",".join(computers_list)


def maybe_initialize_computer(connections: dict[str, set[str]],
                              computer: str) -> None:
    if not computer in connections:
        connections[computer] = set()


def get_any_set_element(items: set):
    for item in items:
        return item
    raise ValueError


def find_largest_clique(connections: dict[str, set[str]],
                        cliques: set[Clique]) -> Clique:
    if len(cliques) == 1:
        return get_any_set_element(cliques)
    larger_cliques = set()
    for clique in cliques:
        computer = get_any_set_element(clique.computers)
        for neighbor in connections[computer]:
            if all([neighbor in connections[c] for c in clique.computers]):
                larger_cliques.add(
                    Clique(clique.computers.union(set([neighbor]))))
    return find_largest_clique(connections, larger_cliques)


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

    triplets = set()
    for computer1 in connections:
        for computer2 in connections[computer1]:
            if computer1 > computer2:
                continue
            for computer3 in connections[computer1].intersection(
                    connections[computer2]):
                if computer2 > computer3:
                    continue
                triplets.add(Clique({computer1, computer2, computer3}))

    larget_clique = find_largest_clique(connections, triplets)
    print(larget_clique.get_password())
