"""Core data models and scheduling interfaces for PawPal+."""

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Owner:
    """An owner and their pet-care preferences."""

    name: str
    preferences: list[str] = field(default_factory=list)
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to this owner's care."""
        raise NotImplementedError

    def update_preferences(self, preferences: list[str]) -> None:
        """Replace this owner's care preferences."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet and the care tasks and plans associated with them."""

    name: str
    species: str
    care_tasks: list["CareTask"] = field(default_factory=list)
    daily_plans: list["DailyPlan"] = field(default_factory=list)

    def add_task(self, task: "CareTask") -> None:
        """Add a care task for this pet."""
        raise NotImplementedError

    def update_task(self, task: "CareTask") -> None:
        """Update a care task for this pet."""
        raise NotImplementedError


@dataclass
class CareTask:
    """A pet-care activity with a duration and priority."""

    title: str
    category: str
    duration_minutes: int
    priority: str

    def update_details(
        self, title: str, duration_minutes: int, priority: str
    ) -> None:
        """Update the task's title, duration, and priority."""
        raise NotImplementedError


@dataclass
class DailyPlan:
    """A daily schedule containing selected care tasks."""

    plan_date: date
    available_minutes: int
    scheduled_tasks: list[CareTask] = field(default_factory=list)
    start_times: dict[str, time] = field(default_factory=dict)

    def generate(
        self,
        pet: Pet,
        available_minutes: int,
        preferences: list[str],
    ) -> None:
        """Build a plan for a pet within the available time."""
        raise NotImplementedError

    def explain(self) -> str:
        """Explain why tasks were selected and when they are scheduled."""
        raise NotImplementedError
