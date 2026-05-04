# OpenVINO Agent Usage Guide

This guide explains how to use the agent-related files in this repository to work effectively with AI agents (such as Jules or Claude). These files are designed to automate complex workflows and ensure that AI-generated contributions meet OpenVINO's quality standards.

## Overview

OpenVINO uses three main types of files to guide AI agents:
1.  **Skills (`.claude/skills/`):** Task-oriented workflows for complex operations like debugging.
2.  **`AGENTS.md`:** Local context, coding standards, and checklists for specific subprojects.
3.  **`AI_USAGE_POLICY.md`:** High-level principles for responsible AI usage.

---

## 1. Skills (Task-Oriented Workflows)

Skills are located in `.claude/skills/` (or `.agents/skills/`). They define a step-by-step process for the agent to follow when a specific task is identified.

### How to use them
You don't usually need to "run" a skill manually. Instead, you can describe a problem that matches a skill's description, and the agent will automatically trigger the corresponding workflow.

**Example: Debugging a MatcherPass**
If you tell the agent: *"This transformation is not being applied to my model,"* the agent will:
1.  Identify that the `debug-matcher-pass` skill is relevant.
2.  Follow the workflow: Gather prerequisites -> Verify debug build -> Collect logs -> Analyze logs -> Create a reproducer test.
3.  Provide a standardized **Diagnosis Report**.

### Creating or modifying Skills
If you want to teach the agent a new recurring task, you can create a new `SKILL.md` file following this structure:
- **YAML Frontmatter:** Define the `name` and a `description` that helps the agent know when to trigger it.
- **Goal:** State the expected deliverables.
- **Steps:** Provide clear, numbered instructions and bash commands.
- **Templates:** Include standardized formats for reports or test cases.

---

## 2. `AGENTS.md` (Contextual Guidelines)

`AGENTS.md` files provide location-specific instructions. They are often found in the root of the repository or in major subdirectories (e.g., `src/plugins/intel_cpu/thirdparty/kleidiai/AGENTS.md`).

### How they are used
The agent is instructed to read all `AGENTS.md` files that are in the path of any file it modifies. For example, if the agent edits a file in `thirdparty/kleidiai/`, it MUST obey the instructions in `thirdparty/kleidiai/AGENTS.md`.

### What to include in an `AGENTS.md`
- **Key Layout:** Map of important files and directories.
- **Build & Run:** Commands specific to that subproject.
- **Review Checklist:** Specific requirements for PRs (e.g., "Always include Signed-off-by", "Update copyright notices").
- **Coding Conventions:** Preferences like "Use the term *micro-kernel* instead of *kernel*".

---

## 3. AI Usage Policy

Before using an AI agent to contribute to OpenVINO, please read [AI_USAGE_POLICY.md](../AI_USAGE_POLICY.md).

**Key Responsibilities:**
- **Verification:** You (the human) are responsible for verifying every line of code.
- **Disclosure:** Significant AI assistance must be disclosed in the Pull Request description.
- **Understanding:** You must be able to explain the design decisions made by the AI.

---

## Summary: How to "Teach" the Agent

To improve the agent's performance on your specific tasks:
1.  **For recurring workflows:** Add a new skill in `.claude/skills/`.
2.  **For project-specific rules:** Add or update `AGENTS.md` in the relevant directory.
3.  **For one-off instructions:** Simply provide them in your chat prompt.

By leveraging these files, you ensure that the AI agent acts as a specialized OpenVINO engineer rather than a general-purpose coding assistant.
