# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What PawPal+ provides

PawPal+ currently lets an owner:

- Set their owner name and add pets with a name and species.
- Add care tasks for each pet with a description, time, frequency, duration, and priority.
- Review each pet's tasks and mark pending tasks complete.
- Generate a priority-first schedule for tasks due today or earlier.
- Find an open time slot for a task duration within the daily 6 AM–10 PM window.
- Keep pet and task data in `data.json` between app runs.

## Features

- **Pet and task management:** Keep multiple pets and their care tasks in Streamlit session state.
- **Priority scheduling:** `Scheduler.organize_tasks()` orders pending due tasks by priority (high, medium, low), then time and stable name/description tie-breakers. `Scheduler.sort_by_time()` remains available for chronological-only ordering.
- **Task filtering:** `Scheduler.filter_tasks()` selects tasks by completion status, pet name, or both.
- **Recurring tasks:** `Scheduler.mark_task_completed()` creates a new pending occurrence for daily tasks due the next day and weekly tasks due in seven days. Tasks marked “as needed” do not repeat automatically.
- **Conflict warnings:** `Scheduler.detect_conflicts()` checks pending tasks due on a selected date for overlapping time intervals, including conflicts between pets. The UI displays warnings with the tasks and times involved.
- **Next available slot:** `Scheduler.find_next_available_slot()` scans the requested day window and returns the earliest gap that can fit the requested duration, or `None` when no slot fits.
- **Persistent JSON storage:** `Owner.save_to_json()` and `Owner.load_from_json()` serialize pet/task data, including due dates and completion status, to `data.json`.
- **Readable output:** The Streamlit tables use colored priority labels and task-status icons; the CLI demo prints a fixed-width priority schedule, filters, conflicts, and the next available slot using standard-library formatting.
- **CLI demo and tests:** Run `main.py` to see sorting, filtering, and conflict warnings; run `python -m pytest` to verify task and scheduler behavior.

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

### Data persistence

The Streamlit app loads `data.json` beside `app.py` when it starts and saves the owner, pets, and tasks after edits. The JSON file is created on the first saved change and is ignored by Git to avoid committing personal pet data. `Owner.save_to_json(path)` and `Owner.load_from_json(path)` can also be used directly; the latter reports invalid or unreadable data instead of silently replacing it.

Persistence is implemented in `pawpal_system.py` and connected in `app.py`; `.gitignore` excludes the generated `data.json`. JSON round-trip tests live in `test_pawpal_system.py`.

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests cover task management, chronological sorting, priority-first scheduling,
filters, daily and weekly recurrence, conflict detection, next-slot selection,
JSON persistence, and invalid inputs.

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: <project directory>
collected 24 items

test_pawpal_system.py ...................                                [ 79%]
tests\test_pawpal.py .....                                               [100%]

============================== 24 passed ==============================
```

**Confidence level:** ★★★★☆ (4/5) — the core scheduling behaviors and key edge cases pass automated tests; broader interactive and real-world scheduling scenarios still need validation.

## 📐 Smarter Scheduling

Implemented priority scheduling, filtering, conflict detection, recurring task handling, next-slot selection, and JSON persistence.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority scheduling | `Scheduler.organize_tasks()` | Sorts by priority (high to low), then time, pet name, and description. |
| Chronological sorting | `Scheduler.sort_by_time()` | Returns tasks sorted by start time. |
| Filtering | `Scheduler.filter_tasks()`, `get_pending_tasks()`, `get_completed_tasks()`, `get_tasks_for_pet()` | Filter by completion status and/or pet name. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warnings for overlapping pending tasks, including tasks for different pets; completed and future tasks are excluded. |
| Recurring tasks | `Scheduler.mark_task_completed()` | Completing daily and weekly tasks creates a pending occurrence due tomorrow or in 7 days; as-needed tasks do not repeat automatically. |
| Open time slots | `Scheduler.find_next_available_slot()` | Finds the earliest gap that fits a requested duration in the configured daily window. |
| Persistence | `Owner.save_to_json()`, `Owner.load_from_json()` | Saves and restores owner, pet, and task data in `data.json`. |
| Output formatting | Streamlit task/schedule tables; `main.py` formatting | Priority and status indicators in the UI and aligned priority-first CLI columns; implemented with Streamlit and Python f-strings. |

## Demo Walkthrough

1. Start the Streamlit app with `streamlit run app.py`. Enter the owner's name.
2. Use **Add a pet** to register a pet, then select it from **Choose a pet**.
3. Enter a care-task description, scheduled time, frequency, duration, and priority, then choose **Add task**.
4. Review each pet's task table. Use **Mark complete** to complete a pending task; daily and weekly tasks receive their next occurrence automatically.
5. Use **Find next available slot** to find a gap for a task duration. Choose **Generate schedule** to view pending due tasks in priority-first order; if tasks overlap, the app shows warnings naming both pets, tasks, and times.
6. Mark a recurring task complete to see the next daily or weekly occurrence. PawPal+ saves changes in `data.json` so they are available on the next app run.

Run `python main.py` for a terminal demo of priority sorting, filtering, conflict detection, next-slot selection, and readable task formatting:

```
Today's priority-first schedule
===============================
HIGH   | 07:00 AM | Mochi  | Breakfast      |  15 min
HIGH   | 08:00 AM | Luna   | Medication     |  10 min
HIGH   | 06:00 PM | Luna   | Evening meal   |  10 min
MEDIUM | 07:30 AM | Luna   | Fresh water    |   5 min
MEDIUM | 08:00 AM | Mochi  | Training       |  15 min

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

Next available 20-minute slot
=============================
06:00 AM
```
