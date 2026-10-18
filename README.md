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

## Implementation Summary

`Task` stores a description, scheduled time, frequency, and completion status. `Pet` keeps its own tasks, while `Owner` manages multiple pets and provides access to all of their tasks. `Scheduler` retrieves tasks through the owner, sorts them by time, and can mark them complete. The example in `main.py` creates two pets and prints their combined daily schedule.

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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
ai110-module2show-pawpal-starter % python3 main.py
Today's Schedule
07:30 - Breakfast
08:00 - Morning walk
18:00 - Evening feeding
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

The tests cover task completion and adding tasks, chronological sorting, filtering by completion status and pet name, daily and weekly recurrence (including date rollover), and conflict detection for duplicate times.

Confidence Level – 5 stars

Sample test output:

```
# Paste your pytest output here
% python3 -m pytest
======================================================== test session starts =========================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/swe/codepathai110/ai110-module2show-pawpal-starter
collected 8 items

tests/test_pawpal.py ........                                                                                                  [100%]

========================================================= 8 passed in 0.02s ==========================================================
```

## Features

- **Sorting by time:** Schedules tasks in chronological order by clock time without changing the original list.
- **Task filtering:** Filters by completion status, pet name, or both. Pet-name matching is case-insensitive.
- **Conflict warnings:** Groups tasks by due date and time and warns when multiple tasks share a time slot. Warnings identify the task and pet names, and whether the conflict is for one pet or multiple pets. Repeated references to the same task are counted once.
- **Daily recurrence:** Completing a daily task creates a new, incomplete occurrence due the next day.
- **Weekly recurrence:** Completing a weekly task creates a new, incomplete occurrence due seven days later.
- **One-time tasks:** Completing a one-time task marks it complete without creating another occurrence. Already-completed tasks are not repeated.
- **Streamlit schedule view:** Shows tasks in time order with pet and completion-status filters, and displays actionable conflict warnings.

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.organize_tasks()` | Sorts by scheduled clock time without modifying the input list. `organize_tasks()` gathers all owner tasks before sorting. |
| Filtering | `Scheduler.filter_tasks()` | Optionally filters by completion status, pet name, or both. Pet-name matching is case-insensitive. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups tasks by due date and time, then returns a warning for each slot with multiple tasks. Warnings identify same-pet and cross-pet conflicts. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks a task complete and appends a new incomplete task for daily or weekly recurrence, due one or seven days later. One-time and already-completed tasks do not recur. |

## Demo Walkthrough

### Streamlit App

The app lets an owner enter their name and the initial pet's name and species, then schedule a task by entering its description, time, and frequency (daily, weekly, or once). The schedule appears in a table with each task's pet, time, frequency, and completion status. Pet and status selectors filter the table. Conflict warnings appear above the schedule when tasks share a due date and time; otherwise, the app confirms that no conflicts were detected.

### Example Workflow

1. Enter the owner's name and the pet's name and species. This creates the initial pet in the app.
2. Enter a task such as "Morning walk," choose its time and frequency, and submit the form.
3. View the task in the schedule table, ordered by time. Use the pet and status selectors to filter the displayed tasks.
4. If two tasks overlap, review the warning for the task names, pets, date, and time, then move one task to another time.

The Streamlit form creates one initial pet; adding additional pets is demonstrated in the CLI example below. The Scheduler sorts tasks by scheduled clock time, filters by pet and completion status, and detects conflicts by due-date/time slot. Completing a daily or weekly task through the Scheduler creates its next occurrence for the following day or seven days later.

### CLI Output

Run `python3 main.py` to print a sample schedule and conflict warning:

```text
Today's Schedule
Owner:  Jordan
07:30 - Breakfast
08:00 - Morning walk
14:00 - Nap
16:00 - Snack
16:00 - Play
18:00 - Evening feeding
Warning: Snack (Biscuit), Play (Biscuit) are scheduled for 16:00 on 2026-10-18 for the same pet.
```
