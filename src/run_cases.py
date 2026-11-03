"""Run CaseNote AI on all synthetic cases and save the predictions.

Progress is saved after every case. If the run stops (for example because the
model is busy), run it again and it continues where it left off.

Usage:
    CASENOTE_PROVIDER=gemini python src/run_cases.py
    CASENOTE_PROVIDER=anthropic python src/run_cases.py
"""

import json
import os
import time
from pathlib import Path

from casenote import PROVIDERS, analyze_note, load_criteria

ROOT = Path(__file__).resolve().parent.parent
PAUSE = float(os.environ.get("CASENOTE_PAUSE", "6"))
RETRY_WAITS = [30, 60, 120, 240]  # seconds
TEMPORARY = {429, 500, 502, 503, 504, 529}  # busy or rate-limited


def is_temporary(error):
    code = getattr(error, "code", None) or getattr(error, "status_code", None)
    return code in TEMPORARY


def analyze_with_retry(note, criteria):
    for attempt, wait in enumerate([0] + RETRY_WAITS):
        if wait:
            print(f"  model busy, waiting {wait} s (retry {attempt} of {len(RETRY_WAITS)})")
            time.sleep(wait)
        try:
            return analyze_note(note, criteria)
        except Exception as e:  # noqa: BLE001
            if not is_temporary(e) or attempt == len(RETRY_WAITS):
                raise


def main():
    provider = os.environ.get("CASENOTE_PROVIDER", "anthropic")
    model = os.environ.get("CASENOTE_MODEL", PROVIDERS[provider][1])
    out = ROOT / f"eval/results/predictions_{model}.json"
    preds = json.load(open(out, encoding="utf-8")) if out.exists() else {}

    criteria = load_criteria()
    notes = json.load(open(ROOT / "data/synthetic_cases/notes.json", encoding="utf-8"))
    for case in notes["cases"]:
        if case["id"] in preds:
            print(f"{case['id']} already done, skipping")
            continue
        print(f"Analysing {case['id']}...")
        try:
            preds[case["id"]] = analyze_with_retry(case["note"], criteria)
        except Exception as e:  # noqa: BLE001
            print(f"  stopped at {case['id']}: {e}\n  Run this cell again later to continue.")
            break
        json.dump(preds, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        time.sleep(PAUSE)

    done = len(preds)
    print(f"\n{done} of {len(notes['cases'])} cases done. Saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
