#!/usr/bin/env python3
"""Print an example PawPal+ multi-pet care schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Build and display a sample household schedule."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "Dog", "Shiba Inu")
    luna = Pet("Luna", "Cat", "Domestic Shorthair")

    mochi.add_task(Task("Evening Walk", "18:30", "daily"))
    mochi.add_task(Task("Morning Walk", "07:30", "daily"))
    mochi.add_task(Task("Medication", "07:30"))
    luna_feeding = Task("Morning Feeding", "07:45", "daily")
    luna.add_task(luna_feeding)
    luna.add_task(Task("Breakfast", "07:30"))
    luna.add_task(Task("Coat Grooming & Brushing", "14:00", "weekly"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(luna_feeding)

    print(f"🐾 SORTED SCHEDULE FOR {owner.name.upper()}'S HOUSEHOLD")
    for pet, task in scheduler.get_schedule():
        print(
            f"[{task.due_date} {task.scheduled_time}] {pet.name} -> "
            f"{task.title} ({task.status})"
        )

    print("\n⚠️ SCHEDULE CONFLICTS")
    conflicts = scheduler.check_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No scheduling conflicts found.")

    print("\n✅ COMPLETED TASKS")
    for pet, task in scheduler.filter_tasks(completed=True):
        print(f"[{task.due_date} {task.scheduled_time}] {pet.name} -> {task.title}")

    print("\n🐶 MOCHI'S TASKS")
    for pet, task in scheduler.filter_tasks(pet_name="Mochi"):
        print(
            f"[{task.due_date} {task.scheduled_time}] "
            f"{pet.name} -> {task.title} ({task.status})"
        )


if __name__ == "__main__":
    main()
