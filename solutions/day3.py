import re
from pathlib import Path


def part1(path: Path) -> int:
    with Path(path).open("r") as file:
        content = file.read()

    pattern = r"mul\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)"
    matches = re.findall(pattern, content)
    mult_sum = sum([int(match[0]) * int(match[1]) for match in matches])
    return mult_sum


def part2(path: Path) -> int:
    with Path(path).open("r") as file:
        content = file.read()

    pattern = r"mul\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)|(do\(\)|don't\(\))"
    matches = re.findall(pattern, content)

    dont_str = "don't()"
    do_str = "do()"
    do = True
    mult_sum = 0

    for group in matches:
        if dont_str in group:
            do = False

        if do_str in group:
            do = True

        if do and group[0] != "" and group[1] != "":
            mult_sum += int(group[0]) * int(group[1])

    return mult_sum


if __name__ == "__main__":
    # day 3.1
    path = Path("inputs/day3.txt")
    print(f"day 3.1 solution: {part1(path)}")
    print(f"day 3.2 solution: {part2(path)}")
