"""Re-run the quote check on saved predictions, without calling the model again.

Use this after the quote check itself changes. Flags removed by the old check are
restored if their quote now passes; flags that still fail stay removed.

Usage:
    python eval/reverify.py eval/results/predictions_<model>.json
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from casenote import quote_in_note  # noqa: E402


def main(pred_path):
    notes = {c["id"]: c["note"] for c in
             json.load(open(ROOT / "data/synthetic_cases/notes.json", encoding="utf-8"))["cases"]}
    preds = json.load(open(pred_path, encoding="utf-8"))
    restored = 0
    for cid, pred in preds.items():
        still_removed = []
        for flag in pred.get("removed_unverified_quotes", []):
            if quote_in_note(flag.get("quote", ""), notes[cid]):
                subject = "person" if "domain" in flag else (
                    "young_carer" if flag.get("area") == "child_care_tasks" else "caregiver")
                pred.setdefault(subject, []).append(flag)
                restored += 1
                print(f"{cid}: restored {flag.get('domain', flag.get('area'))}: {flag['quote'][:70]}")
            else:
                still_removed.append(flag)
        pred["removed_unverified_quotes"] = still_removed
    json.dump(preds, open(pred_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\n{restored} flag(s) restored. Saved {pred_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python eval/reverify.py eval/results/predictions_<model>.json")
    main(sys.argv[1])
