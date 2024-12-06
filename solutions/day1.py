from pathlib import Path

import numpy as np
import polars as pl

if __name__ == "__main__":
    # day 1.1
    df = pl.read_csv(Path("inputs/day1.csv"))
    left = df.select("left").to_series().sort()
    right = df.select("right").to_series().sort()
    print(f"day 1.1 solution: {(left - right).abs().sum()}")

    # day 1.2
    right_counts = df.group_by(
        "right"
    ).len()  # tells us how many times each unique value in right appears
    solution = (
        df.join(right_counts, left_on="left", right_on="right", how="left")
        .select(
            [
                pl.col("left"),
                pl.col("right"),
                pl.col("len").fill_null(0).alias("count"),
            ]
        )
        .with_columns(score=pl.col("left") * pl.col("count"))
        .select("score")
        .sum()
    )
    print(f"day 1.2 solution: {solution.item()}")
