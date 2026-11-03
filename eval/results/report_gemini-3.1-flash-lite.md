# Evaluation report: `gemini-3.1-flash-lite`

| Metric | Result | What it means |
| --- | --- | --- |
| Missed signals | 8 of 45 (18%) | Expert-flagged concerns the system did not raise to review |
|  of which flagged only as record | 6 | Seen, but judged not to need review |
|  of which not flagged at all | 2 | Not noticed |
| Domain 12 (abuse/neglect) missed | 0 of 1 | The most serious miss |
| Under-escalated | 0 | Urgent cases raised only to normal review |
| Harmful over-flagging | 1 | Flags on domains the expert marked as traps |
| Diagnostic labels used | 0 | Forbidden terms in the system's own words |
| Extra flags | 2 | Review flags the expert did not set (not always wrong) |
| Coverage gaps | precision 81%, recall 93% | Agreement with expert 'no information' domains |
| Said vs. observed | 4 of 5 | Contradictions between statements and observations detected |
| Quote accuracy | 99% | Flags whose quote appears word for word in the note |

## Per case

| Case | Missed | Under-escalated | Harmful over-flags | Extra |
| --- | --- | --- | --- | --- |
| C01 | 9 (record) | – | – | – |
| C02 | 9 (record), 8 (record) | – | – | – |
| C03 | – | – | – | – |
| C04 | – | – | – | 11 |
| C05 | – | – | 9 | – |
| C06 | 5 (record) | – | – | – |
| C07 | – | – | – | – |
| C08 | 2 (record) | – | – | – |
| C09 | 9 | – | – | – |
| C10 | 3 | – | – | 4 |
| C11 | – | – | – | – |
| C12 | 1 (record) | – | – | – |

"(record)" = the system flagged the signal but only at record level, not for review.
