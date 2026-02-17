# SDD Unified Documentation Index

**Complete guide to finding what you need in the sdd_unified framework documentation.**

## Quick Navigation

### 🚀 New Users
- [Quick Start Guide](1_getting_started/quick_start.md) - Get running in 5 minutes
- [Architecture Overview](2_architecture/overview.md) - Understand what sdd_unified is
- [Claude Code Integration](3_integration/claude_code.md) - Installation and setup

### 📚 Learning the Framework
- [Workflow Engine](2_architecture/workflow_engine.md) - How DAG execution works
- [Task-Driven Implementation](2_architecture/task_driven_implementation.md) - BDD task system
- [Iterative Reviews](2_architecture/iterative_reviews.md) - Review/rework cycles
- [Context Management](2_architecture/context_management.md) - Agent handover system

### 🔧 Using the Framework
- [Feature Development Workflow](1_getting_started/feature_development_workflow.md) - Step-by-step guide
- [Agent Roles](4_guides/agent_roles.md) - Understanding each agent's responsibility
- [Best Practices](4_guides/best_practices.md) - Tips and patterns

### 📊 Reference & Analysis
- [Framework Assessment](6_analysis/framework_assessment.md) - Honest evaluation
- [Competitive Analysis](6_analysis/competitive_analysis.md) - vs other frameworks
- [Context Schema Reference](5_reference/context_schema.md) - Technical specs

---

## Documentation Structure

### 1. Getting Started
**For new users who want to get up and running quickly**

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [Quick Start](1_getting_started/quick_start.md) | Install and run first feature | 5 min |
| [Feature Development Workflow](1_getting_started/feature_development_workflow.md) | End-to-end walkthrough | 15 min |
| [Installation Guide](1_getting_started/installation.md) | Detailed setup | 10 min |

**Start here if:** You're new to sdd_unified

---

### 2. Architecture
**For understanding how the framework works internally**

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [Overview](2_architecture/overview.md) | High-level architecture | 20 min |
| [Workflow Engine](2_architecture/workflow_engine.md) | DAG execution model | 25 min |
| [Task-Driven Implementation](2_architecture/task_driven_implementation.md) | BDD task system | 30 min |
| [Iterative Reviews](2_architecture/iterative_reviews.md) | Review/rework cycles | 30 min |
| [Context Management](2_architecture/context_management.md) | Agent handover | 25 min |

**Start here if:** You want to understand the design decisions

---

### 3. Integration
**For integrating with Claude Code, Roo Code, or other tools**

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [Claude Code Integration](3_integration/claude_code.md) | Setup and usage | 20 min |
| [Roo Code Integration](3_integration/roo_code.md) | Alternative tool | 15 min |
| [Integration Architecture](3_integration/architecture.md) | How integration works | 15 min |

**Start here if:** You're setting up the framework with your agentic tool

---

### 4. User Guides
**For practical guidance on using the framework**

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [Feature Development](4_guides/feature_development.md) | Complete workflow example | 20 min |
| [Agent Roles](4_guides/agent_roles.md) | Each agent's responsibility | 15 min |
| [Best Practices](4_guides/best_practices.md) | Tips and patterns | 15 min |
| [Troubleshooting](4_guides/troubleshooting.md) | Common issues | 10 min |
| [Playbook](4_guides/playbook.md) | Operational guide | 20 min |

**Start here if:** You're actively developing features

---

### 5. Reference
**For looking up technical specifications**

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [Context Schema](5_reference/context_schema.md) | context.json specification | 10 min |
| [Workflow Schema](5_reference/workflow_schema.md) | workflow.json specification | 10 min |
| [Command Templates](5_reference/command_templates.md) | YAML command format | 10 min |
| [ADR Index](5_reference/adr/index.md) | Architecture decision records | 5 min |

**Start here if:** You need technical specs

---

### 6. Analysis & Assessment
**For understanding framework evaluation and positioning**

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [Framework Assessment](6_analysis/framework_assessment.md) | Comprehensive evaluation | 30 min |
| [Competitive Analysis](6_analysis/competitive_analysis.md) | vs other frameworks | 25 min |
| [Enhancement Proposal](6_analysis/enhancement_proposal.md) | Future improvements | 15 min |
| [Architecture Correction](6_analysis/architecture_correction.md) | Design evolution | 10 min |

**Start here if:** You're evaluating the framework or understanding its position

---

## By Use Case

