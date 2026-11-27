# Project defaults

Edit this file as needed. Every entry is optional. Leave a value blank or set it to `N/A` when it does not apply. Give run-specific overrides in the prompt.

| Setting | Default |
| --- | --- |
| Intake mode | `auto` (`direct` for one reviewable item, `backlog` for several) |
| Ticket, task, or existing plan | |
| Product requirements or feature brief | |
| Architecture or technical constraints | |
| Other sources, such as designs or API contracts | |
| Backend paths and related tests | |
| Frontend paths and related tests | |
| DevOps paths and related checks | |
| Shared code, configuration, or schemas | |
| Local setup and runtime commands | |
| Test, lint, type-check, or integration commands | |
| Preview steps and test fixtures | |
| Project conventions and compatibility constraints | |

Use repository-relative paths, accessible paths outside the repository, links, tracker IDs, or short notes. Add optional context as it becomes available. A ticket title and description or a task written in the prompt can be the only source. For an unfilled check or preview setting, look for the relevant setup in repository instructions, package scripts, and existing tests.

The prompt can add, replace, or exclude particular defaults for the current run. To start a ticket without the project's other reference documents, for example, say “Use the ticket text and the repository only.” The Orchestrator records the effective mode and sources in the run. Update an existing run's scope explicitly if new input changes what will be reviewed.
