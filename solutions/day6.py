from pathlib import Path

import numpy as np


def part1(path: Path):
    contents = np.array([list(line.strip()) for line in list(path.read_text().splitlines())])
    row_idx, column_idx = np.where(contents == "^")
    obstruction = "#"
    seen_char = "X"

    while row_idx >= 0:
        contents[row_idx, column_idx] = seen_char
        next_char = contents[row_idx - 1, column_idx]
        if next_char == obstruction:
            new_row_idx = contents.shape[1] - 1 - column_idx
            new_column_idx = row_idx
            row_idx = new_row_idx
            column_idx = new_column_idx
            contents = np.rot90(contents)
        else:
            row_idx -= 1

    print(f"day 6.1 solution: {np.sum(contents == seen_char)}")


if __name__ == "__main__":
    path = Path("inputs/day6.txt")
    part1(path)
