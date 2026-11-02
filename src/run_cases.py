"""Run CaseNote AI on all synthetic cases and save the predictions.

Usage:
    export ANTHROPIC_API_KEY=...
    python src/run_cases.py
"""

import json
from pathlib import Path

from casenote import DEFAULT_MODEL, analyze_note, load_criteria

ROOT = Path(__file__).resolve().parent.parent


def main():
    import anthropic

    client = anthropic.Anthropic()
    criteria = load_criteria()
    notes = json.load(open(ROOT / "data/synthetic_cases/notes.json", encoding="utf-8"))
    preds = {}
    for case in notes["cases"]:
        print(f"Analysing {case['id']}...")
        preds[case["id"]] = analyze_note(case["note"], criteria, client)
    out = ROOT / f"eval/results/predictions_{DEFAULT_MODEL}.json"
    json.dump(preds, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
