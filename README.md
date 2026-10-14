# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Sample terminal output from running `python main.py`:

```
All tasks sorted by time
========================
07:00 AM | Mochi | Breakfast [pending]
07:30 AM | Luna | Fresh water [pending]
08:00 AM | Mochi | Morning walk [complete]
08:00 AM | Mochi | Training [pending]
08:00 AM | Luna | Medication [pending]
06:00 PM | Luna | Evening meal [pending]

Pending tasks for Mochi
=======================
07:00 AM | Breakfast
08:00 AM | Training

Completed tasks
===============
08:00 AM | Morning walk

Schedule conflict warnings
==========================
WARNING: Conflict: Mochi's Training (08:00 AM to 08:15 AM) overlaps Luna's Medication (starts 08:00 AM).
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

Implemented sorting, filtering, conflict detection, and recurring task handling.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.organize_tasks()` | Sort by start time; organize also uses priority and stable tie-breakers. |
| Filtering | `Scheduler.filter_tasks()`, `get_pending_tasks()`, `get_completed_tasks()`, `get_tasks_for_pet()` | Filter by completion status and/or pet name. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warnings for overlapping pending tasks, including tasks for different pets; completed and future tasks are excluded. |
| Recurring tasks | `Scheduler.mark_task_completed()` | Completing daily and weekly tasks creates a pending occurrence due tomorrow or in 7 days; as-needed tasks do not repeat automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
