# Synthetic case set v2

12 synthetic home-visit notes about older people in Finland, each with an expert-written gold answer.

**All cases are fictional.** They are not based on any real person, case file or institutional record. Case ideas and labelling decisions are the author's own.

## Files

| File | Purpose |
| --- | --- |
| `cases.md` | Human-readable notes, what each case tests, and gold labels |
| `labels.json` | Machine-readable gold labels for the evaluation scripts |

## Why these profiles

The cases are designed to reflect documented features of older people's lives in Finland, not only common risk factors:

| Profile feature | Evidence | Cases |
| --- | --- | --- |
| Ageing population | 24% of Finns were aged 65+ at the end of 2025 ([Statistics Finland](https://stat.fi/en/news/Finland-in-Figures-2026-ageing-Finland-is-visible-in-numbers)) | all |
| Loneliness peaks in old age | Loneliness is most common among people over 75 ([University of Jyväskylä](https://jyx.jyu.fi/handle/123456789/81555)) | C01, C07, C08, C11 |
| Family caregiving at scale | About 300,000 informal care situations; around one million Finns help a relative ([MTV Uutiset / Omaishoitajat ja Läheiset](https://www.mtvuutiset.fi/artikkeli/oletko-omaishoitaja-kerro-arjestasi/270142)) | C03, C04 |
| Dementia drives family care | Memory disorders are the most common reason for informal care, in about a third of cases ([HE 110/2025](https://www.edilex.fi/he/20250110)) | C04 |
| Care support is budget-bound | Informal care support depends on each county's budget and criteria ([SeAMK](https://lehti.seamk.fi/verkkolehti/omaishoito-merkittava-voimavara/?print=pdf)) | C03 |
| Rising alcohol use in later life | Older people's drinking has become more common since the mid-1980s ([Nordic Studies on Alcohol and Drugs](https://pmc.ncbi.nlm.nih.gov/articles/PMC8899280)); recent cohorts, especially women, drink more than earlier ones ([Jemberie et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12365579/)) | C04, C08 |
| Older migrants face access barriers | Russian speakers are the largest foreign-language minority; barriers include language and lack of electronic identification for digital services ([Safarov et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10900858)) | C07 |
| Swedish-speaking older adults | Research reports experiences of exclusion in services in their first language ([Hemberg](https://feedbagel.com/author/jessica-hemberg)) | C10 |
| Distance and dispersed population | Small, dispersed populations create spatial access disparities ([Safarov et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10900858)) | C01, C12 |

## What the set tests

| Test | Cases |
| --- | --- |
| Signals hidden behind "I don't need anything" (said vs. observed) | C01, C04, C11 |
| Caregiver as a second subject (absorbed need) | C03, C04 |
| A minor acting as a carer | C03 |
| Subtle financial abuse with a family member present | C06 |
| Avoiding diagnostic language for mental health changes | C02 |
| Not mistaking hearing loss for cognitive decline | C09 |
| Language barrier and family interpreter | C07, C10 |
| Clean case: no false alarms | C05 |
| Messy, long note | C10 |
| Change over time (second visit) | C11 |
| Rural distance and service access | C12 |

## Label scheme

- **Review levels:** `record` · `human_review` · `urgent_human_review`
- **Subjects:** `person` (the older person) and, where relevant, `caregiver` and `young_carer`
- **`no_info`:** domains the note does not cover at all (coverage gaps)
- **`said_vs_observed`:** the person's statement and the observations that contradict it
- **`overflag_traps`:** domains the system should **not** flag; flagging them counts as harmful over-flagging

Domains follow [`docs/criteria.md`](../../docs/criteria.md) (1–13).
