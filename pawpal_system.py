"""Core data models and task management for PawPal+."""

from dataclasses import dataclass, field
from datetime import time as TimeOfDay


@dataclass
class Task:
    """A recurring pet-care activity scheduled for a time of day."""

    description: str
    time: TimeOfDay
    frequency: str
    duration_minutes: int
    priority: str
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate the task's required fields."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if not isinstance(self.time, TimeOfDay):
            raise TypeError("Task time must be a datetime.time value.")
        if not self.frequency.strip():
            raise ValueError("Task frequency cannot be empty.")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("Task priority must be low, medium, or high.")

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def mark_completed(self) -> None:
        """Mark this task as complete."""
        self.mark_complete()

    def mark_pending(self) -> None:
        """Mark this task as not yet complete."""
        self.completed = False


@dataclass
class Pet:
    """A pet and its care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        if not isinstance(task, Task):
            raise TypeError("task must be a Task instance.")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet by object identity."""
        for index, existing_task in enumerate(self.tasks):
            if existing_task is task:
                del self.tasks[index]
                return
        raise ValueError(f"Task does not belong to pet {self.name!r}.")

    def get_tasks(self) -> list[Task]:
        """Return a copy of this pet's task list."""
        return self.tasks.copy()


@dataclass
class Owner:
    """An owner who manages multiple pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        if not isinstance(pet, Pet):
            raise TypeError("pet must be a Pet instance.")
        if any(existing_pet is pet for existing_pet in self.pets):
            raise ValueError(f"Pet {pet.name!r} is already registered.")
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner by object identity."""
        for index, existing_pet in enumerate(self.pets):
            if existing_pet is pet:
                del self.pets[index]
                return
        raise ValueError(f"Pet {pet.name!r} does not belong to owner {self.name!r}.")

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks belonging to this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    """Retrieves, organizes, and manages tasks for an owner's pets."""

    owner: Owner

    def __post_init__(self) -> None:
        """Ensure the scheduler has a valid owner."""
        if not isinstance(self.owner, Owner):
            raise TypeError("owner must be an Owner instance.")

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> list[Task]:
        """Retrieve tasks that have not been completed."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def get_completed_tasks(self) -> list[Task]:
        """Retrieve tasks that have been completed."""
        return [task for task in self.get_all_tasks() if task.completed]

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Retrieve tasks for a pet registered to this owner."""
        if not any(owned_pet is pet for owned_pet in self.owner.pets):
            raise ValueError(
                f"Pet {pet.name!r} does not belong to owner {self.owner.name!r}."
            )
        return pet.get_tasks()

    def organize_tasks(
        self, include_completed: bool = False
    ) -> list[tuple[Pet, Task]]:
        """Return the owner's tasks ordered by time, pet name, and description."""
        pet_tasks = [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if include_completed or not task.completed
        ]
        return sorted(
            pet_tasks,
            key=lambda item: (
                item[1].time,
                {"high": 0, "medium": 1, "low": 2}[item[1].priority],
                item[0].name.casefold(),
                item[1].description.casefold(),
            ),
        )

    def mark_task_completed(self, task: Task) -> None:
        """Mark a task belonging to this owner as complete."""
        if not any(owned_task is task for owned_task in self.get_all_tasks()):
            raise ValueError("Task does not belong to this owner's pets.")
        task.mark_complete()

    def mark_task_pending(self, task: Task) -> None:
        """Mark a task belonging to this owner as not yet complete."""
        if not any(owned_task is task for owned_task in self.get_all_tasks()):
            raise ValueError("Task does not belong to this owner's pets.")
        task.mark_pending()
