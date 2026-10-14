from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_task_status() -> None:
    task = Task(
        description="Morning walk",
        time=time(8, 0),
        frequency="daily",
        duration_minutes=30,
        priority="high",
    )

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog")
    task = Task(
        description="Morning walk",
        time=time(8, 0),
        frequency="daily",
        duration_minutes=30,
        priority="high",
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_scheduler_returns_tasks_in_chronological_order() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    late_task = Task("Evening meal", time(18, 0), "daily", 15, "high")
    early_task = Task("Breakfast", time(7, 0), "daily", 15, "high")
    pet.add_task(late_task)
    pet.add_task(early_task)
    owner.add_pet(pet)

    assert Scheduler(owner).sort_by_time() == [early_task, late_task]


def test_completing_daily_task_creates_occurrence_for_following_day() -> None:
    today = date(2026, 10, 14)
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    task = Task(
        "Morning walk",
        time(8, 0),
        "daily",
        30,
        "high",
        due_date=today,
    )
    pet.add_task(task)
    owner.add_pet(pet)

    next_task = Scheduler(owner).mark_task_completed(task, today=today)

    assert task.completed is True
    assert next_task is not None
    assert next_task is not task
    assert next_task.completed is False
    assert next_task.due_date == today + timedelta(days=1)
    assert pet.tasks == [task, next_task]


def test_scheduler_warns_when_tasks_start_at_the_same_time() -> None:
    schedule_date = date.today()
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    dog.add_task(
        Task("Morning walk", time(8, 0), "daily", 30, "high", due_date=schedule_date)
    )
    cat.add_task(
        Task("Breakfast", time(8, 0), "daily", 15, "high", due_date=schedule_date)
    )
    owner.add_pet(dog)
    owner.add_pet(cat)

    warnings = Scheduler(owner).detect_conflicts(on_date=schedule_date)

    assert len(warnings) == 1
    assert "Mochi's Morning walk" in warnings[0]
    assert "Luna's Breakfast" in warnings[0]
