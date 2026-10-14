# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked my Copilot coding assistant to extend PawPal+ with a next-available-slot algorithm, JSON persistence, priority-first scheduling, more readable UI/CLI output, and documentation and tests for those features.

**What did the agent do?**

It added `Scheduler.find_next_available_slot()`, `Owner.save_to_json()` and `Owner.load_from_json()`, changed the schedule ordering to prioritize high-priority tasks, connected persistence and slot suggestions to the Streamlit app, and added tests and documentation. The work touched `pawpal_system.py`, `app.py`, `main.py`, `test_pawpal_system.py`, `README.md`, `.gitignore`, `diagrams/uml.mmd`, `diagrams/uml_final.mmd`, and this log. It also ran the test suite and CLI demo during verification.

**What did you have to verify or fix manually?**

I reviewed whether priority-first ordering matched the new requirement and updated an older test that still expected time-first ordering. I checked the JSON round-trip behavior and used temporary test files so automated tests do not overwrite personal data. I verified the actual CLI output before documenting it. I also added `data.json` to `.gitignore` so personal pet details are not accidentally committed.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

I used one AI coding assistant in this project, so I cannot honestly claim to have compared responses from two different models. I recorded the actual implementation prompt below rather than inventing a second model's output.

| | Actual run | Second model |
|-|------------|--------------|
| **Model / tool used** | Copilot coding assistant in VS Code | Not used in this project |
| **Prompt** | “Add a third algorithmic capability such as next available slot, persist pets and tasks in JSON, prioritize scheduling, and improve output formatting. Document and test the changes.” | No prompt was sent |
| **Response summary** | Implemented a time-window slot search, JSON serialization, priority-first schedule order, status/priority indicators, and related tests and documentation. | No response available to compare |
| **What was useful** | The request covered the end-to-end feature, including UI, tests, persistence, and docs. | Not applicable |
| **Problems noticed** | The priority-order change invalidated a time-first test expectation, so I updated the test to match the new intended behavior and reran the suite. | Not applicable |
| **Decision** | Use the implementation after reviewing its behavior and running tests. | A true multi-model comparison remains future work. |

I chose a simple interval scan for the next-slot search because its behavior is easy to follow and verify for a household-sized schedule. I did not claim a multi-model winner because I did not run a second model.
