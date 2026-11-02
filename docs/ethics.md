# Ethics and compliance

*This is a design document, not legal advice. CaseNote AI is a portfolio project that works only with synthetic data, so no compliance obligations apply today. This document answers the question: what would it take to use this responsibly in real practice?*

## Summary

CaseNote AI is designed as a **documentation support tool**, not a decision system. It never scores people, ranks them, or decides eligibility for services. The three design errors that most often make public-sector AI unacceptable are:

1. giving people risk scores or priority rankings,
2. influencing access to services,
3. not telling users they are working with AI.

The design below avoids all three.

## Legal framework

| Rule | What it says | When | Relevance to CaseNote AI |
| --- | --- | --- | --- |
| EU AI Act, Annex III 5(a): high risk | Systems used by public authorities to evaluate eligibility for public assistance and services are high-risk ([Annex III](https://www.artificialintelligenceact.eu/annex/3/)); systems that prioritise applications and thereby affect access are also covered ([AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/fr/node/465)) | 2 December 2027, postponed by the Digital Omnibus ([Cuatrecasas](https://www.cuatrecasas.com/en/latam/intellectual-property/art/digital-omnibus-ai-has-been-published)) | CaseNote AI must stay out of eligibility and prioritisation. It flags documented facts; it does not rank cases. |
| AI Act: support-service carve-out | Systems that only help deliver a public support service, without evaluating a person's eligibility, fall outside 5(a) ([AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/pl/node/465)) | — | The intended positioning of CaseNote AI. |
| AI Act: the "human in the loop" fallacy | Saying "a human makes the final decision" does not automatically remove a system from the high-risk class; Annex III also covers systems that influence human decisions ([Presencis](https://presencis.com/regulations/eu-ai-act/article-6/)) | — | Human approval alone is not enough. The design itself must not steer decisions (no scores, no rankings, evidence quotes only). |
| AI Act Article 50(1): transparency | AI systems that interact directly with people must inform them they are interacting with AI, unless obvious from context ([European Commission](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)) | In force since 2 August 2026 ([CMS](https://cms.law/en/gbr/legal-updates/eu-ai-act-transparency-real-world-examples)) | Every output is labelled as an AI-generated draft. |
| GDPR Article 9: special category data | Health data is prohibited by default; an exception is needed, such as health or social care (9(2)(h)) or explicit consent (9(2)(a)) ([Layer3](https://www.layer3labs.io/guides/gdpr-ai-health-data-compliance)) | In force | Home-visit notes contain health and social care data. A real deployment would rely on 9(2)(h) under the controller's responsibility. |
| GDPR Article 22: automated decisions | Solely automated decisions with legal or similarly significant effects are restricted; a DPIA is required for such processing ([GDPR Local](https://gdprlocal.com/automated-decision-making-gdpr/)) | In force | No decision is made by the system. Every output is a draft approved by a professional. |

## A lesson that shapes the design

In the Netherlands, a risk model used to detect childcare benefit fraud treated non-Dutch nationality as a risk factor; Amnesty International found this to be ethnic profiling ([Dutch IT Channel](https://www.dutchitchannel.nl/news/174184/amnesty-international-reguleer-algoritmes-na-toeslagenaffaire)). The scandal led to the government's resignation in 2021 ([IBFD](https://shop.ibfd.org/journal/lessons-be-learned-dutch-childcare-allowance-scandal-comparative-review-algorithmic)).

CaseNote AI takes three direct lessons from this:

- **No scores.** A flag is a quoted fact plus a review level, never a number about a person.
- **No protected attributes as signals.** Language or origin appears in a note only as a service-access fact (for example, "letter was in Finnish"), never as a risk factor.
- **Over-flagging is measured as harm.** Wrongly flagging a family as neglectful is treated as a separate, serious error in the evaluation, not as a "safe" mistake.

## Red lines

The system never:

- gives people risk, fraud or trustworthiness scores;
- decides eligibility for assistance or services, or ranks people;
- uses nationality, origin, ethnicity or religion as model inputs for flagging;
- works with real case, client or institutional data;
- hides that its output is AI-generated;
- diagnoses, or recommends medication or legal strategy;
- sends a notification under §25 by itself. It only directs the professional to consider their duty.

## Design principles

- **Evidence-bound output.** Every flag quotes the note. No quote, no flag.
- **Meaningful human control.** Outputs are drafts. Approval is required, and the design avoids nudging the reviewer (no scores, no colour-coded people).
- **The person's voice.** What the person said is shown separately from what was observed, and never overwritten.
- **Strengths alongside risks.** Resources are recorded so the output does not become a deficit profile.
- **Data minimisation.** In a real deployment, notes would be processed for the draft and not retained by the AI component.
- **Fairness in evaluation.** The synthetic set includes different genders, ages, languages (Finnish, Swedish, Russian) and living situations. Results will be compared across these groups.
- **Co-design.** Criteria and labels are to be reviewed by practising professionals before any claim of usefulness.

## Draft data protection impact assessment (DPIA)

*A simplified draft showing what a real deployment would need to address. A real DPIA is the controller's responsibility (for example, a Finnish wellbeing services county).*

| Item | Draft answer |
| --- | --- |
| Purpose | Support professionals in documenting home visits: structure notes, surface signals with evidence, report coverage gaps |
| Data subjects | Older people receiving home visits; family carers and other relatives mentioned in notes |
| Data categories | Free-text notes; may contain health and social care data (GDPR Art. 9), family relationships, financial circumstances |
| Legal basis (indicative) | GDPR Art. 6(1)(e) public task; Art. 9(2)(h) health or social care |
| Automated decision-making | None. No decision or legal effect results from the output without professional review |
| Key risks | (1) Hallucinated or misquoted evidence; (2) missed signals, especially abuse; (3) over-flagging that stigmatises families or carers; (4) bias across language or cultural groups; (5) automation bias in reviewers; (6) data leaving the EU through an external model provider |
| Model providers in this project | Development uses only synthetic data. Free API tiers may allow the provider to use inputs to improve its products, which is acceptable for synthetic notes but not for real ones. A real deployment would need a paid or EU-hosted tier with no training on client data and a data processing agreement |
| Mitigations | (1) Verbatim quote check against the note; (2) separate "missed signal" metric, with domain 12 weighted most heavily; (3) separate "harmful over-flagging" metric and over-flag traps in the test set; (4) group-wise evaluation; (5) no scores, evidence shown next to every flag, drafts only; (6) EU-hosted model or on-premise deployment, no training on client data, no retention |
| Residual risk | Medium. Acceptable only with practitioner validation, a pilot under supervision, and ongoing monitoring of both error types |
| Status | Draft for portfolio purposes. Not reviewed by a data protection officer |

## How the evaluation supports these commitments

| Commitment | Metric |
| --- | --- |
| Do not miss serious signals | Missed signals rate, reported separately for domain 12 |
| Do not stigmatise | Harmful over-flagging rate (flags on `overflag_traps` domains) |
| Do not invent | Quote accuracy: share of flags whose quote appears verbatim in the note |
| Show what is missing | Coverage-gap agreement with expert `no_info` labels |
| Keep the person's voice | Said-vs-observed pairs detected |
| See the carer | Caregiver and young-carer flags detected as separate subjects |

## References

- [EU AI Act, Annex III](https://www.artificialintelligenceact.eu/annex/3/)
- [AI Act Service Desk: Annex III 5(a) examples](https://ai-act-service-desk.ec.europa.eu/fr/node/465)
- [European Commission: Article 50 transparency FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- [CMS: Article 50 real-world examples](https://cms.law/en/gbr/legal-updates/eu-ai-act-transparency-real-world-examples)
- [Cuatrecasas: Digital Omnibus on AI published](https://www.cuatrecasas.com/en/latam/intellectual-property/art/digital-omnibus-ai-has-been-published)
- [Presencis: AI Act Article 6](https://presencis.com/regulations/eu-ai-act/article-6/)
- [Layer3: GDPR and health data in AI](https://www.layer3labs.io/guides/gdpr-ai-health-data-compliance)
- [GDPR Local: Article 22](https://gdprlocal.com/automated-decision-making-gdpr/)
- [Dutch IT Channel: Amnesty and the childcare benefits scandal](https://www.dutchitchannel.nl/news/174184/amnesty-international-reguleer-algoritmes-na-toeslagenaffaire)
- [IBFD: lessons from the Dutch childcare allowance scandal](https://shop.ibfd.org/journal/lessons-be-learned-dutch-childcare-allowance-scandal-comparative-review-algorithmic)
