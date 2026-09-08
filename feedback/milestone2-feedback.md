# Milestone 2 Feedback and Revision Log

**2026 Better Scientific Software Fellowship**  
**Project:** *Sustainable AI: Best Practices for Reproducible Scientific Software Development*  
**Fellow:** Suzan Anwar, Ph.D.

## Purpose

This document records technical, mentor, collaborator, and community feedback on the Milestone 2 fellowship deliverables and tracks how that feedback is incorporated into the Best Practices Guide and tutorial materials.

The review lifecycle is tracked explicitly as:

**Prepared → Shared → Feedback Received → Revision Incorporated**

This provides clear evidence of progress without claiming that review or revision has occurred before it actually happens.

## Deliverables Under Review

- [`../guide/best-practices-guide.md`](../guide/best-practices-guide.md) — comprehensive Milestone 2 Best Practices Guide draft.
- [`../notebooks/README.md`](../notebooks/README.md) — tutorial-series overview and learning path.
- Tutorials 1–6 in [`../notebooks/`](../notebooks/).
- Tutorial 7 ReproPilot case-study notebooks in [`../notebooks/`](../notebooks/).

## Review Priorities

Reviewers are asked to focus on technical and scientific accuracy, relevance to scientific software/AI/HPC audiences, clarity and usefulness, appropriate treatment of reproducibility readiness versus successful reproduction, responsible use of AI assistance, quality of examples and exercises, missing considerations, and accessibility.

## Milestone 2 Review Lifecycle

| Reviewer / Source | Deliverable | Prepared | Shared | Feedback Received | Revision Incorporated | Evidence / Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Sameer Shende — professional mentor | Best Practices Guide and supporting ReproPilot/tutorial documentation | Yes — comprehensive draft prepared | Yes — materials shared for mentor review | Yes — 2026-09-08 | Yes — PR #34 merged | Mentor identified an undocumented Ollama prerequisite and asked whether `gemma3:1b` was required or whether other/newer models could be used. PR #34 documents Ollama setup and clarifies the reference-model/alternative-model policy. Follow-up review requested after revision. |
| Collaborator / research software practitioner | Guide and/or tutorial series | Yes — review materials prepared | Pending | Pending | Pending | Record technical/relevance review |
| Beta tester group | Tutorials 1–7 | Yes — executable drafts and testing protocol prepared | Pending | Pending | Pending | See [`tutorial-beta-testing.md`](tutorial-beta-testing.md) |

### Status Definitions

- **Prepared:** the material is complete enough to be reviewed or tested.
- **Shared:** the material has actually been sent or made available to an identified reviewer/tester with a request for feedback.
- **Feedback Received:** substantive comments, observations, or testing results have been received and documented.
- **Revision Incorporated:** actionable feedback has been addressed through a documented revision, or a reasoned decision not to change has been recorded.

## Detailed Feedback Log

| Date | Reviewer / Source | Deliverable or Section | Feedback | Planned or Completed Action | Status / Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-09-08 | Sameer Shende — professional mentor | ReproPilot grounded-AI setup and tutorial documentation | The materials used `gemma3:1b` through Ollama but assumed Ollama was already installed. Sameer recommended documenting the Ollama installation prerequisite and asked whether a newer or different model could also be used. | Added explicit optional Ollama installation and verification guidance; clarified that `gemma3:1b` is the reference model for the current prototype/benchmark rather than a universal requirement; documented that alternative Ollama-hosted models may be explored but should be recorded and separately validated because outputs may differ. | Feedback incorporated in merged PR #34: [`Incorporate mentor feedback on Ollama setup and model choice`](https://github.com/szuananwar/ai-assisted-reproducibility-bssw/pull/34). Follow-up mentor review requested. |
| TBD | Collaborator / research software practitioner | Tutorial series | Pending review | Request feedback on learning sequence, examples, and technical accuracy | Prepared |
| TBD | Beta tester(s) | Tutorials 1–7 | See [`tutorial-beta-testing.md`](tutorial-beta-testing.md) | Incorporate usability and execution feedback | Prepared |

## Revision Summary

| Revision Date | Source of Feedback | Change Made | Files / Sections Updated | Verification |
| --- | --- | --- | --- | --- |
| 2026-09-08 | Sameer Shende — professional mentor | Documented Ollama installation/verification and clarified `gemma3:1b` as the current reference model while defining cautious use of alternative Ollama-hosted models. | `examples/repropilot/README.md`; `notebooks/README.md` | Merged PR #34; follow-up mentor review requested. |

## Milestone 2 Completion Criterion

For Milestone 2, the review record should demonstrate the complete initial feedback lifecycle:

**Prepared → Shared → Feedback Received → Revision Incorporated**

At minimum, the Best Practices Guide should have documented technical/mentor or collaborator review, and actionable initial feedback should be considered and incorporated where warranted. Tutorial-specific usability and execution evidence is tracked separately in [`tutorial-beta-testing.md`](tutorial-beta-testing.md).

This document is a living record and will continue to be updated during Milestone 3 revisions.