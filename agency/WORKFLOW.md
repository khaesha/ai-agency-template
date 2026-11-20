# AI Agency workflow

## Actions

These are natural-language instructions to the assistant. Start by reading `agency/PROJECT.md` and checking whether the run already exists.

| Action | Orchestrator behavior |
| --- | --- |
| `Plan <run-id>` | In direct mode, prepare the ticket record with acceptance criteria and a test plan. In backlog mode, prepare the backlog. Stop before implementation. |
| `Run <run-id> [PLAN-ID]` | Open or initialize the run. Execute the direct ticket or one eligible PLAN through preview. Continue the active PLAN first if there is one. |
| `Resume <run-id>` | Read the saved state. Continue active work when possible. If a decision is pending, show the preview. If only prepared work is queued, report what is ready. |
| `Status <run-id>` | Report state, the next eligible item, blockers, or the pending preview. Read only. |
| `Approve / Request changes / Hold <run-id> <item-id> <revision>` | Apply the explicit decision to the current preview using the rules below. |

Use a run ID made of lowercase letters, digits, and hyphens. Choose a clear ID if the user supplies a new scope and requests work without naming a run. Ask for identification if several existing runs match or a supplied ID already belongs to different work. Treat a repeat request for the same scope as a continuation. An explicit plan-and-run request authorizes both actions.

If the item is `AWAITING_HUMAN`, route it through the preview decision before resuming execution or selecting another item. A direct run ends at `APPROVED`. Report an unknown or ineligible requested PLAN and its blocker before selecting any other work.

## 1. Intake

1. Read the current request, project instructions, and available inputs. Apply per-run overrides to `agency/PROJECT.md`. Ignore blank or `N/A` values. For a continuing run, use its recorded mode, sources, and decisions unless the user explicitly revises the scope. A ticket, task text, external link, or existing plan can be the only input. Find the relevant code and tests for implementation context when available.
2. Record source references and the scope in English. Preserve original quotes and source material. If a tracker link is unavailable, use an equivalent description supplied by the user or ask for the missing text when necessary. For an incomplete ticket, use the repository for established conventions and current behavior. Record reversible assumptions. Ask a focused question only when unresolved ambiguity materially affects scope, expected behavior, a contract, compatibility, or a required check. Mark the affected item `BLOCKED` and proceed with independent in-scope work where possible.
3. Respect an explicit `direct` or `backlog` selection. In `auto`, choose direct for one reviewable outcome, even when it touches multiple code areas. Choose backlog for several independently reviewable outcomes. If the user supplies an existing plan, reuse its requirements, tasks, and dependencies where applicable. Derive missing criteria or checks from the input and repo evidence.
4. Have the Planner use `agency-plan` to prepare the chosen format. For a small direct ticket, the Orchestrator can do this step using the same skill. Write the record using the matching template in `agency/templates/`.

| Mode | Run record under `agency/runs/<run-id>/` | Review item ID |
| --- | --- | --- |
| Direct | `TICKET.md` holds scope, status, criteria, checks, implementation, and QA. Add steps inside that record if several owners are needed. | `TICKET`. Keep the external ticket ID in the source field. |
| Backlog | `BACKLOG.md` lists PLANs in order, with their dependencies. Create `plans/PLAN-001.md` and `tasks/PLAN-001-T01.md` when preparing a selected PLAN. | A stable ID such as `PLAN-001`. |

The Orchestrator owns run documents. Preserve existing IDs, history, and verified results when updating queued scope. For an active item with a revised scope, update the work record, revisit affected criteria and checks, and invalidate stale evidence before rerunning.

## 2. Prepare one review item

- For backlog runs, select the named or first eligible PLAN. Dependencies must be `APPROVED` and scope blockers resolved. Record it as the active PLAN. Prepare its scope, acceptance criteria (AC), and implementation tasks with one owner per task. Use stable task IDs within a PLAN and stable AC IDs within each review item.
- For direct runs, use the ticket as the implementation brief when one owner can complete it. For work spanning layers, assign ordered steps inside `TICKET.md`.
- For shared files or contracts, identify one owner per file and settle the relevant interface, errors, access rules, and compatibility before dispatching dependent work.
- Save the scope and criteria, then have QA use `agency-verify` to prepare a test plan before implementation. Map each AC to an expected result, a repeatable check, and any setup or fixture it needs. Mark checks required or optional. Reuse a prepared test plan when the relevant scope and setup still match. For a direct `Plan` request, stop here with the item `QUEUED` if ready.
- When execution begins, keep a baseline of the affected code and any existing local changes before editing. A Git HEAD and a description of relevant local edits work for a Git repo. Otherwise, use the relevant file state. Set the review item to `IN_PROGRESS`.

