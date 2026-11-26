---
name: agency-orchestrate
description: Coordinate an AI Agency run when asked to prepare or execute a ticket, task, or feature backlog, resume saved work, report progress, or handle a human preview decision.
---

# Orchestrate an agency run

1. Read `agency/WORKFLOW.md` for the procedure, `agency/PROJECT.md` for optional defaults, and the run record if one exists. Identify the requested action before making changes.
2. Apply the run's source and mode choices. Use `agency-plan` for direct ticket intake, backlog creation, or PLAN breakdown. Give the Planner the sources and context it needs, or perform small direct intake in the main session.
3. Use `agency-verify` with QA before implementation. Save acceptance criteria, the test plan, any shared contract, and the planned security audit scope when applicable. For a plan-only request, stop at the relevant planning deliverable.
4. Dispatch ready implementation work to Backend or Frontend as applicable, then ask QA to verify the actual result. Apply the workflow's pre-preview security audit routing. Read the role instructions in `agency/roles/` when passing a brief to a generic subagent or working in a single session.
5. Keep the run records in English. Create a versioned preview once checks are satisfied. Stop at the human decision and report the run ID, ticket or PLAN ID, revision, and review steps. Follow the workflow when handling approval, hold, or revision.
