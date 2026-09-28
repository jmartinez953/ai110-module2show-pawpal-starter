from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: int
    frequency: str = "once"
    completed_at: datetime | None = None

    def mark_complete(self) -> None:
        """Record the current date and time as the task's completion time."""
        self.completed_at = datetime.now()

    def is_completed(self) -> bool:
        """Return whether the task has a recorded completion time."""
        return self.completed_at is not None 


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a caretask to the pet's list of tasks."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet's list of tasks if it is present."""
        if task in self.tasks:
            self.tasks.remove(task)

    def has_been_fed_today(self) -> bool:

        """Return whether at least one feeding task has been completed today."""
        today = datetime.now().date()

        for task in self.tasks:
            if (
                task.category == "feeding"
                and task.completed_at is not None
                and task.completed_at.date() == today
            ):
                return True

        return False
    def has_been_walked_today(self) -> bool:
        """Return whether at least one walking task has been completed today."""
        today = datetime.now().date()

        for task in self.tasks:
            if (
                task.category == "walking"
                and task.completed_at is not None
                and task.completed_at.date() == today
            ):
                return True

        return False


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict[str, str] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet) 

    def set_available_time(self, minutes: int) -> None:
        """Set the owner's available time for pet care tasks, rejecting negative values."""
        if minutes < 0:
            raise ValueError("Available time cannot be negative.")
        self.available_minutes = minutes

    def update_preferences(self, preferences: dict[str, str]) -> None:
        """Update/add the owner's preferences while keeping unspecified preferences."""
        self.preferences.update(preferences)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return a list of tasks for each pet and their associated tasks, including completed tasks."""
        all_tasks = []

        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))

        return all_tasks

class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Initialize the Scheduler with an Owner instance and initialize an empty daily plan."""
        self.owner = owner
        self.daily_plan: list[tuple[Pet, Task]] = []

    def generate_plan(self) -> None:
        """Rebuild the daily plan with unfinished tasks paired with their pets"""
        self.daily_plan = []

        for pet, task in self.owner.get_all_tasks():
            if task.completed_at is None:
                self.daily_plan.append((pet, task))

    def explain_plan(self) -> str:
        """Return a readable explanation of the current daily plan."""
        if not self.daily_plan:
            return "The daily plan is empty. No tasks are scheduled."
        lines = ["These tasks were included because they are unfinished."]
        for pet, task in self.daily_plan:
            lines.append(f"- {pet.name}: {task.name}")
        return "\n".join(lines) 
    