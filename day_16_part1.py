import argparse
import heapq
import dataclasses

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclasses.dataclass(frozen=True)
class RaceTrackEntry:
    location: tuple[int, int]
    score: int
    incoming_direction: tuple[int, int]

    def __lt__(self, other) -> bool:
        return self.score < other.score

    def __eq__(self, other) -> bool:
        return self.score == other.score


def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return tuple(p1 + p2 for p1, p2 in zip(t1, t2))


def get_value(race_track: list[str], pos: tuple[int, int]) -> str:
    return race_track[pos[0]][pos[1]]


def get_lowest_score(race_track: list[str], start_loc: tuple[int, int],
                     end_loc: tuple[int, int]) -> int:
    start_entry = RaceTrackEntry(start_loc, 0, (0, 1))
    queue = [start_entry]
    best_scores = {start_loc: 0}
    while queue:
        curr_entry = heapq.heappop(queue)
        for direction in DIRECTIONS:
            new_loc = add(curr_entry.location, direction)
            if get_value(race_track, new_loc) == "#":
                continue
            new_score = curr_entry.score + 1
            if direction != curr_entry.incoming_direction:
                new_score += 1000
            if new_loc not in best_scores:
                best_scores[new_loc] = new_score
            else:
                if new_score + 1000 > best_scores[new_loc]:
                    continue
                if new_score < best_scores[new_loc]:
                    best_scores[new_loc] = new_score
            heapq.heappush(queue, RaceTrackEntry(new_loc, new_score,
                                                 direction))
    return best_scores[end_loc]


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

    score = get_lowest_score(race_track, start_loc, end_loc)
    print(score)
