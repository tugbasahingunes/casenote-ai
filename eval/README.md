# Evaluation

`evaluate.py` compares a system's predictions with the expert gold labels in `data/synthetic_cases/labels.json`.

Missing a risk and wrongly flagging a family are different harms, so they are reported separately instead of being folded into one accuracy number.

## Metrics

| Metric | Definition |
| --- | --- |
| **Missed signals** | Expert concerns (level `human_review` or higher) that the system did not raise to review |
| **Domain 12 missed** | Missed signals in suspected neglect or abuse, the most serious miss |
| **Under-escalated** | Expert `urgent_human_review` flags that the system raised only to `human_review` |
| **Harmful over-flagging** | Review flags on domains the expert marked as `overflag_traps`, and any review flag in the clean case |
| **Diagnostic labels** | Forbidden diagnostic terms in the system's own words (quotes from the note are excluded) |
| **Extra flags** | Review flags the expert did not set. Not always wrong, but worth inspecting |
| **Coverage gaps** | Precision and recall against the expert's "no information" domains |
| **Said vs. observed** | Cases where the expert recorded a contradiction and the system detected one |
| **Quote accuracy** | Share of flags whose quote appears word for word in the note. Unverified quotes are removed before scoring |

## Results so far

| System | Missed signals | Harmful over-flagging | Said vs. observed | Report |
| --- | --- | --- | --- | --- |
| Keyword baseline (no AI) | 11 of 45 (24%) | 11 | 0 of 5 | [report](results/report_keyword-baseline.md) |
| LLM (Claude) | *coming* | | | |

The keyword baseline sets the bar. It misses every family carer and young carer signal, raises six false alarms in the clean case (C05), flags hearing loss as cognitive decline (C09) and never detects a said-vs-observed contradiction. An AI system is only useful if it beats this on both kinds of error at once.

## Not yet scored

- Change over time between C01 and C11 (improved vs. worsened domains)
- Need–action check from `docs/criteria.md`
- Group-wise comparison across language and gender

## Run

```bash
python src/baseline_keywords.py
python eval/evaluate.py eval/results/predictions_keyword-baseline.json

export ANTHROPIC_API_KEY=...        # never commit your key
python src/run_cases.py
python eval/evaluate.py eval/results/predictions_claude-sonnet-5-5.json
```
