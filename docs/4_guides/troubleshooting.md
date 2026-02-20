# Troubleshooting

## Common Issues

1. Agents not visible: verify `.sdd_unified/agents/configs/*.yaml` is imported.
2. `/feature` fails: ensure `.sdd_unified/orchestrator/main.py` exists in the target project.
3. `/feature-status` fails: ensure `.sdd_unified/orchestrator/status.py` exists in the target project.
4. Workflow stuck: inspect task dependencies and statuses in `workflow.json`.
5. Missing handoff context: verify `context.json` is present and updated after each phase.
