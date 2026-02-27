# Task 02: Agent and Workflow Configuration (YAML)

## Description
Externalize the definition of Agent Roles and Workflows into highly configurable YAML files. This task involves designing the schemas for both and implementing the loaders necessary to instantiate them at runtime.

## Requirements
- **Agent YAML Schema:** Define properties for roles, responsibilities, default LLMs, hyperparameter overrides (e.g., temperature, max tokens), and system prompts.
- **Agent Overlay Support:** Allow an agent definition to "extend" or act as an overlay on a base agent (e.g., `role: Senior Developer`, `extends: Base Developer`).
- **Workflow YAML Schema:** Define nodes (agents), edges (transitions), handovers, loops, and conditions for breaking loops.
- **Default Implementations:** Provide robust default YAML configurations for standard roles (BA, PE, DEV, Reviewer) and a basic workflow template.

## Acceptance Criteria
- [ ] YAML schemas for Agents and Workflows are documented and validated.
- [ ] The engine correctly parses the YAML and instantiates the defined agents with correct hyperparameter/LLM bindings.
- [ ] Extended agents successfully inherit and override properties from their base agents.
- [ ] The orchestrator uses a loaded YAML workflow definition to guide execution.