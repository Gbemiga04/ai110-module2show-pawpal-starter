"""Run a small PawPal+ schedule demo from the command line."""

from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "Dog")
    luna = Pet("Luna", "Cat")

    mochi.add_task(
        Task("Breakfast", time(7, 0), "daily", 15, "high")
    )
    mochi.add_task(
        Task("Morning walk", time(8, 0), "daily", 30, "high")
    )
    luna.add_task(
        Task("Fresh water", time(7, 30), "daily", 5, "medium")
    )
    luna.add_task(
        Task("Evening meal", time(18, 0), "daily", 10, "high")
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    print("Today's Schedule")
    print("================")
    for pet, task in Scheduler(owner).organize_tasks():
        scheduled_time = task.time.strftime("%I:%M %p")
        print(
            f"{scheduled_time} | {pet.name} ({pet.species}) | "
            f"{task.description} - {task.duration_minutes} min "
            f"[{task.priority}; {task.frequency}]"
        )


if __name__ == "__main__":
    main()
