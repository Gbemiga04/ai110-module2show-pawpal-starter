from datetime import time

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def make_task(
    description: str,
    scheduled_time: time,
    *,
    completed: bool = False,
    priority: str = "medium",
) -> Task:
    return Task(
        description=description,
        time=scheduled_time,
        frequency="daily",
        duration_minutes=20,
        priority=priority,
        completed=completed,
    )


def test_owner_collects_tasks_from_all_pets() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Miso", "cat")
    dog_task = make_task("Walk", time(8, 0))
    cat_task = make_task("Feed", time(7, 30))
    dog.add_task(dog_task)
    cat.add_task(cat_task)
    owner.add_pet(dog)
    owner.add_pet(cat)

    assert owner.get_all_tasks() == [dog_task, cat_task]


def test_scheduler_organizes_tasks_by_time_then_priority() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    dog.add_task(make_task("Late", time(9, 0)))
    dog.add_task(make_task("Lower priority", time(8, 0), priority="low"))
    dog.add_task(make_task("Higher priority", time(8, 0), priority="high"))
    owner.add_pet(dog)

    organized = Scheduler(owner).organize_tasks()

    assert [task.description for _, task in organized] == [
        "Higher priority",
        "Lower priority",
        "Late",
    ]


def test_scheduler_filters_completion_and_can_update_status() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    task = make_task("Walk", time(8, 0))
    done_task = make_task("Feed", time(7, 0), completed=True)
    pet.add_task(task)
    pet.add_task(done_task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    assert scheduler.get_pending_tasks() == [task]
    assert scheduler.get_completed_tasks() == [done_task]
    assert [scheduled.description for _, scheduled in scheduler.organize_tasks()] == [
        "Walk"
    ]

    scheduler.mark_task_completed(task)
    assert scheduler.get_pending_tasks() == []
    assert task in scheduler.get_completed_tasks()

    scheduler.mark_task_pending(done_task)
    assert done_task in scheduler.get_pending_tasks()


def test_scheduler_rejects_pet_or_task_not_owned_by_owner() -> None:
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    outside_pet = Pet("Mochi", "dog")
    outside_task = make_task("Walk", time(8, 0))

    with pytest.raises(ValueError, match="does not belong"):
        scheduler.get_tasks_for_pet(outside_pet)
    with pytest.raises(ValueError, match="does not belong"):
        scheduler.mark_task_completed(outside_task)


def test_task_rejects_invalid_duration_and_priority() -> None:
    with pytest.raises(ValueError, match="duration"):
        Task("Walk", time(8, 0), "daily", 0, "medium")
    with pytest.raises(ValueError, match="priority"):
        Task("Walk", time(8, 0), "daily", 20, "urgent")
