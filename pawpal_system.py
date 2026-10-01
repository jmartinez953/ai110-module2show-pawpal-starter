from dataclasses import dataclass, field
from datetime import datetime, timedelta



@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: int
    frequency: str = "once"
    completed_at: datetime | None = None
    scheduled_start: datetime | None = None
    def mark_complete(self) -> None:
        """Record the current date and time as the task's completion time."""
        self.completed_at = datetime.now()

    def is_completed(self) -> bool:
        """Return whether the task has a recorded completion time."""
        return self.completed_at is not None 
    
    def next_due_date(self) -> datetime | None:
        """Calculate the next due date for a completed recurring task."""
        # Unfinished tasks and one-time tasks do not generate a next due date.
        if self.completed_at is None or self.frequency == "once":
            return None
        # Convert the frequency into days and count forward from completion.
        intervals = {"daily": 1, "weekly": 7}
        days = intervals[self.frequency]
        next_date = self.completed_at + timedelta(days=days)
        # Keep the original scheduled clock time on the new date.
        if self.scheduled_start is not None:
            next_date = datetime.combine(
                next_date.date(),
                self.scheduled_start.time(),
            )

        return next_date

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
    def sort_by_time(self) -> list[tuple[Pet, Task]]:
        
        """Return the daily plan sorted by start time, with unscheduled tasks last."""
        # Return a new sorted list without changing the original daily plan.
        # Each pair contains a Pet at position 0 and a Task at position 1.
        # The key puts scheduled tasks first, then orders them by start time.
        # Missing start times use datetime.max as a comparison placeholder.
        return sorted(
            self.daily_plan,
            key=lambda pair: (
                pair[1].scheduled_start is None,
                pair[1].scheduled_start or datetime.max,
            ),
        )



    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Return tasks matching the optional pet name and completion status."""
        matches = []
        requested_name = pet_name.strip().casefold() if pet_name is not None else None

                # Visit each pet and its task, one pair at a time.
        for pet, task in self.owner.get_all_tasks():
            # If a name was requested, skip pets whose names do not match.
            if requested_name is not None and pet.name.casefold() != requested_name:
                continue

            # If a completion status was requested, skip tasks with a different status.
            if completed is not None and task.is_completed() != completed:
                continue

            # This pair passed both checks, so include it in the results.
            matches.append((pet, task))

        # After checking every pair, return all the matches.
        return matches



    
    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Complete a pet's task and add its next occurrence when recurring."""
        # Check that this exact Task object belongs to the selected pet.
        if not any(existing is task for existing in pet.tasks):
            raise ValueError("This task does not belong to the selected pet.")
        # Stop if already completed so repeated calls cannot create duplicates.
        if task.is_completed():
            return

        if task.frequency not in {"once", "daily", "weekly"}:
            raise ValueError("Frequency must be once, daily, or weekly.")
        # Keep the original task as a completed record and calculate its next date.
        task.mark_complete()
        next_start = task.next_due_date()

        # Create a separate unfinished task for the next recurring occurrence.
        if next_start is not None:
            next_task = Task(
                name=task.name,
                category=task.category,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                scheduled_start=next_start,
            )
            pet.add_task(next_task)





    def detect_conflicts(self) -> list[str]:
        """Return warnings for overlapping unfinished tasks across all pets."""
        # Build a list of pet-task pairs that need conflict checking.
        # Include only unfinished tasks with a scheduled start time.
        scheduled = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.scheduled_start is not None
            and not task.is_completed()
        ]
        warnings = []
        # Choose each scheduled task as the first task in a comparison.
        for index, (pet_a, task_a) in enumerate(scheduled):
            start_a = task_a.scheduled_start
            end_a = start_a + timedelta(minutes=task_a.duration_minutes)

            # Compare only with later entries to avoid self-comparisons and duplicate pairs.
            for pet_b, task_b in scheduled[index + 1:]:
                start_b = task_b.scheduled_start
                end_b = start_b + timedelta(minutes=task_b.duration_minutes)

                # Both tasks must start before the other ends to overlap.
                # A task starting exactly when another ends is allowed.
                if start_a < end_b and start_b < end_a:
                    warnings.append(
                        f"Conflict: {pet_a.name}'s {task_a.name} "
                        f"({start_a:%Y-%m-%d %H:%M} to {end_a:%H:%M}) "
                        f"overlaps with {pet_b.name}'s {task_b.name} "
                        f"({start_b:%Y-%m-%d %H:%M} to {end_b:%H:%M})."
                    )
        # Return the collected messages; an empty list means no conflicts were found.
        return warnings