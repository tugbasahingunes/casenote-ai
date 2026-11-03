"""Compare predictions with the expert gold labels.

Missing a risk and wrongly flagging a family are different harms, so they are
reported separately instead of being folded into one accuracy number.

Usage:
    python eval/evaluate.py eval/results/predictions_<model>.json
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RANK = {"record": 0, "human_review": 1, "urgent_human_review": 2}


def keyed(flags, subject, key):
    """Map (subject, domain-or-area) -> highest level."""
    out = {}
    for f in flags:
        k = (subject, f[key])
        out[k] = max(out.get(k, -1), RANK[f["level"]])
    return out


def all_levels(case):
    levels = {}
    levels.update(keyed(case.get("person", []), "person", "domain"))
    levels.update(keyed(case.get("caregiver", []), "caregiver", "area"))
    levels.update(keyed(case.get("young_carer", []), "young_carer", "area"))
    return levels


def free_text(obj, skip="quote"):
    """All string values except quotes copied from the note."""
    if isinstance(obj, dict):
        return " ".join(free_text(v) for k, v in obj.items() if k != skip)
    if isinstance(obj, list):
        return " ".join(free_text(v) for v in obj)
    return obj if isinstance(obj, str) else ""


def accepted_alternatives(gold):
    """(subject, domain) -> other domains the expert also accepts for that signal."""
    return {("person", f["domain"]): {("person", a) for a in f.get("accept", [])}
            for f in gold.get("person", []) if f.get("accept")}


def evaluate_case(gold, pred):
    g, p = all_levels(gold), all_levels(pred)
    alts = accepted_alternatives(gold)

    def best(k):
        """Highest level the system gave this signal, in its domain or an accepted one."""
        return max([p.get(k, -1)] + [p.get(a, -1) for a in alts.get(k, ())])

    concerns = [k for k, lv in g.items() if lv >= 1]
    missed = [k for k in concerns if best(k) < 1]
    seen_low = [k for k in missed if best(k) == 0]      # flagged, but only as "record"
    not_seen = [k for k in missed if best(k) == -1]     # not flagged at all
    under = [k for k, lv in g.items() if lv == 2 and best(k) == 1]

    traps = set(gold.get("overflag_traps", []))
    harmful = [k for k, lv in p.items() if k[0] == "person" and k[1] in traps and lv >= 1]
    if gold.get("max_level") == "record":
        harmful += [k for k, lv in p.items() if lv >= 1 and k not in harmful]
    text = free_text(pred).lower()
    labels = [t for t in gold.get("forbidden_terms", []) if t in text]

    covered = set(concerns) | {a for k in concerns for a in alts.get(k, ())}
    extra = [k for k, lv in p.items() if lv >= 1 and k not in covered and g.get(k, -1) < 1
             and k not in harmful]

    gold_gap, pred_gap = set(gold.get("no_info", [])), set(pred.get("no_info", []))
    total_quotes = sum(len(pred.get(s, [])) for s in ("person", "caregiver", "young_carer"))
    removed = len(pred.get("removed_unverified_quotes", []))

    return {
        "concerns": len(concerns),
        "missed": missed,
        "seen_low": seen_low,
        "not_seen": not_seen,
        "under_escalated": under,
        "harmful_overflags": harmful,
        "diagnostic_labels": labels,
        "extra_flags": extra,
        "gap_tp": len(gold_gap & pred_gap),
        "gap_gold": len(gold_gap),
        "gap_pred": len(pred_gap),
        "svo_expected": gold.get("said_vs_observed") is not None,
        "svo_found": bool(pred.get("said_vs_observed")),
        "quotes": total_quotes + removed,
        "quotes_removed": removed,
        "d12_gold": [k for k in concerns if k == ("person", 12)],
        "d12_missed": [k for k in missed if k == ("person", 12)],
    }


def fmt(keys):
    prefix = {"person": "", "caregiver": "carer:", "young_carer": "young carer:"}
    return ", ".join(f"{prefix[s]}{k}" for s, k in keys) or "–"


def main(pred_path):
    gold = {c["id"]: c for c in json.load(open(ROOT / "data/synthetic_cases/labels.json"))["cases"]}
    preds = json.load(open(pred_path, encoding="utf-8"))
    name = Path(pred_path).stem.replace("predictions_", "")
    rows = {cid: evaluate_case(gold[cid], preds.get(cid, {})) for cid in gold}

    s = lambda key: sum(len(r[key]) if isinstance(r[key], list) else r[key] for r in rows.values())
    concerns, missed = s("concerns"), s("missed")
    svo_exp = sum(r["svo_expected"] for r in rows.values())
    svo_ok = sum(r["svo_expected"] and r["svo_found"] for r in rows.values())
    gap_p = s("gap_tp") / s("gap_pred") if s("gap_pred") else 0
    gap_r = s("gap_tp") / s("gap_gold") if s("gap_gold") else 0
    q_ok = 1 - s("quotes_removed") / s("quotes") if s("quotes") else 1

    lines = [
        f"# Evaluation report: `{name}`", "",
        "| Metric | Result | What it means |", "| --- | --- | --- |",
        f"| Missed signals | {missed} of {concerns} ({missed / concerns:.0%}) | Expert-flagged concerns the system did not raise to review |",
        f"| \u2003of which flagged only as record | {s('seen_low')} | Seen, but judged not to need review |",
        f"| \u2003of which not flagged at all | {s('not_seen')} | Not noticed |",
        f"| Domain 12 (abuse/neglect) missed | {s('d12_missed')} of {s('d12_gold')} | The most serious miss |",
        f"| Under-escalated | {s('under_escalated')} | Urgent cases raised only to normal review |",
        f"| Harmful over-flagging | {s('harmful_overflags')} | Flags on domains the expert marked as traps |",
        f"| Diagnostic labels used | {s('diagnostic_labels')} | Forbidden terms in the system's own words |",
        f"| Extra flags | {s('extra_flags')} | Review flags the expert did not set (not always wrong) |",
        f"| Coverage gaps | precision {gap_p:.0%}, recall {gap_r:.0%} | Agreement with expert 'no information' domains |",
        f"| Said vs. observed | {svo_ok} of {svo_exp} | Contradictions between statements and observations detected |",
        f"| Quote accuracy | {q_ok:.0%} | Flags whose quote appears word for word in the note |",
        "", "## Per case", "",
        "| Case | Missed | Under-escalated | Harmful over-flags | Extra |", "| --- | --- | --- | --- | --- |",
    ]
    footnote = "\n\"(record)\" = the system flagged the signal but only at record level, not for review.\n"
    for cid, r in rows.items():
        missed_txt = ", ".join(
            [fmt([k]) + " (record)" for k in r["seen_low"]] + [fmt([k]) for k in r["not_seen"]]) or "–"
        lines.append(f"| {cid} | {missed_txt} | {fmt(r['under_escalated'])} | "
                     f"{fmt(r['harmful_overflags'])}{' ' + str(r['diagnostic_labels']) if r['diagnostic_labels'] else ''} | {fmt(r['extra_flags'])} |")
    report = "\n".join(lines) + "\n" + footnote
    out = ROOT / f"eval/results/report_{name}.md"
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"Saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python eval/evaluate.py eval/results/predictions_<model>.json")
    main(sys.argv[1])
