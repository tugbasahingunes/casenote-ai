"""A deliberately naive keyword baseline.

It flags a domain whenever a keyword appears, with no understanding of context.
It needs no API key. Its purpose is to show what the evaluation catches:
keyword matching misses subtle signals and raises false alarms.

Usage:
    python src/baseline_keywords.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KEYWORDS = {
    1: ["fall", "fell", "walker", "stick", "bedridden", "stairs"],
    2: ["medication", "forget", "pills", "tablet", "dosette"],
    3: ["tearful", "grief", "died", "cries", "lonely", "energy", "empty"],
    4: ["alone", "lonely", "friends", "visit"],
    5: ["fridge", "weight", "food", "appetite"],
    6: ["hearing", "glasses", "eyesight", "language", "finnish", "interpret"],
    7: ["garden", "shopping", "cooking"],
    8: ["roof", "mould", "lock", "cold", "radiator", "bracelet", "safety", "heat"],
    9: ["bill", "pension", "money", "bus", "km", "codes", "support"],
    10: ["beer", "wine", "bottles", "alcohol"],
    11: ["wants", "asked", "said"],
    12: ["bank", "papers", "codes", "bruise", "lock"],
    13: ["choir", "neighbour", "enjoys", "walks", "knits", "bakes", "church"],
}
ESCALATE = {8, 12}


def sentences(note):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", note) if s.strip()]


def predict(note):
    person, seen = [], set()
    for sent in sentences(note):
        low = sent.lower()
        for domain, words in KEYWORDS.items():
            if domain not in seen and any(w in low for w in words):
                seen.add(domain)
                level = "urgent_human_review" if domain == 12 else (
                    "human_review" if domain in ESCALATE or domain != 13 else "record")
                person.append({"domain": domain, "level": level, "quote": sent,
                               "source": "professional_observed"})
    return {
        "person": person,
        "caregiver": [],
        "young_carer": [],
        "no_info": [d for d in KEYWORDS if d not in seen],
        "said_vs_observed": [],
        "model": "keyword-baseline",
    }


def main():
    notes = json.load(open(ROOT / "data/synthetic_cases/notes.json", encoding="utf-8"))
    preds = {c["id"]: predict(c["note"]) for c in notes["cases"]}
    out = ROOT / "eval/results/predictions_keyword-baseline.json"
    json.dump(preds, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
