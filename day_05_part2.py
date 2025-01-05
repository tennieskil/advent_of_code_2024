import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    lines = []
    with open(args.filename, "r") as file:
        lines = [line.strip() for line in file]

    rules = {}
    line_index = 0
    while lines[line_index]:
        pages = [int(n) for n in lines[line_index].split("|")]
        assert len(pages) == 2
        if not pages[0] in rules:
            rules[pages[0]] = set()
        rules[pages[0]].add(pages[1])
        line_index += 1

    line_index += 1
    page_sum = 0
    while line_index < len(lines):
        pages = [int(n) for n in lines[line_index].split(",")]
        valid_combination = True
        for i in range(len(pages)):
            earlier_page = pages[i]
            for j in range(i + 1, len(pages)):
                later_page = pages[j]
                if earlier_page in rules[later_page]:
                    valid_combination = False
        line_index += 1
        if valid_combination:
            continue
        reordered_pages = []
        used_pages = set()
        while len(reordered_pages) < len(pages):
            for page in pages:
                if page in used_pages: continue
                is_next_page = True
                for later_page in pages:
                    if later_page == page or later_page in used_pages:
                        continue
                    if later_page not in rules[page]:
                        is_next_page = False
                        break
                if is_next_page:
                    reordered_pages.append(page)
                    used_pages.add(page)
                    break
        page_sum += reordered_pages[int(len(pages) / 2)]

    print(page_sum)
