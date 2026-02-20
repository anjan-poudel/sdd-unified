# SDD Unified Day 1 Checklist

Use this checklist to get productive with `sdd-unified` in one session.

## 0. Goal

Ship your first feature using the SDD flow:

1. Requirements (`sdd-ba`)
2. L1 design (`sdd-architect`)
3. Reviews (`sdd-ba`, `sdd-pe`, `sdd-le`)
4. L2 design (`sdd-pe`)
5. L3 tasks (`sdd-le`)
6. Implementation (`sdd-coder`)
7. Code review (`sdd-le`)

---

## 1. One-Time Setup In Your App Repo

Replace `/path/to/your-app` with your actual app repo path.

```bash
cd /path/to/your-app

# Create local SDD config folder
mkdir -p .sdd_unified

# Copy framework configs from your local sdd-unified project
cp -R /Users/anjan/workspace/projects/sdd-unified/agents .sdd_unified/
cp -R /Users/anjan/workspace/projects/sdd-unified/commands .sdd_unified/
cp -R /Users/anjan/workspace/projects/sdd-unified/templates .sdd_unified/
cp -R /Users/anjan/workspace/projects/sdd-unified/orchestrator .sdd_unified/
cp -R /Users/anjan/workspace/projects/sdd-unified/spec .sdd_unified/
```

Quick verification:

```bash
ls -la .sdd_unified/agents/configs
ls -la .sdd_unified/commands/slash
ls -la .sdd_unified/templates
ls -la .sdd_unified/orchestrator
```

Expected:
- 5 agent YAML files
- slash command YAML files
- `workflow.json.template`

---

## 2. Register Agents In Claude Code

Import these files as custom agents:

- `.sdd_unified/agents/configs/sdd-ba.yaml`
- `.sdd_unified/agents/configs/sdd-architect.yaml`
- `.sdd_unified/agents/configs/sdd-pe.yaml`
- `.sdd_unified/agents/configs/sdd-le.yaml`
- `.sdd_unified/agents/configs/sdd-coder.yaml`

Verification:
- All 5 agents appear in the agent picker.

---

## 3. Create Your First Feature Workspace

```bash
cd /path/to/your-app
mkdir -p features/feature-001-auth/{spec,design,implementation/tasks,review}
cp .sdd_unified/templates/workflow.json.template features/feature-001-auth/workflow.json
cat > features/feature-001-auth/context.json << 'EOF'
{
  "feature_id": "feature-001-auth",
  "feature_name": "User Authentication",
  "current_phase": "init"
}
EOF
```

Verification:

```bash
ls -la features/feature-001-auth
```

Expected:
- `workflow.json`
- `context.json`
- `spec/`, `design/`, `implementation/tasks/`, `review/`

---

## 4. Run Day 1 Feature Flow (Manual Mode)

Run these prompts in Claude Code while switching agents:

Pair protocol for each critical step:
- Driver creates first draft artifact.
- Challenger critiques assumptions, coverage, and risks.
- Driver revises once before formal review.

1. Agent: `sdd-ba`  
   Prompt: `Define requirements for POST /login with username/password, bcrypt hashing, JWT output, and 401 on invalid credentials.`

2. Agent: `sdd-architect`  
   Prompt: `Create L1 architecture from the requirements.`

3. Agents: `sdd-ba`, `sdd-pe`, `sdd-le`  
   Prompt (each): `Review L1 architecture and return APPROVED or REJECTED_WITH_FEEDBACK.`

4. Agent: `sdd-pe`  
   Prompt: `Create L2 component design based on approved L1.`

5. Agent: `sdd-le`  
   Prompt: `Create L3 implementation tasks with BDD acceptance criteria.`

6. Agent: `sdd-coder`  
   Prompt: `Implement task-001 exactly as defined.`

7. Agent: `sdd-le`  
   Prompt: `Review task-001 implementation against BDD criteria and produce approval/rejection.`

Reference:
- [Pair + Formal Review Overlay](../2_architecture/pair_review_overlay.md)

---

## 5. Day 1 Output Checklist

You are done for Day 1 when these files exist:

```text
features/feature-001-auth/spec/requirements.md
features/feature-001-auth/design/l1_architecture.md
features/feature-001-auth/design/l2_component_design.md
features/feature-001-auth/implementation/tasks/task-001.md
features/feature-001-auth/review/review_l1_ba.json
features/feature-001-auth/review/review_l1_pe.json
features/feature-001-auth/review/review_l1_le.json
```

Optional check:

```bash
find features/feature-001-auth -maxdepth 3 -type f | sort
```

---

## 6. Known Caveat (Current State)

Use manual/supervised flow first. Full autonomous mode needs path and integration validation in this repo version.

---

## 7. Day 2 Next Step

After Day 1 works:

1. Add `/feature-status` checks to your routine.
2. Standardize review JSON schema in your app repo.
3. Automate task execution incrementally (not all-at-once).
