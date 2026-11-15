#!/usr/bin/env python3
"""Print an example PawPal+ multi-pet care schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Build and display a sample household schedule."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "Dog", "Shiba Inu")
    luna = Pet("Luna", "Cat", "Domestic Shorthair")

    mochi.add_task(Task("Morning Walk", "07:30 AM", "daily"))
    mochi.add_task(Task("Breakfast Feeding", "08:00 AM", "daily"))
    luna.add_task(Task("Morning Feeding", "07:45 AM", "daily"))
    luna.add_task(Task("Coat Grooming & Brushing", "02:00 PM", "weekly"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    Scheduler(owner).display_schedule()


if __name__ == "__main__":
    main()
