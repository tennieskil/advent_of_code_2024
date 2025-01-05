import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    contents = None
    with open(args.filename, "r") as file:
        contents = [line.strip() for line in file][0]

    memory = {}
    value_locations = []
    memory_location = 0
    for i in range(len(contents)):
        is_file = i % 2 == 0
        content_value = int(contents[i])
        for j in range(content_value):
            if is_file:
                memory[memory_location] = int(i / 2)
                value_locations.append(memory_location)
            memory_location += 1

    memory_location = 0
    reverse_location_index = len(value_locations) - 1
    checksum = 0
    while memory_location <= value_locations[reverse_location_index]:
        if memory_location in memory:
            checksum += memory_location * memory[memory_location]
        else:
            checksum += memory_location * memory[
                value_locations[reverse_location_index]]
            reverse_location_index -= 1
        memory_location += 1

    print(checksum)
