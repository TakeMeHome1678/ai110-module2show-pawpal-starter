# main.py

from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # 1. Create an Owner
    jordan = Owner("Jordan")

    # 2. Create at least two Pets
    mochi = Pet("Mochi", "Dog", "Shiba Inu")
    luna = Pet("Luna", "Cat", "Domestic Shorthair")

    # 3. Add at least three Tasks with different times to those pets
    # Mochi's tasks
    mochi.add_task(Task("Morning Walk", "07:30 AM", "daily"))
    mochi.add_task(Task("Breakfast Feeding", "08:00 AM", "daily"))
    
    # Luna's tasks
    luna.add_task(Task("Morning Feeding", "07:45 AM", "daily"))
    luna.add_task(Task("Coat Grooming & Brushing", "02:00 PM", "weekly"))

    # Link pets to the owner
    jordan.add_pet(mochi)
    jordan.add_pet(luna)

    # 4. Initialize the Scheduler and print Today's Schedule to the terminal
    scheduler = Scheduler(jordan)
    scheduler.display_schedule()

if __name__ == "__main__":
    main()