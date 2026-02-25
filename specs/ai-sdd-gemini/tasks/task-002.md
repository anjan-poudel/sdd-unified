# Task 002: YAML Configuration Systems

## Objective
Externalize Agent roles and Workflow definitions into human-readable YAML configurations.

## Requirements
1. **Agent YAML Schema**:
   - Must support properties for: `name`, `description`, `llm_provider`, `llm_model`, `hyperparameters` (temperature, max_tokens, etc.).
   - Must support an `extends: <agent_name>` property to allow overlays and inheritance.
2. **Workflow YAML Schema**:
   - Must support defining tasks, assigning an agent to a task, and mapping task dependencies (inputs/outputs).
   - Must support configuring loops, thresholds, and handovers.
3. **Loaders**:
   - Implement a parser that validates and instantiates these YAML files into the core objects required by Task 001.
4. **Default Content**:
   - Provide default YAML configurations for BA, PE, DEV, Architect, and Reviewer.

## Acceptance Criteria
- Engine successfully parses and executes a workflow entirely defined in YAML.
- Custom agent YAML successfully overrides the `llm_model` and `temperature` of a base agent using the `extends` keyword.
