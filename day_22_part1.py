import argparse

PRUNE_MODULO = 16777216


def mix(secret_number: int, number: int) -> int:
    return secret_number ^ number


def prune(number: int) -> int:
    return number % PRUNE_MODULO


def get_next_secret_number(secret_number: int) -> int:
    partial_secret = prune(mix(secret_number, 64 * secret_number))
    partial_secret = prune(mix(partial_secret, int(partial_secret / 32)))
    return prune(mix(partial_secret, 2048 * partial_secret))


def get_nth_secret_number(secret_number: int, n: int) -> int:
    for _ in range(n):
        secret_number = get_next_secret_number(secret_number)
    return secret_number


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    secret_numbers = [1, 10, 100, 2024]
    with open(args.filename, "r") as file:
        secret_numbers = [int(line.strip()) for line in file]

    new_numbers = [get_nth_secret_number(n, 2000) for n in secret_numbers]
    print(sum(new_numbers))