## 3. Implement and verify

1. Give each implementation role the ticket or task path, scope, writable areas, applicable criteria, contracts, and checks. For direct work with one owner, pass `TICKET.md` as the brief. Run sequentially by default. Parallel work requires satisfied dependencies, disjoint write scopes, and a workspace that supports it.
2. Inspect the changes and route QA against the criteria and actual workspace state. Record commands or reproduction steps and observed results. For several tasks, verify the integrated outcome and reuse current task evidence when it covers the same behavior.
3. Send failures and regressions back to the assigned owner, then rerun the affected checks. If a required check cannot run, try a check that provides equivalent evidence. Record the gap as a blocker if required evidence is still missing. Report optional gaps in the preview.
4. Create a preview once each required AC has adequate evidence and, in backlog mode, all implementation tasks are `VERIFIED`.

Use named specialists when configured and supported. Otherwise, give a generic subagent the corresponding file from `agency/roles/` and the task brief. If delegation is unavailable, perform the roles sequentially in the main session and record `single-session QA`. For chat without workspace access, provide draft changes or review steps and request the needed execution evidence. Mark checks as `NOT_RUN` until there is an actual result.

## 4. Preview and human decision

1. Save `previews/<item-id>-r01.md` and increment the revision for each replacement preview. Include changes, links to evidence, review steps, and a reference to the verified result. Use a commit that covers the reviewed content, or hashes of relevant files, including new files and markers for deletions. Record the versions or snapshots of relevant input, contracts, and criteria.
2. Set the current item to `AWAITING_HUMAN`, link the preview from the run record, and end execution. Report the run ID, item ID, revision, and how to review it.
3. Accept an explicit decision for the current preview. Use implied IDs only if the reply clearly identifies one pending preview. If the user gives an older revision, show the current one and wait for a decision. Before approval, confirm that the relevant verified result and scope still match. If either changed, reverify the affected work and produce a new revision for review.
4. Record the decision in the preview and update the run record. If a decision was already applied, confirm the recorded state without duplicating it. Preserve past previews.

| Decision | Result |
| --- | --- |
| `APPROVE` | Set the item to `APPROVED`. For a backlog run, clear the active PLAN. Continue to another PLAN only when the user also asks to run it. Merging, deployment, and publication require their own instructions. |
| `REQUEST CHANGES` | Record the feedback and return the same item to `IN_PROGRESS`. Update affected criteria or steps, reimplement as needed, and rerun QA. Pause affected work if a material scope decision remains unresolved. Issue a new preview revision. |
| `HOLD` | Record the hold and keep the item at `AWAITING_HUMAN` with the same preview. |

## State and recovery

- The source of truth is the status field in `TICKET.md` for direct runs and the PLAN row in `BACKLOG.md` for backlog runs. Review states are `QUEUED`, `IN_PROGRESS`, `BLOCKED`, `AWAITING_HUMAN`, and `APPROVED`. Keep at most one active PLAN per run. A PLAN blocked before selection can return to `QUEUED` once unblocked. A blocked active item resumes at its last incomplete stage.
- For separate backlog task files, use `READY`, `IN_PROGRESS`, `CHANGES_REQUESTED`, `BLOCKED`, and `VERIFIED`. Schedule dependent tasks after prerequisite work is verified or the prerequisite is demonstrated available. Keep dependencies acyclic.
- Write status, evidence, and decisions as they become available. On resume, check the records against the workspace. Preserve unrelated edits and completed in-scope work. Recover missing state from evidence where possible. Explicit user decisions are the basis for an approved state.
- Use one active Orchestrator session per run. Use separate checkouts or schedule overlapping work sequentially when multiple runs edit the same code.
