I want to use sdd-unified to create a new framework `ai-sdd`.
extract the framework from the current sdd-unified repo with below requirements and considerations.

- ensure the core/base if extensible and flexible  to allow overlaying strategies and workflows.
- besides the core, everything else is overlay - code review, pair programming, confidence scoring and automation etc.
- AI Agent Roles and responsibilities are externalised to yaml config files, instead hardcoded BA,PE,LE etc in current project.
- default agents will be provided ( BA, PE, DEV, etc) - they can be used or clients can plugin their own agents ( roles/modes/persona)
- Clients can provide yaml files for agents that define roles and responsibilities
- Agents should be extensible ( LLM should be able to load  the extended agents - which again are overlays on top of existing agents -everyting can be viewed from overlay perspective)
- Workflow should be defined in yaml file that dictates what agents interact with which agents and how  handover is done, and loops and loop break conditions
- Later workflow sdk will be provided in phase two for programmatic workflow definitions along with yaml based.

The core of the engine will provide the following
- constitutions - recursive support for defining, extending and overriding project/folder's  steers (purpose/background, overview, rules and standards etc) in submodule/subfolder
- thin core layer for AI workflow orchestration
- Agents can be configured to use any LLM. And allow tuning hyperparameter along with llm
- uses existing frameworks or AI coding agent ( claudeCode/Codex/Gemini/Etc) to create plans and breakdown tasks.
- Rules and guidelines for plan and task breakdown etc will be provided as part of constitution (sys prompt level)
- provide tools for calculating evaluation metrics from evidence to compute confidence score ( confidence = f([]EvalMetric) -> decimal ). Note: use raw eval scores if this adds too much complexity, ask to choose option

Overlays:
general
- All agents should support configurable llm and hyper params
- All loops will have MAX_ITERATION config prop to control when loop should exit if no progress made or slow progress between the pairs - use sensible default.
- All loops must have exit conditions besides MAX_ITERATION.

loops and tasks
- confidence level loop: if confidence score is above X% (configurable), auto transition/proceed to next task in the workflow ( i.e paired workflow loop)
- Paired workflow  loop: support for - Pair programming style - Paired workflow,loop continuing until either confidence score is above X% (configurable) or reviewer pair signal ok to proceed. e.g PO & BA pair, 2 devs pair ( pair programming) etc
  In this setting pairs switch roles once the driver has implemented a portion and is ok to proceed - or the switch can be at subtask level ( configurable)
- agentic review loop :  similar to paired workflow, except the roles don't switch and coder should follow some code review guideline to ensure the PR raised meets PR quality metrics and requirements.
  e.g PR code review loop , design review loop etc.
- confidence scoring and automatic transition to next subtask/task or feature ( based on configured sequence in workflow definition).
- agent handovers.
- Human in the loop : when some task is marked as requiring Human to approve, or there's some deadlock or infinite loop  in some loops and need human to make next step judgement calls.


Principles of flexibility:
Most things are configurable
- confidence scoring is turned off by default.
- paired workflow is turned off by default.
- agentic review is turned off by default.
- any llm can be used for any persona/role
- hIL is turned on by default - in case some task do require manual HIL.

These knobs and dials can be turned on and off and values tweaked to get different LLM inference behavior.
Initially all loops can be turned on and only turned off or thresholds tweaked if it causes high latency, making it not very usable.
The more loops are enables, it will be costlier and slower to generate output.
Same goes with certain thresholds, they can be lowered to speed things up.. 

