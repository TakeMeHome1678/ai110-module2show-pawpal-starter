"""Unit tests for PawPal+ task and multi-pet behavior."""

import unittest
from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


class TestPawPalSystem(unittest.TestCase):
    """Test core PawPal+ domain behavior."""

    def test_task_addition(self) -> None:
        """Verify that pets store tasks added to them."""
        pet = Pet("Mochi", "Dog", "Shiba Inu")
        first_task = Task("Morning Walk", "07:30 AM")
        second_task = Task("Breakfast Feeding", "08:00 AM")

        pet.add_task(first_task)
        pet.add_task(second_task)

        self.assertEqual(pet.get_tasks(), [first_task, second_task])

    def test_task_completion(self) -> None:
        """Verify that completing a task changes its status."""
        task = Task("Afternoon Walk", "03:00 PM", "daily")

        self.assertEqual(task.status, "PENDING")
        task.mark_complete()
        self.assertEqual(task.status, "COMPLETED")

    def test_owner_aggregates_tasks_from_all_pets(self) -> None:
        """Verify that an owner can retrieve tasks for every pet."""
        owner = Owner("Jordan")
        mochi = Pet("Mochi", "Dog")
        luna = Pet("Luna", "Cat")
        walk = Task("Morning Walk", "07:30 AM")
        feeding = Task("Breakfast Feeding", "08:00 AM")
        mochi.add_task(walk)
        luna.add_task(feeding)
        owner.add_pet(mochi)
        owner.add_pet(luna)

        self.assertEqual(owner.get_all_tasks(), [walk, feeding])

    def test_owner_returns_pets(self) -> None:
        """Verify that an owner can retrieve the pets in the household."""
        owner = Owner("Jordan")
        pet = Pet("Mochi", "Dog")
        owner.add_pet(pet)

        self.assertEqual(owner.get_pets(), [pet])

    def test_scheduler_sorts_tasks_by_hhmm_time(self) -> None:
        """Verify that tasks are sorted chronologically by their HH:MM time."""
        scheduler = Scheduler(Owner("Jordan"))
        tasks = [
            Task("Evening Walk", "18:30"),
            Task("Morning Feeding", "07:45"),
            Task("Breakfast", "08:00 AM"),
        ]

        self.assertEqual(
            [task.title for task in scheduler.sort_by_time(tasks)],
            ["Morning Feeding", "Breakfast", "Evening Walk"],
        )
        self.assertEqual(tasks[0].time, "18:30")

    def test_schedule_orders_by_due_date_then_time(self) -> None:
        """Verify that the schedule sorts by date first, then time."""
        owner = Owner("Jordan")
        mochi = Pet("Mochi", "Dog")
        luna = Pet("Luna", "Cat")

        mochi.add_task(Task("Late first day", "09:00", due_date=date(2026, 11, 15)))
        mochi.add_task(Task("Early next day", "07:00", due_date=date(2026, 11, 16)))
        luna.add_task(Task("Middle first day", "08:00", due_date=date(2026, 11, 15)))
        luna.add_task(Task("Early first day", "06:30", due_date=date(2026, 11, 15)))
        owner.add_pet(mochi)
        owner.add_pet(luna)

        schedule = Scheduler(owner).get_schedule()

        self.assertEqual(
            [(pet.name, task.title) for pet, task in schedule],
            [
                ("Luna", "Early first day"),
                ("Luna", "Middle first day"),
                ("Mochi", "Late first day"),
                ("Mochi", "Early next day"),
            ],
        )

    def test_scheduler_filters_by_completion_and_pet_name(self) -> None:
        """Verify that tasks can be filtered by completion state and pet."""
        owner = Owner("Jordan")
        mochi = Pet("Mochi", "Dog")
        luna = Pet("Luna", "Cat")
        completed_walk = Task("Walk", "07:30 AM")
        completed_walk.mark_complete()
        pending_walk = Task("Walk", "08:00 AM")
        pending_feeding = Task("Feeding", "08:30 AM")
        mochi.add_task(completed_walk)
        mochi.add_task(pending_walk)
        luna.add_task(pending_feeding)
        owner.add_pet(mochi)
        owner.add_pet(luna)
        scheduler = Scheduler(owner)

        self.assertEqual(
            [task for _, task in scheduler.filter_tasks(completed=True)],
            [completed_walk],
        )
        self.assertEqual(
            [pet.name for pet, _ in scheduler.filter_tasks(pet_name="lUnA")],
            ["Luna"],
        )
        self.assertEqual(
            [task for _, task in scheduler.filter_tasks(completed=False, pet_name="Mochi")],
            [pending_walk],
        )

    def test_daily_recurrence_is_due_exactly_next_day(self) -> None:
        """Verify that a completed daily task creates tomorrow's occurrence."""
        owner = Owner("Jordan")
        pet = Pet("Mochi", "Dog")
        task = Task("Walk", "07:30", "daily")
        pet.add_task(task)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        completed_on = date(2026, 11, 15)

        next_task = scheduler.mark_task_complete(task, completed_on)

        self.assertEqual(task.status, "COMPLETED")
        self.assertIsNotNone(next_task)
        self.assertIsNot(next_task, task)
        self.assertEqual(next_task.due_date, date(2026, 11, 16))
        self.assertEqual(next_task.status, "PENDING")
        self.assertEqual(pet.get_tasks(), [task, next_task])

    def test_completing_weekly_task_adds_next_weeks_occurrence(self) -> None:
        """Verify that completing a weekly task schedules it seven days later."""
        owner = Owner("Jordan")
        pet = Pet("Luna", "Cat")
        task = Task("Grooming", "14:00", "weekly")
        pet.add_task(task)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        completed_on = date(2026, 11, 15)

        next_task = scheduler.mark_task_complete(task, completed_on)

        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.due_date, completed_on + timedelta(days=7))
        self.assertEqual(pet.get_tasks(), [task, next_task])

    def test_completing_one_time_task_does_not_add_an_occurrence(self) -> None:
        """Verify that completing a one-time task does not reschedule it."""
        owner = Owner("Jordan")
        pet = Pet("Mochi", "Dog")
        task = Task("Vet Visit", "10:00")
        pet.add_task(task)
        owner.add_pet(pet)

        self.assertIsNone(Scheduler(owner).mark_task_complete(task))
        self.assertEqual(task.status, "COMPLETED")
        self.assertEqual(pet.get_tasks(), [task])

    def test_scheduler_warns_about_same_pet_time_conflict(self) -> None:
        """Verify that same-pet tasks at the same time produce a warning."""
        owner = Owner("Jordan")
        pet = Pet("Mochi", "Dog")
        pet.add_task(Task("Walk", "07:30"))
        pet.add_task(Task("Medication", "07:30 AM"))
        owner.add_pet(pet)

        warnings = Scheduler(owner).check_conflicts()

        self.assertEqual(len(warnings), 1)
        self.assertIn("Warning:", warnings[0])
        self.assertIn("Mochi", warnings[0])
        self.assertIn("Walk and Medication", warnings[0])

    def test_same_time_tasks_across_pets_produce_one_conflict(self) -> None:
        """Verify that matching times across pets produce one warning."""
        owner = Owner("Jordan")
        mochi = Pet("Mochi", "Dog")
        luna = Pet("Luna", "Cat")
        mochi.add_task(Task("Walk", "07:30"))
        luna.add_task(Task("Feeding", "07:30"))
        owner.add_pet(mochi)
        owner.add_pet(luna)

        warnings = Scheduler(owner).check_conflicts()

        self.assertEqual(len(warnings), 1)
        self.assertIn("Mochi and Luna", warnings[0])
        self.assertIn("Walk and Feeding", warnings[0])

    def test_scheduler_does_not_conflict_across_due_dates(self) -> None:
        """Verify that tasks at the same time on different dates are not conflicts."""
        owner = Owner("Jordan")
        pet = Pet("Mochi", "Dog")
        pet.add_task(Task("Walk today", "07:30", due_date=date(2026, 11, 15)))
        pet.add_task(Task("Walk tomorrow", "07:30", due_date=date(2026, 11, 16)))
        owner.add_pet(pet)

        self.assertEqual(Scheduler(owner).check_conflicts(), [])


if __name__ == "__main__":
    unittest.main()
