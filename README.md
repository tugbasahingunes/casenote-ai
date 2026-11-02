# CaseNote AI

**Evidence-based, expert-defined AI support for social care home-visit documentation.**

> **Status: Phase 1 — design and evaluation dataset.** Criteria, ethics framework and synthetic test cases are published first. Code and evaluation results will follow.

---

## The problem

Social and health care professionals spend a large part of their working day on documentation. In Finland, a professional in social and health services spends on average **3 hours 15 minutes a day** recording information ([Sitra](https://arkisto.sitra.fi/en/projects/ai-in-social-and-health-services/)).

AI documentation tools are already being piloted and rolled out. Early pilots show efficiency gains, but also raise questions about data protection, transparency and professional accountability ([University of Oulu](https://oulurepo.oulu.fi/handle/10024/64408)).

The open question is not *whether* AI can write a case note. It is:

**Who decides what the AI should look for — and how do we know when it gets it wrong?**

## What CaseNote AI does

A professional writes (or dictates) a free-text note after a home visit. CaseNote AI:

1. Scans the note across **13 assessment domains** defined by a social care expert.
2. Flags signals, each **linked to the exact sentence** in the note that supports it.
3. Assigns a review level: *record*, *human review*, or *urgent human review*.
4. Lists the domains the note **does not cover at all** (coverage gaps).
5. Records the person's **strengths and resources**, not only problems.
6. Treats a **family caregiver as a second subject**, so their burden does not disappear inside the cared-for person's file.

It never diagnoses, scores people, or decides eligibility for services. Every output is a draft for a professional to review.

## Why Finland

- **Ageing:** At the end of 2025, 24% of Finland's population were aged 65 or over ([Statistics Finland](https://stat.fi/en/news/Finland-in-Figures-2026-ageing-Finland-is-visible-in-numbers)).
- **A legally defined standard:** Since April 2023, municipalities must use the RAI system when assessing the functional capacity of older people who need regular social services ([Finlex, Act 565/2020](https://finlex.fi/api/media/statute/26315/mainPdf/main.pdf)). This makes Finland an ideal setting for expert-defined, evaluable AI support.
- **Policy direction:** Finland aims to raise public-sector productivity through AI and automation by 2031 ([Verkkouutiset](https://www.verkkouutiset.fi/a/en/minister-finlands-public-sector-cannot-remain-stuck-in-ai-pilot-projects/)).

*RAI is a licensed interRAI instrument. This project does not reproduce RAI items; its criteria are independently written.*

## Approach

**1. The expert defines the criteria.** The 13 domains are grounded in the Finnish Act on Services for Older Persons, the WHO ICF and ICOPE frameworks, and Finnish research on gaps in care documentation. See [`docs/criteria.md`](docs/criteria.md).

**2. Every output is evidence-based.** Each flag quotes the sentence it relies on. No quote, no flag.

**3. Performance is measured against expert labels.** Every synthetic case comes with an expert-written "gold" answer. The system is evaluated against it.

## What makes this different

- **Asymmetric error costs.** Missing a risk signal and wrongly flagging a caregiver as negligent are different harms. The evaluation measures them separately: *missed signals* and *harmful over-flagging*.
- **Coverage gap reporting.** The system reports what the note does not mention, because research shows psychological and social domains are often under-documented.
- **Said vs. observed.** When a person says "I don't need anything" but the observations suggest otherwise, both are shown side by side. The person's voice is never discarded.
- **The caregiver as a second subject.** In family-centred care, needs are often absorbed by a relative. This project makes that *absorbed need* visible.
- **Strengths-based output.** Resources and coping strategies are recorded alongside risks.
- **Context-adaptable.** Criteria live in a separate file, so the system can be adapted to another country's framework without changing the code.

## Ethics and compliance

- **Synthetic data only.** No real case, client or institutional data is used.
- **Support, not decisions.** Under the EU AI Act, systems used by public authorities to evaluate eligibility for public assistance are high-risk ([Annex III](https://www.artificialintelligenceact.eu/annex/3/)). CaseNote AI is designed to stay out of that role.
- **No scoring of people.** No risk, fraud or trustworthiness scores.
- **No diagnostic language.** Observations are reported, not interpreted as diagnoses.
- **Transparency.** Users are informed they are working with AI.

See [`docs/ethics.md`](docs/ethics.md) for the full framework and a draft data protection impact assessment.

## Repository structure

```
casenote-ai/
├── README.md
├── docs/
│   ├── criteria.md          # 13 assessment domains and flagging rules
│   └── ethics.md            # ethics, EU AI Act, GDPR, DPIA draft
├── data/
│   └── synthetic_cases/     # 12 synthetic notes + expert gold labels
├── src/                     # (coming) application code
└── eval/                    # (coming) evaluation scripts and results
```

## Roadmap

- [x] Assessment criteria (Finland, older people living at home)
- [x] Ethics and compliance framework
- [x] 12 synthetic cases with expert labels (v2)
- [ ] 20 synthetic cases
- [ ] Prototype: note → structured flags (Python + LLM API)
- [ ] Evaluation: missed signals, harmful over-flagging, coverage gaps
- [ ] Simple interface and demo video
- [ ] Review by practising social care professionals

## Author

**Tuğba Güneş** — social policy and family services specialist with 10+ years of experience in social research and data-driven policy. Building AI tools grounded in how social care actually works.

[LinkedIn](https://www.linkedin.com/public-profile/settings/?trk=d_flagship3_profile_self_view_public_profile&lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3BBTsAsmnaSraMRoqpLEvNYQ%3D%3D)

*Developed with AI assistance. Domain criteria, case design and evaluation labels are the author's own.*
