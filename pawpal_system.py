from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: int
    completed_at: datetime | None = None

    def mark_complete(self) -> None:
        pass

    def is_completed(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def has_been_fed_today(self) -> bool:
        pass

    def has_been_walked_today(self) -> bool:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict[str, str] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def set_available_time(self, minutes: int) -> None:
        pass

    def update_preferences(self, preferences: dict[str, str]) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.daily_plan: list[Task] = []

    def generate_plan(self) -> None:
        pass

    def explain_plan(self) -> str:
        pass
    