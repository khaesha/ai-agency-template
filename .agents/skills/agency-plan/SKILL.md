---
name: agency-plan
description: Scope a single ticket or task, turn a feature brief or existing plan into a backlog, or prepare a selected PLAN with observable acceptance criteria, owners, and dependencies.
---

# Plan an agency work item

Read the available sources and relevant repository instructions. Use the requested phase and return the matching format from `agency/templates/`.

For a direct ticket or selected PLAN, apply the security audit triggers in `agency/WORKFLOW.md`. When an audit applies, include the reason, review scope, and any observable security requirements in the brief so QA can plan checks before implementation.

## Direct ticket

1. Summarize the intended change and source. Inspect established behavior and conventions in the affected code and tests. Record assumptions that can be reversed and decisions that genuinely need an answer.
2. Write observable acceptance criteria with IDs such as `AC-01`. Describe normal and error cases where relevant. Give each criterion a source or assumption.
3. Assign one implementation owner where possible. List short ordered steps in the ticket for work that needs multiple owners. Use acceptance criteria and a test plan to prepare the ticket for execution.

## Backlog or PLAN breakdown

1. For a backlog, group changes into independently reviewable outcomes, with source references, dependencies, and a quick description of how to review each outcome. Reuse relevant work from any existing plan.
2. For a selected PLAN, write acceptance criteria and scope small implementation tasks with one owner each, AC references, writable areas, checks, and dependencies. Identify a single owner for each shared file.
3. Record relevant contracts, including interfaces, errors, access, or compatibility. Identify conflicts or gaps that change the work materially and show which PLAN or task they affect.
