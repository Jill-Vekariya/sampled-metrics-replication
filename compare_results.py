"""Compare a rerun to the archived Windows evidence without changing it."""
import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
FIELDS = (
    "exact", "expected", "analytic_sd", "monte_carlo_mean",
    "monte_carlo_sd", "calibration_mean",
)


def compare_summaries(original, rerun):
    """Return numeric differences; reject incompatible experiment summaries."""
    if original["protocol_sha256"] != rerun["protocol_sha256"]:
        raise ValueError("Protocol changed")
    if len(original["primary"]) != len(rerun["primary"]):
        raise ValueError("Primary result counts differ")
    errors = []
    for x, y in zip(original["primary"], rerun["primary"], strict=True):
        if (x["model"], x["metric"]) != (y["model"], y["metric"]):
            raise ValueError("Primary model/metric order differs")
        for name in FIELDS:
            if not np.isclose(x[name], y[name], rtol=0, atol=1e-12):
                errors.append({
                    "model": x["model"], "metric": x["metric"], "field": name,
                    "reference": x[name], "rerun": y[name],
                })
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rerun", help="Result directory relative to project root")
    args = parser.parse_args()
    original = json.loads(
        (ROOT / "results/windows-final/summary.json").read_text(encoding="utf-8")
    )
    rerun = json.loads(
        (ROOT / args.rerun / "summary.json").read_text(encoding="utf-8")
    )
    try:
        errors = compare_summaries(original, rerun)
    except ValueError as exc:
        parser.exit(2, f"Comparison failed: {exc}\n")
    print(json.dumps({"match_within_1e-12": not errors, "differences": errors}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
