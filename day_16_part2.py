import argparse
import collections
import dataclasses
import heapq

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def is_horizontal(dirction: tuple[int, int]) -> bool:
    return dirction[0] == 0


@dataclasses.dataclass
class Node:
    loc: tuple[int, int]
    horizontal: bool
    score: int = -1

    def __hash__(self):
        return self.loc.__hash__()

    def __eq__(self, other) -> bool:
        return self.loc == other.loc and self.horizontal == other.horizontal

    def __lt__(self, other) -> bool:
        return self.score < other.score


@dataclasses.dataclass(frozen=True)
class Edge:
    to: Node
    cost: int


def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return tuple(p1 + p2 for p1, p2 in zip(t1, t2))


def get_value(race_track: list[str], pos: tuple[int, int]) -> str:
    return race_track[pos[0]][pos[1]]


def get_node(loc_nodes: tuple[Node, Node], horizontal: bool) -> Node:
    if horizontal:
        return loc_nodes[0]
    return loc_nodes[1]


def build_nodes(race_track: list[str]):
    nodes = {}
    for i in range(len(race_track)):
        for j in range(len(race_track[0])):
            if race_track[i][j] == "#":
                continue
            horizontal_node = Node((i, j), True)
            vertical_node = Node((i, j), False)
            nodes[(i, j)] = (horizontal_node, vertical_node)
    return nodes


def build_graph(race_track: list[str], nodes) -> dict[Node, list[Edge]]:
    graph = {}
    for i in range(len(race_track)):
        for j in range(len(race_track[0])):
            if not (i, j) in nodes:
                continue
            loc_nodes = nodes[(i, j)]
            graph[loc_nodes[0]] = [Edge(loc_nodes[1], 1000)]
            graph[loc_nodes[1]] = [Edge(loc_nodes[0], 1000)]
    for i in range(len(race_track)):
        for j in range(len(race_track[0])):
            if not (i, j) in nodes:
                continue
            for direction in DIRECTIONS:
                neighbor_loc = add((i, j), direction)
                if not neighbor_loc in nodes:
                    continue
                a = get_node(nodes[(i, j)], is_horizontal(direction))
                b = get_node(nodes[neighbor_loc], is_horizontal(direction))
                graph[a].append(Edge(b, 1))
                graph[b].append(Edge(a, 1))

    return graph


def get_n_best_locs(race_track: list[str], start_loc: tuple[int, int],
                    end_loc: tuple[int, int]) -> int:
    nodes = build_nodes(race_track)
    graph = build_graph(race_track, nodes)
    start_node = get_node(nodes[start_loc], horizontal=True)
    start_node.score = 0
    queue = [start_node]
    best_path_to = {start_node: {}}
    while queue:
        curr_node = heapq.heappop(queue)
        for edge in graph[curr_node]:
            new_score = curr_node.score + edge.cost
            if edge.to.score == -1 or edge.to.score > new_score:
                edge.to.score = new_score
                heapq.heappush(queue, edge.to)
                best_path_to[edge.to] = {curr_node}
            elif edge.to.score == new_score:
                best_path_to[edge.to].add(curr_node)

    min_score = min([node.score for node in nodes[end_loc]])
    path_nodes = [node for node in nodes[end_loc] if node.score == min_score]

    queue = collections.deque(path_nodes)
    visited = set([end_loc])
    while queue:
        curr_node = queue.popleft()
        for node in best_path_to[curr_node]:
            queue.append(node)
            visited.add(node.loc)

    return len(visited)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    race_track = []
    with open(args.filename, "r") as file:
        race_track = [line.strip() for line in file]

    start_loc = None
    end_loc = None
    for i in range(len(race_track)):
        for j in range(len(race_track[0])):
            if get_value(race_track, (i, j)) == 'S':
                start_loc = (i, j)
            elif get_value(race_track, (i, j)) == 'E':
                end_loc = (i, j)

    n_locs = get_n_best_locs(race_track, start_loc, end_loc)
    print(n_locs)
