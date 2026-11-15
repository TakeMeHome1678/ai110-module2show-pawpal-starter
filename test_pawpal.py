"""Unit tests for PawPal+ task and multi-pet behavior."""

import unittest

from pawpal_system import Owner, Pet, Task


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


if __name__ == "__main__":
    unittest.main()
