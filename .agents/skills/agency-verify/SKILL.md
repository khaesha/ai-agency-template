---
name: agency-verify
description: Prepare a test plan for an agency ticket or PLAN before implementation, then verify actual changes against its acceptance criteria with repeatable evidence.
---

# Verify an agency work item

Read the ticket or PLAN, applicable task files, relevant contracts, and repository checks. Use the phase in the brief.

## Plan tests before implementation

Map each acceptance criterion to a scenario, setup or fixture where needed, expected result, and method. Mark required and optional checks. Consider negative cases, regressions, and cross-layer behavior when relevant. Identify any unresolved input or unavailable environment that would prevent required verification.

## Verify implementation

1. Inspect the actual changes and exercise the normal entry point where practical. Run targeted checks and give the command or reproduction steps and the observed result. For integrated verification, use fresh checks or existing evidence that still applies.
2. Record `PASS`, `FAIL`, `NOT_RUN`, or `N/A` for each scenario. Give reasons for `NOT_RUN` and `N/A`. Cover each required criterion with at least one applicable scenario.
3. Report `PASS` when required evidence is sufficient, `FAIL` for an unmet criterion or reproduced regression, and `BLOCKED` for missing required evidence. Report optional gaps separately.
