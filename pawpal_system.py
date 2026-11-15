"""Core domain classes for the PawPal+ multi-pet care scheduler."""

from __future__ import annotations

from datetime import date, datetime, timedelta

_RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


class Task:
    """Represent one scheduled care task."""

    def __init__(
        self,
        title: str,
        scheduled_time: str,
        recurrence: str = "once",
        due_date: date | None = None,
    ) -> None:
        """Create a pending task with its schedule, recurrence, and due date."""
        self.title = title
        self.scheduled_time = scheduled_time
        try:
            parsed_time = datetime.strptime(scheduled_time, "%H:%M")
        except ValueError:
            parsed_time = datetime.strptime(scheduled_time, "%I:%M %p")
        self.time = parsed_time.strftime("%H:%M")
        self.recurrence = recurrence
        self.due_date = due_date or date.today()
        self.status = "PENDING"

    def mark_complete(self, completed_on: date | None = None) -> Task | None:
        """Complete the task and return a pending copy for its next recurrence.

        Daily and weekly intervals come from ``_RECURRENCE_DAYS``. One-time
        tasks, and tasks already completed, do not produce another occurrence.
        """
        if self.status == "COMPLETED":
            return None
        self.status = "COMPLETED"
        days = _RECURRENCE_DAYS.get(self.recurrence.casefold())
        if days is None:
            return None

        next_due_date = (completed_on or date.today()) + timedelta(days=days)
        return Task(
            self.title,
            self.scheduled_time,
            self.recurrence,
            next_due_date,
        )


class Pet:
    """Represent a pet and its care tasks."""

    def __init__(self, name: str, species: str, breed: str = "") -> None:
        """Create a pet with an empty task list."""
        self.name = name
        self.species = species
        self.breed = breed
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self._tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        return list(self._tasks)


class Owner:
    """Represent an owner responsible for multiple pets."""

    def __init__(self, name: str) -> None:
        """Create an owner with no pets."""
        self.name = name
        self._pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self._pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        return list(self._pets)

    def get_all_tasks(self) -> list[Task]:
        """Return care tasks aggregated across all owned pets."""
        return [task for pet in self._pets for task in pet.get_tasks()]


class Scheduler:
    """Build and display an owner's time-ordered care schedule."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for one owner."""
        self.owner = owner

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return a new list sorted chronologically by each task's HH:MM time."""
        return sorted(tasks, key=lambda task: task.time)

    def get_schedule(self) -> list[tuple[Pet, Task]]:
        """Aggregate pet tasks and sort them by due date, then time."""
        entries = [
            (pet, task)
            for pet in self.owner._pets
            for task in pet.get_tasks()
        ]
        return sorted(entries, key=lambda entry: (entry[1].due_date, entry[1].time))

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Return scheduled tasks matching the provided optional filters.

        Pet-name matching is case-insensitive. If a filter is ``None``, that
        property is not used to exclude tasks.
        """
        entries = self.get_schedule()
        return [
            (pet, task)
            for pet, task in entries
            if (completed is None or (task.status == "COMPLETED") is completed)
            and (pet_name is None or pet.name.casefold() == pet_name.casefold())
        ]

    def check_conflicts(self) -> list[str]:
        """Return warnings for each pair sharing a due date and time.

        Compares scheduled task pairs and reports conflicts without modifying
        tasks or interrupting schedule generation.
        """
        entries = self.get_schedule()
        warnings: list[str] = []
        for index, (first_pet, first_task) in enumerate(entries):
            for second_pet, second_task in entries[index + 1 :]:
                if (
                    first_task.due_date == second_task.due_date
                    and first_task.time == second_task.time
                ):
                    if first_pet is second_pet:
                        conflict_description = f"{first_pet.name} has"
                    else:
                        conflict_description = (
                            f"{first_pet.name} and {second_pet.name} have"
                        )
                    warnings.append(
                        f"Warning: {conflict_description} tasks at the same time "
                        f"({first_task.due_date} {first_task.scheduled_time}): "
                        f"{first_task.title} and {second_task.title}."
                    )
        return warnings

    def mark_task_complete(
        self,
        task: Task,
        completed_on: date | None = None,
    ) -> Task | None:
        """Complete an owner's task and add its next occurrence, if recurring.

        Raises ``ValueError`` if the task is not assigned to one of the
        owner's pets; otherwise returns the newly added task or ``None``.
        """
        pet = next(
            (
                pet
                for pet in self.owner._pets
                if task in pet.get_tasks()
            ),
            None,
        )
        if pet is None:
            raise ValueError("Task does not belong to this owner's pets.")

        next_task = task.mark_complete(completed_on)
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def display_schedule(self) -> None:
        """Print the owner's household schedule to the terminal."""
        print(f"🐾 MASTER SCHEDULE FOR {self.owner.name.upper()}'S HOUSEHOLD")
        for pet, task in self.get_schedule():
            print(
                f"[{task.due_date} {task.scheduled_time}] {pet.name} -> {task.title} "
                f"({task.recurrence})"
            )
