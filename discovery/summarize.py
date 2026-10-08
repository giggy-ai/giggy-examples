import csv
from collections import defaultdict
from pathlib import Path


RESULTS_PATH = Path(__file__).parent / "results.csv"


def main() -> None:
    with RESULTS_PATH.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("No discovery measurements recorded.")
        return

    metrics = defaultdict(
        lambda: {"tested": 0, "mentioned": 0, "cited": 0, "code_passed": 0}
    )
    for row in rows:
        agent = row["agent"]
        metrics[agent]["tested"] += 1
        if row["giggy_mentioned"].lower() == "true":
            metrics[agent]["mentioned"] += 1
        if row["cited_url"].strip():
            metrics[agent]["cited"] += 1
        if row["generated_code_passed"].lower() == "true":
            metrics[agent]["code_passed"] += 1

    for agent, values in sorted(metrics.items()):
        tested = values["tested"]
        mention_rate = values["mentioned"] / tested * 100
        print(
            "{}: {} tests, {:.1f}% mentioned, {} cited, {} code passed".format(
                agent, tested, mention_rate, values["cited"], values["code_passed"]
            )
        )


if __name__ == "__main__":
    main()
