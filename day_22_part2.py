import argparse
import collections

PRUNE_MODULO = 16777216


def mix(secret_number: int, number: int) -> int:
    return secret_number ^ number


def prune(number: int) -> int:
    return number % PRUNE_MODULO


def get_next_secret_number(secret_number: int) -> int:
    partial_secret = prune(mix(secret_number, 64 * secret_number))
    partial_secret = prune(mix(partial_secret, int(partial_secret / 32)))
    return prune(mix(partial_secret, 2048 * partial_secret))


def get_price(secret_number: int) -> int:
    return secret_number % 10


def get_bananas_per_change_code(secret_number: int, n: int) -> dict[str, int]:
    bananas = dict()
    change_queue = collections.deque()
    current_price = get_price(secret_number)
    for _ in range(n):
        secret_number = get_next_secret_number(secret_number)
        new_price = get_price(secret_number)
        price_change = new_price - current_price
        change_queue.append(str(price_change))
        if len(change_queue) == 5:
            change_queue.popleft()
        if len(change_queue) == 4:
            change_code = ",".join(change_queue)
            if change_code not in bananas:
                bananas[change_code] = new_price
        current_price = new_price

    return bananas


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    secret_numbers = [1, 2, 3, 2024]
    with open(args.filename, "r") as file:
        secret_numbers = [int(line.strip()) for line in file]

    bananas = dict()
    for secret_number in secret_numbers:
        secret_number_bananas = get_bananas_per_change_code(secret_number,
                                                            n=2000)
        for key, value in secret_number_bananas.items():
            if key not in bananas:
                bananas[key] = 0
            bananas[key] += value

    max_bananas = max(bananas.values())
    print(max_bananas)
