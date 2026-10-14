from datetime import date, time, timedelta

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


def test_scheduler_sorts_tasks_by_time_and_includes_completed_by_default() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    late_task = make_task("Late", time(9, 0))
    early_task = make_task("Early", time(7, 0), completed=True)
    dog.add_task(late_task)
    dog.add_task(early_task)
    owner.add_pet(dog)

    sorted_tasks = Scheduler(owner).sort_by_time()

    assert sorted_tasks == [early_task, late_task]
    assert Scheduler(owner).sort_by_time(False) == [late_task]


def test_scheduler_filters_by_completion_and_case_insensitive_pet_name() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    pending_task = make_task("Walk", time(8, 0))
    completed_task = make_task("Feed", time(7, 0), completed=True)
    dog.add_task(pending_task)
    cat.add_task(completed_task)
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(completed=False, pet_name="mochi") == [
        pending_task
    ]
    assert scheduler.filter_tasks(completed=True) == [completed_task]
    assert scheduler.filter_tasks(pet_name="unknown") == []


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

    next_task = scheduler.mark_task_completed(task)
    assert next_task is not None
    assert scheduler.get_pending_tasks() == [next_task]
    assert task in scheduler.get_completed_tasks()

    scheduler.mark_task_pending(done_task)
    assert scheduler.get_pending_tasks() == [done_task, next_task]


def test_completing_daily_task_creates_next_occurrence() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    task = make_task("Walk", time(8, 0))
    pet.add_task(task)
    owner.add_pet(pet)
    today = date(2026, 10, 14)

    next_task = Scheduler(owner).mark_task_completed(task, today=today)

    assert task.completed is True
    assert next_task is not None
    assert next_task is not task
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False
    assert pet.tasks == [task, next_task]
    assert Scheduler(owner).organize_tasks() == []


def test_completing_weekly_task_creates_next_occurrence_in_seven_days() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    task = Task("Grooming", time(10, 0), "weekly", 45, "medium")
    pet.add_task(task)
    owner.add_pet(pet)
    today = date(2026, 10, 14)

    next_task = Scheduler(owner).mark_task_completed(task, today=today)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)
    assert next_task.description == task.description
    assert next_task.time == task.time
    assert next_task.frequency == task.frequency
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.priority == task.priority


def test_as_needed_and_already_completed_tasks_do_not_create_occurrences() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    as_needed = Task("Vet visit", time(11, 0), "as needed", 60, "high")
    daily = make_task("Food", time(7, 0))
    daily.mark_complete()
    pet.add_task(as_needed)
    pet.add_task(daily)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    assert scheduler.mark_task_completed(as_needed) is None
    assert scheduler.mark_task_completed(daily) is None
    assert len(pet.tasks) == 2
    assert as_needed.completed is True


def test_scheduler_detects_overlaps_for_the_same_pet() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(make_task("Walk", time(8, 0)))
    pet.add_task(make_task("Medication", time(8, 15)))
    pet.add_task(make_task("Breakfast", time(8, 20)))
    owner.add_pet(pet)

    warnings = Scheduler(owner).detect_conflicts(on_date=date.today())

    assert len(warnings) == 2
    assert all("Mochi" in warning and "overlaps" in warning for warning in warnings)


def test_scheduler_detects_overlaps_across_pets_but_ignores_completed_tasks() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    dog.add_task(make_task("Walk", time(8, 0)))
    cat.add_task(make_task("Feed", time(8, 10)))
    cat.add_task(make_task("Old appointment", time(8, 5), completed=True))
    owner.add_pet(dog)
    owner.add_pet(cat)

    warnings = Scheduler(owner).detect_conflicts(on_date=date.today())

    assert len(warnings) == 1
    assert "Mochi's Walk" in warnings[0]
    assert "Luna's Feed" in warnings[0]


def test_scheduler_does_not_report_tasks_that_do_not_overlap_or_are_future() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(make_task("Walk", time(8, 0)))
    pet.add_task(make_task("Dinner", time(9, 0)))
    future_task = Task(
        "Future task",
        time(8, 5),
        "daily",
        20,
        "high",
        due_date=date.today() + timedelta(days=1),
    )
    pet.add_task(future_task)
    owner.add_pet(pet)

    assert Scheduler(owner).detect_conflicts(on_date=date.today()) == []


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
