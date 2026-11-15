"""Core domain classes for the PawPal+ multi-pet care scheduler."""

from datetime import datetime


class Task:
    """Represent one scheduled care task."""

    def __init__(
        self,
        title: str,
        scheduled_time: str,
        recurrence: str = "once",
    ) -> None:
        """Create a pending task with its schedule and recurrence."""
        self.title = title
        self.scheduled_time = scheduled_time
        self.recurrence = recurrence
        self.status = "PENDING"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.status = "COMPLETED"


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

    def get_all_tasks(self) -> list[Task]:
        """Return care tasks aggregated across all owned pets."""
        return [task for pet in self._pets for task in pet.get_tasks()]


class Scheduler:
    """Build and display an owner's time-ordered care schedule."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for one owner."""
        self.owner = owner

    def get_schedule(self) -> list[tuple[Pet, Task]]:
        """Return all pet tasks sorted by their scheduled time."""
        entries = [
            (pet, task)
            for pet in self.owner._pets
            for task in pet.get_tasks()
        ]
        return sorted(
            entries,
            key=lambda entry: datetime.strptime(entry[1].scheduled_time, "%I:%M %p"),
        )

    def display_schedule(self) -> None:
        """Print the owner's household schedule to the terminal."""
        print(f"🐾 MASTER SCHEDULE FOR {self.owner.name.upper()}'S HOUSEHOLD")
        for pet, task in self.get_schedule():
            print(
                f"[{task.scheduled_time}] {pet.name} -> {task.title} "
                f"({task.recurrence})"
            )