### "I want to create my first feature"
1. [Quick Start](1_getting_started/quick_start.md)
2. [Feature Development Workflow](1_getting_started/feature_development_workflow.md)
3. [Claude Code Integration](3_integration/claude_code.md)

### "I need to understand the architecture"
1. [Architecture Overview](2_architecture/overview.md)
2. [Workflow Engine](2_architecture/workflow_engine.md)
3. [Framework Assessment](6_analysis/framework_assessment.md)

### "I'm evaluating sdd_unified vs alternatives"
1. [Framework Assessment](6_analysis/framework_assessment.md)
2. [Competitive Analysis](6_analysis/competitive_analysis.md)
3. [Architecture Overview](2_architecture/overview.md)

### "I'm having problems"
1. [Troubleshooting](4_guides/troubleshooting.md)
2. [Claude Code Integration](3_integration/claude_code.md)
3. [Best Practices](4_guides/best_practices.md)

### "I want to understand reviews and iteration"
1. [Iterative Reviews](2_architecture/iterative_reviews.md)
2. [Circuit Breakers](2_architecture/iterative_reviews.md#circuit-breaker-pattern)
3. [Best Practices](4_guides/best_practices.md)

### "I need the technical specs"
1. [Context Schema](5_reference/context_schema.md)
2. [Workflow Schema](5_reference/workflow_schema.md)
3. [Command Templates](5_reference/command_templates.md)

---

## By Role

### Framework Users (Developers)
- [Quick Start](1_getting_started/quick_start.md)
- [Feature Development](4_guides/feature_development.md)
- [Agent Roles](4_guides/agent_roles.md)

### Framework Evaluators (Technical Leaders)
- [Framework Assessment](6_analysis/framework_assessment.md)
- [Architecture Overview](2_architecture/overview.md)
- [Competitive Analysis](6_analysis/competitive_analysis.md)

### Framework Integrators (DevOps/Platform Engineers)
- [Claude Code Integration](3_integration/claude_code.md)
- [Integration Architecture](3_integration/architecture.md)
- [Troubleshooting](4_guides/troubleshooting.md)

### Framework Contributors (Developers)
- [Architecture docs](2_architecture/)
- [ADR Index](5_reference/adr/index.md)
- [Enhancement Proposal](6_analysis/enhancement_proposal.md)

---

## Document Status

| Status | Meaning | Documents |
|--------|---------|-----------|
| ✅ Complete | Fully written, reviewed | Most docs |
| 🚧 In Progress | Partially complete | Some guides |
| 📝 Planned | Not yet started | Advanced topics |

### Complete (✅)
- All architecture documents
- Framework assessment
- Competitive analysis
- Quick start guide
- Integration guides

### In Progress (🚧)
- Feature development workflow
- Agent roles guide
- Troubleshooting guide

### Planned (📝)
- Advanced customization
- Performance tuning
- Multi-cloud deployment

---

## Contributing to Documentation

Found an error? Want to improve a doc?

1. Check the document status above
2. Read the document you want to improve
3. Make your changes
4. Submit for review

**Documentation standards:**
- Clear, concise language
- Real examples
- Honest about limitations
- Linked cross-references

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-16 | Initial organized documentation structure |

---

## Quick Links

### Essential Documents
- [README](../README.md) - Project overview
- [Architecture Overview](2_architecture/overview.md) - What is sdd_unified
- [Quick Start](1_getting_started/quick_start.md) - Get started fast
- [Framework Assessment](6_analysis/framework_assessment.md) - Honest evaluation

### Configuration Files
- `agents/configs/` - Agent definitions
- `commands/` - Command templates
- `templates/workflow.json.template` - Workflow DAG

### Examples
- `use_cases/examples/` - Complete feature examples
- [Feature Development](4_guides/feature_development.md) - Walkthrough

---

## Need Help?

**Can't find what you're looking for?**

1. Check this index for the right section
2. Use the "By Use Case" navigation above
3. Search for keywords in the relevant section
4. Check the troubleshooting guide

**Still stuck?**
- Review the [Framework Assessment](6_analysis/framework_assessment.md) for known limitations
- Check [Claude Code Integration](3_integration/claude_code.md) for setup issues
- See the [Enhancement Proposal](6_analysis/enhancement_proposal.md) for planned features

---

**Last Updated:** 2025-10-16  
**Documentation Version:** 1.0.0  
**Framework Version:** 1.0.0-alpha