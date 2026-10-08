# PawPal+ (Module 2 Project)

**PawPal+** is a Python and Streamlit app for organizing care tasks across multiple pets.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

## Features

- **Multiple pets:** Add pets and assign care tasks to each one.
- **Scheduled tasks:** Enter a task's category, duration, priority, date, and start time.
- **Chronological sorting:** Display unfinished tasks across all dates in scheduled order, with unscheduled tasks last.
- **Task filtering:** Filter the task table by pet name and completion status.
- **Conflict warnings:** Identify overlapping unfinished tasks across all pets using their start times and durations. Tasks that meet exactly at an endpoint do not conflict.
- **Session memory:** Keep pets and tasks available during Streamlit reruns within the current session.
- **Daily and weekly recurrence (backend and CLI):** Completing a recurring task through Scheduler creates its next occurrence and retains the completed task. The next date is based on completion, preserving the scheduled clock time.

The browser currently supports adding tasks, filtering, sorting, and conflict warnings. Task completion and recurrence are demonstrated in the CLI; browser controls for completing, repeating, or rescheduling tasks are not yet implemented. Priority is recorded and displayed but does not determine schedule order.
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









## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Optional coverage report (requires pytest-cov):
python -m pip install pytest-cov
python -m pytest --cov=pawpal_system
```

Sample test output:

```

collected 2 items

tests\test_pawpal.py .. [100%]

2 passed in 0.06s
```

These two tests verify task completion and adding a task to a pet. Sorting, filtering, recurrence, and conflict detection are demonstrated by the CLI walkthrough; they are not covered by these tests.

## 📐 Smarter Scheduling

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Sorting | `Scheduler.sort_by_time()` | Returns unfinished plan entries in scheduled date and time order, with unscheduled tasks last. |
| Filtering | `Scheduler.filter_tasks()` | Filters by optional pet name and completion status. Name matching ignores capitalization. |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns about overlapping unfinished tasks across pets. Skips unscheduled tasks and allows one task to begin exactly when another ends. |
| Recurrence | `Task.next_due_date()`, `Scheduler.mark_task_complete()` | Creates the next daily or weekly occurrence from the completion date, preserves its scheduled clock time, and retains the completed task. |



## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. From the project folder, run `python -m streamlit run app.py` and open the Local URL.
2. Enter an owner name. Add a pet named Mochi with species dog.
3. Select Mochi and add a walking task named Morning walk: 30 minutes, high priority, today at 09:00.
4. Add a grooming task named Brush fur for Mochi: 30 minutes, medium priority, the same date at 08:45.
5. Review Current tasks. Use Filter by pet name and Show tasks to narrow the table. Choosing Completed shows no matches until completed tasks exist.
6. Click Generate schedule. Brush fur appears before Morning walk because Scheduler sorts by scheduled date and time.
7. Read the conflict warning: Brush fur ends at 09:15, overlapping the walk that starts at 09:00. The app reports the overlap without changing either task.

Report filters apply to Current tasks. Generate schedule includes all unfinished tasks across pets and dates, independently of those filters.

To explore completion and daily or weekly recurrence, run `python main.py` in the terminal. The CLI also demonstrates sorting, filtering, and conflict warnings.


## 🖥️ Sample Output
### Sample CLI output

Example run on October 1, 2026. Recurring dates depend on the completion date. Each section shows the task state at that point in the script.

```text
Scheduled tasks
---------------------------
2026-10-01 08:00 - Buddy: Morning Feed (10 minutes)
2026-10-01 08:30 - Luna: Brush fur (15 minutes)
2026-10-01 09:00 - Buddy: Morning walk (30 minutes)

Buddy's tasks
-------------
Buddy: Morning walk
Buddy: Morning Feed

Completed tasks
---------------
Buddy: Morning Feed

Unfinished tasks
----------------
Buddy: Morning walk
Buddy: Morning Feed
Luna: Brush fur

Feeding occurrences
-------------------
Buddy: Morning Feed | 2026-10-01 08:00 | Completed
Buddy: Morning Feed | 2026-10-02 08:00 | Unfinished

Grooming occurrences
--------------------
Luna: Brush fur | 2026-10-01 08:30 | Completed
Luna: Brush fur | 2026-10-08 08:30 | Unfinished

Conflict warnings
-----------------
Conflict: Buddy's Morning walk (2026-10-01 09:00 to 09:30) overlaps with Luna's Grooming appointment (2026-10-01 09:00 to 09:20).
```