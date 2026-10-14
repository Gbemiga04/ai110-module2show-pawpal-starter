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

    print("Today's priority-first schedule")
    print("===============================")
    schedule = scheduler.organize_tasks()
    for pet, task in schedule:
        print(
            f"{task.priority.upper():<6} | {task.time.strftime('%I:%M %p')} | "
            f"{pet.name:<6} | {task.description:<14} | {task.duration_minutes:>3} min"
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

    next_slot = scheduler.find_next_available_slot(20)
    print("\nNext available 20-minute slot")
    print("=============================")
    print(next_slot.strftime("%I:%M %p") if next_slot else "No slot available.")

if __name__ == "__main__":
    main()
