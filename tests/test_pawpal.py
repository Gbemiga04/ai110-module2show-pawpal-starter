from datetime import time

from pawpal_system import Pet, Task


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
