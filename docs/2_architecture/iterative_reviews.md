# Iterative Reviews

## Purpose

Make reviews actionable by connecting rejection outcomes to explicit rework loops.

## Review Outcomes

- `APPROVED`: advance workflow
- `REJECTED_WITH_FEEDBACK`: trigger mapped rework task

## Required Review Output

Each review artifact should include:

- decision status
- concrete findings
- required rework actions
- next-step task

## Gate Policy

Use evidence-based GO/NO-GO decisions:

1. requirement coverage exists
2. acceptance criteria are testable
3. validation evidence attached (tests/checks)
4. for higher risk: security + rollout evidence

## Rework Controls

- mapped rework task per review type
- max iteration limit per phase
- escalation to human reviewer on limit breach

## Independence Rule

In pair mode, formal reviewers must be independent from the producing pair.

## Related

- `workflow_engine.md`
- `pair_review_overlay.md`

Full historical version: `../archive/non_core/2_architecture/iterative_reviews-full.md`
