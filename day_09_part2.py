import argparse
import dataclasses


@dataclasses.dataclass
class File:
    memory_location: int
    value: int
    size: int


@dataclasses.dataclass
class Gap:
    memory_location: int
    size: int


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    contents = None
    with open(args.filename, "r") as file:
        contents = [line.strip() for line in file][0]

    memory = {}
    files = []
    gaps = []
    value_locations = []
    memory_location = 0
    for i in range(len(contents)):
        is_file = i % 2 == 0
        content_size = int(contents[i])
        if is_file:
            files.append(File(memory_location, int(i / 2), content_size))
        else:
            gaps.append(Gap(memory_location, content_size))
        memory_location += content_size

    file_index_to_move = len(files) - 1
    while file_index_to_move >= 0:
        file = files[file_index_to_move]
        for gap in gaps:
            if gap.memory_location >= file.memory_location:
                break
            if gap.size >= file.size:
                file.memory_location = gap.memory_location
                gap.memory_location += file.size
                gap.size -= file.size
                break
        file_index_to_move -= 1

    checksum = 0
    for file in files:
        for i in range(file.size):
            memory_location = file.memory_location + i
            checksum += memory_location * file.value
    print(checksum)
