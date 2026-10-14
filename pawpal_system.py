"""Core data models and task management for PawPal+."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, time as TimeOfDay, timedelta
from pathlib import Path


def _require_json_object(value: object, field_name: str) -> dict[str, object]:
    """Return a decoded JSON object or raise a field-specific error."""
    if not isinstance(value, dict):
        raise ValueError(f"Expected {field_name} to be a JSON object.")
    return value


def _require_json_string(value: object, field_name: str) -> str:
    """Return a decoded JSON string or raise a field-specific error."""
    if not isinstance(value, str):
        raise ValueError(f"Expected {field_name} to be a string.")
    return value


@dataclass
class Task:
    """A recurring pet-care activity scheduled for a time of day."""

    description: str
    time: TimeOfDay
    frequency: str
    duration_minutes: int
    priority: str
    due_date: date = field(default_factory=date.today)
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
        if not isinstance(self.due_date, date):
            raise TypeError("Task due_date must be a datetime.date value.")

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

    def save_to_json(self, path: str | Path) -> None:
        """Save this owner, pets, and tasks as readable JSON."""
        data = {
            "name": self.name,
            "pets": [
                {
                    "name": pet.name,
                    "species": pet.species,
                    "tasks": [
                        {
                            "description": task.description,
                            "time": task.time.isoformat(),
                            "frequency": task.frequency,
                            "duration_minutes": task.duration_minutes,
                            "priority": task.priority,
                            "due_date": task.due_date.isoformat(),
                            "completed": task.completed,
                        }
                        for task in pet.tasks
                    ],
                }
                for pet in self.pets
            ],
        }
        Path(path).write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def load_from_json(cls, path: str | Path) -> Owner:
        """Load an owner, pets, and tasks from the PawPal JSON format."""
        data = _require_json_object(
            json.loads(Path(path).read_text(encoding="utf-8")), "root"
        )
        owner_name = _require_json_string(data.get("name"), "owner name")
        pets_data = data.get("pets")
        if not isinstance(pets_data, list):
            raise ValueError("Expected pets to be a JSON array.")

        owner = cls(owner_name)
        for pet_index, pet_value in enumerate(pets_data):
            pet_data = _require_json_object(pet_value, f"pets[{pet_index}]")
            pet_name = _require_json_string(
                pet_data.get("name"), f"pets[{pet_index}].name"
            )
            species = _require_json_string(
                pet_data.get("species"), f"pets[{pet_index}].species"
            )
            tasks_data = pet_data.get("tasks")
            if not isinstance(tasks_data, list):
                raise ValueError(f"Expected pets[{pet_index}].tasks to be a JSON array.")

            pet = Pet(pet_name, species)
            for task_index, task_value in enumerate(tasks_data):
                task_field = f"pets[{pet_index}].tasks[{task_index}]"
                task_data = _require_json_object(task_value, task_field)
                description = _require_json_string(
                    task_data.get("description"), f"{task_field}.description"
                )
                scheduled_time = _require_json_string(
                    task_data.get("time"), f"{task_field}.time"
                )
                frequency = _require_json_string(
                    task_data.get("frequency"), f"{task_field}.frequency"
                )
                duration = task_data.get("duration_minutes")
                if type(duration) is not int:
                    raise ValueError(f"Expected {task_field}.duration_minutes to be an integer.")
                priority = _require_json_string(
                    task_data.get("priority"), f"{task_field}.priority"
                )
                due_date = _require_json_string(
                    task_data.get("due_date"), f"{task_field}.due_date"
                )
                completed = task_data.get("completed")
                if type(completed) is not bool:
                    raise ValueError(f"Expected {task_field}.completed to be a boolean.")

                pet.add_task(
                    Task(
                        description=description,
                        time=TimeOfDay.fromisoformat(scheduled_time),
                        frequency=frequency,
                        duration_minutes=duration,
                        priority=priority,
                        due_date=date.fromisoformat(due_date),
                        completed=completed,
                    )
                )
            owner.add_pet(pet)
        return owner


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

    def sort_by_time(
        self, include_completed: bool = True
    ) -> list[Task]:
        """Sort all owner tasks by start time, optionally including completed tasks."""
        tasks = [
            task
            for task in self.get_all_tasks()
            if include_completed or not task.completed
        ]
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self,
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter tasks by completion status and a case-insensitive pet name."""
        normalized_pet_name = pet_name.strip().casefold() if pet_name else None
        return [
            task
            for pet in self.owner.pets
            for task in pet.tasks
            if (completed is None or task.completed is completed)
            and (
                normalized_pet_name is None
                or pet.name.casefold() == normalized_pet_name
            )
        ]

    def organize_tasks(
        self, include_completed: bool = False
    ) -> list[tuple[Pet, Task]]:
        """Sort due tasks by priority, time, pet name, then description."""
        today = date.today()
        pet_tasks = [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if task.due_date <= today
            and (include_completed or not task.completed)
        ]
        return sorted(
            pet_tasks,
            key=lambda item: (
                {"high": 0, "medium": 1, "low": 2}[item[1].priority],
                item[1].time,
                item[0].name.casefold(),
                item[1].description.casefold(),
            ),
        )

    def find_next_available_slot(
        self,
        duration_minutes: int,
        on_date: date | None = None,
        start_time: TimeOfDay = TimeOfDay(6, 0),
        end_time: TimeOfDay = TimeOfDay(22, 0),
    ) -> TimeOfDay | None:
        """Find the earliest free interval within the requested daily window."""
        if duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        if start_time >= end_time:
            raise ValueError("The scheduling window must end after it starts.")

        schedule_date = on_date or date.today()
        window_start = datetime.combine(schedule_date, start_time)
        window_end = datetime.combine(schedule_date, end_time)
        candidate = window_start
        tasks = sorted(
            (
                task
                for task in self.get_all_tasks()
                if task.due_date == schedule_date and not task.completed
            ),
            key=lambda task: task.time,
        )

        for task in tasks:
            task_start = datetime.combine(schedule_date, task.time)
            task_end = task_start + timedelta(minutes=task.duration_minutes)
            if task_end <= candidate:
                continue
            requested_end = candidate + timedelta(minutes=duration_minutes)
            if requested_end > window_end:
                return None
            if requested_end <= task_start:
                return candidate.time()
            if task_start < requested_end:
                candidate = max(candidate, task_end)
            if candidate + timedelta(minutes=duration_minutes) > window_end:
                return None

        if candidate + timedelta(minutes=duration_minutes) <= window_end:
            return candidate.time()
        return None

    def detect_conflicts(self, on_date: date | None = None) -> list[str]:
        """Warn about overlapping pending task intervals on the selected date."""
        schedule_date = on_date or date.today()
        scheduled_tasks = [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if task.due_date == schedule_date and not task.completed
        ]
        scheduled_tasks.sort(key=lambda item: item[1].time)

        warnings = []
        for index, (pet, task) in enumerate(scheduled_tasks):
            task_start = datetime.combine(schedule_date, task.time)
            task_end = task_start + timedelta(minutes=task.duration_minutes)

            for other_pet, other_task in scheduled_tasks[index + 1 :]:
                other_start = datetime.combine(schedule_date, other_task.time)
                if other_start >= task_end:
                    break

                warnings.append(
                    f"Conflict: {pet.name}'s {task.description} "
                    f"({task_start.strftime('%I:%M %p')} to "
                    f"{task_end.strftime('%I:%M %p')}) overlaps "
                    f"{other_pet.name}'s {other_task.description} "
                    f"(starts {other_task.time.strftime('%I:%M %p')})."
                )

        return warnings

    def mark_task_completed(self, task: Task, today: date | None = None) -> Task | None:
        """Complete an owned task and append its next daily or weekly occurrence."""
        pet = next(
            (
                pet
                for pet in self.owner.pets
                if any(owned_task is task for owned_task in pet.tasks)
            ),
            None,
        )
        if pet is None:
            raise ValueError("Task does not belong to this owner's pets.")
        if task.completed:
            return None

        task.mark_complete()
        recurrence = {
            "daily": timedelta(days=1),
            "weekly": timedelta(days=7),
        }.get(task.frequency.strip().casefold())
        if recurrence is None:
            return None

        next_task = Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            due_date=(today or date.today()) + recurrence,
        )
        pet.add_task(next_task)
        return next_task

    def mark_task_pending(self, task: Task) -> None:
        """Mark a task belonging to this owner as not yet complete."""
        if not any(owned_task is task for owned_task in self.get_all_tasks()):
            raise ValueError("Task does not belong to this owner's pets.")
        task.mark_pending()
