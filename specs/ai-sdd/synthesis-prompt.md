compare the plans created bydifferent models  under @specs/ai-sdd/ai-sdd-<AI_CODING_TOOL> folder, to create a sdd framework for AI driven development. 
then extract the best from the plans from different models intoai-sdd-synthesized-<CURRENT_AI_CODING_TOOL> folder. 
identify gaps in the implementations and if any found,propose solutions to address those gaps. 

note:
from gemini synthesis prompt output
```
 Execution Model & Overlays (Codex): Integrated the strict, safety-first execution order for overlays: Human-in-the-Loop (HIL) -> Evidence Policy Gate -> Agentic Review -> Paired Workflow -> Confidence Loop
     -> Agent Execution. Crucially, incorporated the rule that "confidence never promotes by itself" and T2 routing requires human sign-off.

```