from pathlib import Path

import numpy as np


def part1(path: Path, target: str) -> int:
    contents = np.array(
        [list(line.strip()) for line in list(path.read_text().splitlines())]
    )
    pad = len(target) - 1
    contents = np.pad(contents, pad, mode="constant", constant_values="-")
    window_length = 2 * (len(target)) - 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    target_matches = 0
    for row_idx in range(contents.shape[0]):
        for column_idx in range(contents.shape[1]):
            # find all possible starting locations of the target string
            if contents[row_idx][column_idx] == target[0]:
                # get the window for the possible target string
                columns = np.arange(
                    column_idx - len(target) + 1, column_idx + len(target)
                )
                column_indices = (
                    np.repeat(columns, window_length)
                    .reshape((window_length, window_length))
                    .T
                )
                rows = np.arange(row_idx - len(target) + 1, row_idx + len(target))
                row_indices = (
                    np.tile(rows, window_length)
                    .reshape((window_length, window_length))
                    .T
                )
                window = contents[row_indices, column_indices]

                # determine the number of times the target string occurs in the window
                center = len(window) // 2
                for row_direction, column_direction in directions:
                    char_matches = 0
                    for i in range(len(target)):
                        r, c = center + row_direction * i, center + column_direction * i
                        if window[r, c] != target[i]:
                            break
                        else:
                            char_matches += 1

                    if char_matches == len(target):
                        target_matches += 1

    return target_matches


def part2(path: Path, target: str) -> int:
    contents = np.array(
        [list(line.strip()) for line in list(path.read_text().splitlines())]
    )
    rev_target = target[::-1]
    x_mas_matches = 0
    for row_index in range(1, contents.shape[0] - 1):
        for column_index in range(1, contents.shape[1] - 1):
            if contents[row_index, column_index] == target[len(target) // 2]:
                # get the window indices for the possible target string
                idx_past_center = len(target[: len(target) // 2])
                column_indices = np.arange(
                    column_index - idx_past_center, column_index + idx_past_center + 1
                )
                row_indices = np.arange(
                    row_index - idx_past_center, row_index + idx_past_center + 1
                )

                diag1 = "".join(contents[row_indices, column_indices])
                diag2 = "".join(contents[row_indices[::-1], column_indices])
                if (diag1 == target or diag1 == rev_target) and (
                    diag2 == target or diag2 == rev_target
                ):
                    x_mas_matches += 1
    return x_mas_matches


if __name__ == "__main__":
    path = Path("inputs/day4.txt")
    part1_target = "XMAS"
    part2_target = "MAS"
    print(f"day 4.1 solution: {part1(path, part1_target)}")
    print(f"day 4.2 solution: {part2(path, part2_target)}")
