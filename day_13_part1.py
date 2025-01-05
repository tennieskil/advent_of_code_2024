import argparse
import dataclasses

BUTTON_COSTS = {
    "A": 3,
    "B": 1,
}


@dataclasses.dataclass(frozen=True)
class Button:
    cost: int
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Machine:
    a: Button
    b: Button
    prize: tuple[int, int]


def parse_button(line: str, name: str) -> Button:
    line = line.strip()
    expected_line_prefix = f"Button {name}:"
    assert line.startswith(expected_line_prefix)
    x_part, y_part = [
        part.strip() for part in line[len(expected_line_prefix):].split(", ")
    ]
    x_prefix = "X+"
    y_prefix = "Y+"
    assert x_part.startswith(x_prefix)
    assert y_part.startswith(y_prefix)
    x = int(x_part[len(x_prefix):])
    y = int(y_part[len(y_prefix):])
    return Button(BUTTON_COSTS[name], x, y)


def parse_prize(line: str) -> tuple[int, int]:
    line = line.strip()
    expected_line_prefix = "Prize:"
    assert line.startswith(expected_line_prefix)
    x_part, y_part = [
        part.strip() for part in line[len(expected_line_prefix):].split(", ")
    ]
    x_prefix = "X="
    y_prefix = "Y="
    assert x_part.startswith(x_prefix)
    assert y_part.startswith(y_prefix)
    x = int(x_part[len(x_prefix):])
    y = int(y_part[len(y_prefix):])
    return (x, y)


def solve(machine: Machine) -> int:
    """ Solves the machine.

    Solves the machine minimizing the number of tokens payed. The requirements
    are:
      - Each button is pressed at most 100 times

    Returns:
      (int) the number of tokens required to solve the machine, or 0 if the machine
      cannot be solved.
    """
    min_cost = -1
    for press_a in range(101):
        for press_b in range(101):
            x = press_a * machine.a.x + press_b * machine.b.x
            y = press_a * machine.a.y + press_b * machine.b.y
            if (x, y) == (machine.prize):
                cost = press_a * machine.a.cost + press_b * machine.b.cost
                if min_cost == -1 or cost < min_cost:
                    min_cost = cost
    return max(0, min_cost)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    machines = []
    with open(args.filename, "r") as file:
        button_a = None
        button_b = None
        prize = None
        for line in file:
            if not line.strip():
                assert button_a
                assert button_b
                assert prize
                machines.append(Machine(button_a, button_b, prize))
                button_a, button_b, prize = None, None, None
            elif button_a is None:
                button_a = parse_button(line, "A")
            elif button_b is None:
                button_b = parse_button(line, "B")
            else:
                prize = parse_prize(line)
    assert not button_a
    assert not button_b
    assert not prize

    total_cost = sum([solve(machine) for machine in machines])
    print(total_cost)
