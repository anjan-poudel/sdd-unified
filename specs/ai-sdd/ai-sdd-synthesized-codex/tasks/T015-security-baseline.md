# T015 Security Baseline

## Objective
Add baseline runtime controls for prompt/output safety and secret hygiene.

## Deliverables
- Secret redaction in logs/artifacts
- Prompt/output sanitization pipeline
- Policy checks for restricted data egress
- Security-focused test fixtures

## Done When
- Sensitive tokens are never emitted in logs.
- Known prompt-injection fixtures are blocked or quarantined.
