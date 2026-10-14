"""Run a small PawPal+ schedule demo from the command line."""

from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "Dog")
    luna = Pet("Luna", "Cat")

    morning_walk = Task("Morning walk", time(8, 0), "daily", 30, "high")
    mochi.add_task(morning_walk)
    mochi.add_task(Task("Breakfast", time(7, 0), "daily", 15, "high"))
    mochi.add_task(Task("Training", time(8, 0), "daily", 15, "medium"))
    luna.add_task(Task("Evening meal", time(18, 0), "daily", 10, "high"))
    luna.add_task(Task("Fresh water", time(7, 30), "daily", 5, "medium"))
    luna.add_task(Task("Medication", time(8, 0), "daily", 10, "high"))
    morning_walk.mark_complete()

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    print("All tasks sorted by time")
    print("========================")
    for task in scheduler.sort_by_time():
        status = "complete" if task.completed else "pending"
        print(
            f"{task.time.strftime('%I:%M %p')} | {task.description} [{status}]"
        )

    print("\nPending tasks for Mochi")
    print("=======================")
    for task in scheduler.filter_tasks(completed=False, pet_name="mochi"):
        print(f"{task.time.strftime('%I:%M %p')} | {task.description}")

    print("\nCompleted tasks")
    print("===============")
    for task in scheduler.filter_tasks(completed=True):
        print(f"{task.time.strftime('%I:%M %p')} | {task.description}")

    print("\nSchedule conflict warnings")
    print("==========================")
    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"WARNING: {warning}")
    else:
        print("No conflicts detected.")


if __name__ == "__main__":
    main()
