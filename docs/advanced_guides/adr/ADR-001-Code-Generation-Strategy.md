# ADR-001: Choice of Templating Engine for Code Generation

**Date:** 2025-10-06
**Status:** Proposed

## Context

The SDD framework's `spec-derive` command requires a templating engine to transform a structured `spec.yaml` file into source code. The `ENHANCEMENT_STRATEGY.md` initially proposed using `Jsonnet` for this purpose. This decision has been challenged, with the valid suggestion that a general-purpose language like TypeScript could also perform this task. This ADR provides a first-principles analysis to make a final, reasoned decision.

## Decision Drivers

*   **Safety & Security:** The templating engine will be a core part of the framework's runtime. It must be sandboxed and guaranteed not to have unintended side effects (e.g., no filesystem or network access).
*   **Declarative Nature:** For data transformation, a declarative approach (defining *what* you want) is often more maintainable and easier to reason about than an imperative one (defining *how* to get it).
*   **Maintainability of Templates:** The templates will be complex and will evolve. They must be easy to read and manage.
*   **Developer Experience:** The learning curve and familiarity of the tool for end-users who may wish to write their own templates.

## Considered Options

### Option 1: `Jsonnet`

A declarative, data templating language that is a superset of JSON. It is designed specifically for managing and generating structured data.

*   **Pros:**
    *   **Fundamentally Safe (Pro):** `Jsonnet` is **hermetic**. It is a pure data transformation language with no access to the filesystem, network, or environment variables. This is its most critical feature from a framework security perspective. We can execute any `Jsonnet` template with absolute confidence that it has no side effects.
    *   **Declarative (Pro):** Its design forces a declarative style that is exceptionally well-suited for transforming one data structure into another. This leads to high signal-to-noise ratio in templates.
    *   **Designed for Configuration (Pro):** It has powerful features for composition, inheritance, and abstraction that are specifically built for managing complex data, which is exactly what a `spec.yaml` is.

*   **Cons:**
    *   **Niche Language (Con):** It is not a mainstream language. This imposes a learning curve on developers who want to create or modify templates, negatively impacting Developer Experience.

### Option 2: TypeScript (as a representative general-purpose language)

Using a standard programming language like TypeScript to write scripts that perform the code generation.

*   **Pros:**
    *   **Extremely Familiar (Pro):** Most developers will be familiar with TypeScript or a similar language. The learning curve is zero for most of the target audience.
    *   **Powerful and Flexible (Pro):** As a Turing-complete language, it can perform any logic imaginable. It has a vast ecosystem of libraries that could be leveraged.

*   **Cons:**
    *   **Fundamentally Unsafe (Con):** A TypeScript script, when executed via Node.js, has full access to the underlying system. It can read arbitrary files, make network calls, and execute shell commands. To use it safely within our framework would require building a complex and likely imperfect sandbox, significantly increasing the framework's internal complexity. Using it without a sandbox is an unacceptable security risk for a general-purpose tool.
    *   **Imperative Overhead (Con):** Writing a data transformation in TypeScript requires imperative boilerplate: setting up file reads, parsing YAML, building strings manually or with a sub-templating library, and writing the output. This can obscure the core transformation logic.

## The Decision

Based on this first-principles analysis, **Option 1: `Jsonnet`** is the correct choice **for the core, built-in templating engine of the framework.**

**Justification:** The principle of **Safety** is non-negotiable for a framework component. `Jsonnet`'s hermetic, sandboxed nature is a fundamental feature that aligns perfectly with this requirement. While TypeScript is more familiar, its lack of inherent safety makes it an inappropriate choice for a core, built-in templating mechanism that needs to be trusted by default. The declarative nature of `Jsonnet` is also a better fit for the specific problem of data transformation.

We are choosing to prioritize the long-term safety and maintainability of the framework over the short-term familiarity for developers. The learning curve of `Jsonnet` is a one-time cost, while the security risks and imperative complexity of using TypeScript would be a permanent architectural burden.

### Acknowledging the User's Point: A Hybrid Strategy

The user's point about familiarity and the power of general-purpose languages is still valid. To honor this, we can adopt a hybrid strategy:

1.  **Default to `Jsonnet`:** The default, built-in templates provided with the framework will use `Jsonnet`. This is our "safe mode."
2.  **Allow Custom Generator Scripts:** The `spec-derive` command can be enhanced with an optional `--custom_generator` flag. This flag would point to an executable script (e.g., `my_ts_generator.ts`). The framework would then simply shell out to this script, passing the `spec.yaml` path as an argument.

This approach provides a safe, robust default while giving advanced users the escape hatch to use any tool they wish, placing the responsibility for the safety of that custom script on them.

I will now update the `ENHANCEMENT_ROADMAP.md` to reflect this nuanced decision.