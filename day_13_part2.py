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
    return (10000000000000 + x, 10000000000000 + y)


def solve(machine: Machine) -> int:
    """ Solves the machine.

    Solves the machine minimizing the number of tokens payed.

    Equation system:
    
    * prize.x = press_a * a.x + press_b * b.x
    * prize.y = press_a * a.y + press_b * b.y

    leads to

    * press_a = (prize.x - press_b * b.x) / a.x

    inserting into the second equation yields

    * prize.y = (prize.x - press_b * b.x) / a.x * a.y + press_b * b.y
    ->
    * a.x * prize.y = (prize.x - press_b * b.x) * a.y + a.x * press_b * b.y
    ->
    press_b * (a.x * b.y - b.x * a.y) = a.x * prize.y - a.y * prize.x

    Returns:
      (int) the number of tokens required to solve the machine, or 0 if the machine
      cannot be solved.
    """
    denominator = machine.a.x * machine.b.y - machine.b.x * machine.a.y
    if denominator == 0:
        assert False

    nominator = (machine.a.x * machine.prize[1] -
                 machine.a.y * machine.prize[0])
    press_b = nominator / denominator
    press_a = (machine.prize[0] - press_b * machine.b.x) / machine.a.x
    if press_a != int(press_a) or press_b != int(press_b):
        return 0
    return press_a * machine.a.cost + press_b * machine.b.cost


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
