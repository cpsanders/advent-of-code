from pathlib import Path

import polars as pl


def calculate_middle_sums(rules_path: Path, updates_path: Path) -> None:
    rules_arr = pl.read_csv(rules_path, separator="|").to_numpy()

    # create hash map of rules
    rules_hash: dict[int, list[int]] = {}
    for rule in rules_arr:
        if rules_hash.get(rule[0]) is None:
            rules_hash[int(rule[0])] = [int(rule[1])]
        else:
            rules_hash[rule[0]].append(int(rule[1]))

    valid_middle_page_sum = 0
    sorted_middle_page_sum = 0
    with updates_path.open("r") as file:
        for i, line in enumerate(file):
            page_update = list(map(int, line.strip().split(",")))
            update_is_valid = True

            # validate sort order, sort if needed
            j = 1
            while j < len(page_update):
                page_rules = rules_hash.get(page_update[j])
                if page_rules is None:  # if no rule specified for the given page number
                    j += 1
                    continue

                for page_rule in page_rules:
                    if page_rule in page_update[:j]:
                        update_is_valid = False
                        move_page = page_update.pop(j)
                        page_update.insert(j - 1, move_page)
                        j = 0
                        break
                j += 1

            if update_is_valid:
                valid_middle_page_sum += page_update[len(page_update) // 2]
            else:
                sorted_middle_page_sum += page_update[len(page_update) // 2]

    print(f"Originally-correct sum: {valid_middle_page_sum}")
    print(f"Originally-incorrect sum: {sorted_middle_page_sum}")


if __name__ == "__main__":
    # day 5.1 + 5.2
    rules_path = Path("inputs/day5_rules.txt")
    updates_path = Path("inputs/day5_updates.txt")
    calculate_middle_sums(rules_path, updates_path)
