# test_pawpal.py
import unittest
from pawpal_system import Task, Pet

class TestPawPalSystem(unittest.TestCase):

    def test_task_completion(self):
        """Verify that calling mark_complete() changes the task's status."""
        # Arrange
        task = Task("Afternoon Walk", "03:00 PM", "daily")
        
        # Act & Assert initial state
        self.assertEqual(task.status, "PENDING", "Initial task status should be PENDING")
        
        # Act
        task.mark_complete()
        
        # Assert final state
        self.assertEqual(task.status, "COMPLETED", "Task status should update to COMPLETED after mark_complete()")

    def test_task_addition(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange
        pet = Pet("Mochi", "Dog", "Shiba Inu")
        self.assertEqual(len(pet.get_tasks()), 0, "New pet should start with 0 tasks")
        
        task1 = Task("Morning Walk", "07:30 AM")
        task2 = Task("Breakfast Feeding", "08:00 AM")
        
        # Act
        pet.add_task(task1)
        
        # Assert count after first addition
        self.assertEqual(len(pet.get_tasks()), 1, "Task count should be 1 after adding a task")
        
        # Act
        pet.add_task(task2)
        
        # Assert count after second addition
        self.assertEqual(len(pet.get_tasks()), 2, "Task count should be 2 after adding a second task")
        self.assertIn(task1, pet.get_tasks())
        self.assertIn(task2, pet.get_tasks())

if __name__ == "__main__":
    unittest.main()