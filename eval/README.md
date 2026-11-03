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

| System | Missed signals | of which flagged only as record | Harmful over-flagging | Said vs. observed | Report |
| --- | --- | --- | --- | --- | --- |
| Keyword baseline (no AI) | 10 of 45 (22%) | 0 | 11 | 0 of 5 | [report](results/report_keyword-baseline.md) |
| Gemini 3.1 Flash Lite | 8 of 45 (18%) | 6 | 1 | 4 of 5 | [report](results/report_gemini-3.1-flash-lite.md) |

**Keyword baseline.** Misses every family-carer and young-carer signal, raises six alarms in the clean case (C05), reads the hearing-aid case as a memory problem and never detects a said-vs-observed contradiction.

**Gemini 3.1 Flash Lite.** Avoids all designed traps: no abuse flag for the locked door (C04), no cognitive flag for hearing loss (C09), no diagnostic language (C02, C08). Raises the quiet financial-abuse case (C06) as urgent, and treats the daughter-in-law and the 15-year-old grandson in C03 as separate subjects. Six of its eight misses are signals it noticed but rated only as "record":

| Case | Signal | Domain |
| --- | --- | --- |
| C01 | 40 km from the health centre; bus twice a week | 9 Service access |
| C02 | Saving money for future care; cancelled subscriptions | 9 Finances |
| C02 | Keeps radiators low | 8 Living environment |
| C06 | Little food in the fridge | 5 Nutrition |
| C08 | Sleeping pills, alongside nightly alcohol and a recent fall | 2 Medication |
| C12 | A fall, after which she waited for a neighbour instead of using the safety phone | 1 Physical function |

The two signals it did not flag at all: C09, not knowing where to get hearing-aid batteries (service access), and C10, the wife now in a nursing home who "doesn't always know him" (life event).

**Reading the pattern.** The model under-weights service access, finances and the living environment. Finnish studies of care documentation report the same tendency in human records, where physical issues dominate and social and economic needs receive less attention. A system that copies this pattern would reproduce an existing gap rather than close it.

**Notes on method**
- One run per system, 12 cases. Results show the method, not a general performance level.
- Labels version 2.1 accepts a second domain only where `cases.md` already listed two (for example "1 / 8") before any model was run. No label or level was changed after seeing results.
- The first run used a quote check that treated single and double quotation marks as different, which wrongly removed two valid quotes in C04. The check was fixed and the saved predictions re-verified with [`reverify.py`](reverify.py), without calling the model again.

## Not yet scored

- Change over time between C01 and C11 (improved vs. worsened domains)
- Need–action check from `docs/criteria.md`
- Group-wise comparison across language and gender

## Run

**Recommended: GitHub Actions.** In the repository, open **Actions → Run evaluation → Run workflow**. The model key is stored as a repository secret (`GEMINI_API_KEY` or `ANTHROPIC_API_KEY`). The score table appears on the run page, and predictions and the report can be downloaded under **Artifacts**.

**Alternatives:** the [Colab notebook](../notebooks/run_in_colab.ipynb), or locally:

```bash
python src/baseline_keywords.py
python eval/evaluate.py eval/results/predictions_keyword-baseline.json

export GEMINI_API_KEY=...           # never commit your key
CASENOTE_PROVIDER=gemini CASENOTE_MODEL=gemini-3.1-flash-lite python src/run_cases.py
python eval/evaluate.py eval/results/predictions_gemini-3.1-flash-lite.json
```
