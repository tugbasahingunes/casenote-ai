# Evaluation report: `keyword-baseline`

| Metric | Result | What it means |
| --- | --- | --- |
| Missed signals | 11 of 45 (24%) | Expert-flagged concerns the system did not raise to review |
| Domain 12 (abuse/neglect) missed | 0 of 1 | The most serious miss |
| Under-escalated | 0 | Urgent cases raised only to normal review |
| Harmful over-flagging | 11 | Flags on domains the expert marked as traps |
| Diagnostic labels used | 0 | Forbidden terms in the system's own words |
| Extra flags | 33 | Review flags the expert did not set (not always wrong) |
| Coverage gaps | precision 79%, recall 80% | Agreement with expert 'no information' domains |
| Said vs. observed | 0 of 5 | Contradictions between statements and observations detected |
| Quote accuracy | 100% | Flags whose quote appears word for word in the note |

## Per case

| Case | Missed | Under-escalated | Harmful over-flags | Extra |
| --- | --- | --- | --- | --- |
| C01 | – | – | – | 11, 1 |
| C02 | – | – | – | 4, 5, 11 |
| C03 | carer:care_burden_health, carer:social_isolation, carer:work_income_loss, young carer:child_care_tasks | – | – | 1, 7, 4 |
| C04 | carer:care_burden_health, carer:psychological_wellbeing, carer:social_isolation, carer:substance_use | – | 12 | 4, 11, 3, 10 |
| C05 | – | – | 6, 2, 8, 5, 4, 11 | – |
| C06 | – | – | – | 4 |
| C07 | – | – | 12 | 2, 3 |
| C08 | – | – | 12 | 11 |
| C09 | 9 | – | 12, 2 | 8, 11, 3 |
| C10 | 3, 8 | – | – | 4, 7, 9, 5, 1, 2, 11 |
| C11 | – | – | – | 8, 2, 11 |
| C12 | – | – | – | 4, 9, 11, 2 |
