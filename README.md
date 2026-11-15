# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- Add pets with a name, species, and optional breed in the Streamlit UI.
- Schedule tasks for a pet with a time and once, daily, or weekly recurrence.
- View household tasks ordered by due date and time with their current status.
- Filter the schedule by pet and by pending/completed status.
- Mark tasks complete; daily and weekly tasks create a new pending occurrence for the next day or week.
- Detect same-time tasks on the same date and show warnings for conflicts within or across pets.
- Run the terminal demo with `python main.py` to see sorted tasks, conflict warnings, and filtered task lists.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the example terminal schedule with:

```bash
python main.py
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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```text
...............                                                          [100%]
15 passed in 0.01s
```
## 📐 Smarter Scheduling

The scheduler supports the following behaviors:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.get_schedule()` | `sort_by_time()` returns tasks ordered by their 24-hour `HH:MM` time. `get_schedule()` returns pet-task pairs ordered by due date and then time. |
| Filtering | `Scheduler.filter_tasks()` | Optionally filter by completion status, pet name, or both. Pet names match without case sensitivity. |
| Conflict detection | `Scheduler.check_conflicts()` | Returns warning messages when two tasks share a due date and time, including conflicts for the same pet or across pets. It does not interrupt schedule generation. |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates a new pending occurrence due one or seven days later, respectively. One-time tasks are only marked complete. |

## Demo Walkthrough

### Using the Streamlit UI

1. Run `streamlit run app.py` and open PawPal+ in your browser. The app starts with example pets and tasks.
2. In **Your Pets**, enter a pet's name, choose a species, optionally add a breed, and select **Add pet**. The pet list refreshes with the new pet.
3. In **Schedule a Task**, choose a pet, enter a task, select its time and recurrence, then select **Add task**. New tasks are due today by default.
4. In **Complete a Task**, choose a pending task and select **Mark complete**. A daily or weekly task reports its next due date and adds a new pending occurrence.
5. Review **Schedule Conflicts** for warnings that identify overlapping tasks, pets, date, and time. Use **Filter by pet** and **Filter by status** to narrow the household schedule.

The schedule is ordered by due date and time. The scheduler also detects same-date, same-time conflicts between tasks for one pet or across pets; warnings are informational and do not prevent the schedule from displaying.

### Terminal demo

Run `python main.py` to see an example schedule with deliberately overlapping tasks, a completed recurring task, the resulting next occurrence, and filtered views:

```text
🐾 SORTED SCHEDULE FOR JORDAN'S HOUSEHOLD
[2026-11-15 07:30] Mochi -> Morning Walk (PENDING)
[2026-11-15 07:30] Mochi -> Medication (PENDING)
[2026-11-15 07:30] Luna -> Breakfast (PENDING)
[2026-11-15 07:45] Luna -> Morning Feeding (COMPLETED)
[2026-11-15 14:00] Luna -> Coat Grooming & Brushing (PENDING)
[2026-11-15 18:30] Mochi -> Evening Walk (PENDING)
[2026-11-16 07:45] Luna -> Morning Feeding (PENDING)

⚠️ SCHEDULE CONFLICTS
Warning: Mochi has tasks at the same time (2026-11-15 07:30): Morning Walk and Medication.
Warning: Mochi and Luna have tasks at the same time (2026-11-15 07:30): Morning Walk and Breakfast.
Warning: Mochi and Luna have tasks at the same time (2026-11-15 07:30): Medication and Breakfast.

✅ COMPLETED TASKS
[2026-11-15 07:45] Luna -> Morning Feeding

🐶 MOCHI'S TASKS
[2026-11-15 07:30] Mochi -> Morning Walk (PENDING)
[2026-11-15 07:30] Mochi -> Medication (PENDING)
[2026-11-15 18:30] Mochi -> Evening Walk (PENDING)
```
