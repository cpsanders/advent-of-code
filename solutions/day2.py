from pathlib import Path

import numpy as np
import polars as pl
from numpy.typing import NDArray

if __name__ == "__main__":
    # day 2.1
    path = Path("inputs/day2.txt")
    lines = path.read_text().splitlines()

    def is_safe(nums: list[int]) -> bool:
        nums = np.array(nums)
        diff = np.diff(nums)
        in_range = np.all(np.abs(diff) >= 1) and np.all(np.abs(diff) <= 3)
        consistent_sign = np.all(diff < 0) or np.all(diff > 0)
        return bool(in_range and consistent_sign)

    num_safe = 0
    for line in lines:
        report = list(map(int, line.split()))
        diff = np.diff(report)
        if is_safe(report):
            num_safe += 1

    print(f"day 2.1 solution: {num_safe}")

    # day 2.1 (polars)
    MAX_COLUMNS = 8
    schema = {f"col{i}": pl.Int64 for i in range(MAX_COLUMNS)}
    df = pl.read_csv(path, separator=" ", schema=schema, has_header=False)

    # partition based on which one should be increasing
    increasing_df = df.filter(pl.col("col2") > pl.col("col1"))
    decreasing_df = df.filter(pl.col("col2") < pl.col("col1"))

    # define the filter expressions for each case (increasing/decreasing)
    def get_filter_expression(increasing: bool, column_idx: int):
        increment_expression = (
            (pl.col(f"col{column_idx}") < pl.col(f"col{column_idx+1}"))
            if increasing
            else (pl.col(f"col{column_idx}") > pl.col(f"col{column_idx+1}"))
        )
        return (
            (abs(pl.col(f"col{i}").sub(pl.col(f"col{i+1}"))) >= 1)
            & (abs(pl.col(f"col{i}").sub(pl.col(f"col{i+1}"))) <= 3)
            & increment_expression
            | (pl.col(f"col{i}").is_null())
            | (pl.col(f"col{i+1}").is_null())
        )

    # filter dataframes based on condition
    for i in range(len(df.columns) - 1):
        increasing_df = increasing_df.filter(get_filter_expression(True, i))
        decreasing_df = decreasing_df.filter(get_filter_expression(False, i))

    print(f"day 2.1 solution (polars): {len(increasing_df) + len(decreasing_df)}")

    # day 2.2
    num_safe = 0
    for line in lines:
        report = list(map(int, line.split()))
        if is_safe(report):
            num_safe += 1
        else:
            for i in range(len(report)):
                sub_report = report[:i] + report[i + 1 :]
                if is_safe(sub_report):
                    num_safe += 1
                    break

    print(f"day 2.2 solution: {num_safe}")
