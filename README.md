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

`Task` stores a description, scheduled time, frequency, and completion status. `Pet` keeps its own tasks, while `Owner` manages multiple pets and provides access to all of their tasks. `Scheduler` retrieves tasks through the owner, sorts them by time, and can mark them complete. The example in `main.py` creates two pets and prints their combined daily schedule; tests cover task completion and adding tasks to a pet.

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

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.organize_tasks()` | Sorts tasks by scheduled clock time without modifying the input list. `organize_tasks()` gathers all owner tasks before sorting. |
| Filtering | `Scheduler.filter_tasks()` | Optionally filters by completion status, pet name, or both. Pet-name matching is case-insensitive. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups tasks by due date and time, then returns a warning for each slot with multiple tasks. Warnings identify same-pet and cross-pet conflicts. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks a task complete and appends a new incomplete task for daily or weekly recurrence. The next due date is one or seven days from today; one-time tasks do not recur. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
