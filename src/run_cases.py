"""Run CaseNote AI on all synthetic cases and save the predictions.

Usage:
    CASENOTE_PROVIDER=gemini python src/run_cases.py
    CASENOTE_PROVIDER=anthropic python src/run_cases.py
"""

import json
import os
import time
from pathlib import Path

from casenote import analyze_note, load_criteria

ROOT = Path(__file__).resolve().parent.parent
PAUSE = float(os.environ.get("CASENOTE_PAUSE", "6"))


def main():
    criteria = load_criteria()
    notes = json.load(open(ROOT / "data/synthetic_cases/notes.json", encoding="utf-8"))
    preds = {}
    for case in notes["cases"]:
        print(f"Analysing {case['id']}...")
        preds[case["id"]] = analyze_note(case["note"], criteria)
        time.sleep(PAUSE)  # stay within free-tier rate limits
    model = next(iter(preds.values()))["model"]
    out = ROOT / f"eval/results/predictions_{model}.json"
    json.dump(preds, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
