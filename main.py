
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


owner = Owner(name="Juan", available_minutes=60)

dog = Pet(name= "Buddy", species="dog")
cat = Pet(name = "Luna", species = "cat")


owner.add_pet(dog)
owner.add_pet(cat)

walk = Task(
    name="Morning walk",
    category="walking",
    duration_minutes=30,
    priority=2,
    scheduled_start=datetime(2026, 10, 1, 9, 0),
)

feeding = Task(
    name="Morning Feed",
    category="feeding",
    duration_minutes=10,
    priority=1,
    frequency="daily",
    scheduled_start=datetime.now().replace(
    hour=8, minute=0, second=0, microsecond=0),

)

grooming = Task(
    name="Brush fur",
    category="grooming",
    duration_minutes=15,
    priority=3,
    frequency="weekly",
    scheduled_start=datetime.now().replace(hour=8, minute=30, second=0, microsecond=0),
)

dog.add_task(walk)
dog.add_task(feeding)
cat.add_task(grooming)

scheduler = Scheduler(owner)
scheduler.generate_plan()



print("Scheduled tasks")
print("---------------------------")

for pet, task in scheduler.sort_by_time():
    start_time = (
        task.scheduled_start.strftime("%Y-%m-%d %H:%M")
        if task.scheduled_start is not None
        else "Unscheduled"
    )
    print(
        f"{start_time} - {pet.name}: {task.name} "
        f"({task.duration_minutes} minutes)"
    )


print("\nBuddy's tasks")
print("-------------")

for pet, task in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"{pet.name}: {task.name}")



scheduler.mark_task_complete(dog, feeding)

print("\nCompleted tasks")
print("---------------")

for pet, task in scheduler.filter_tasks(completed=True):
    print(f"{pet.name}: {task.name}")


print("\nUnfinished tasks")
print("----------------")

for pet, task in scheduler.filter_tasks(completed=False):
    print(f"{pet.name}: {task.name}")



print("\nFeeding occurrences")
print("-------------------")

for pet, task in scheduler.filter_tasks(pet_name=dog.name):
    if task.category == "feeding":
        due = (
            task.scheduled_start.strftime("%Y-%m-%d %H:%M")
            if task.scheduled_start is not None
            else "Unscheduled"
        )
        status = "Completed" if task.is_completed() else "Unfinished"
        print(f"{pet.name}: {task.name} | {due} | {status}")



scheduler.mark_task_complete(cat, grooming)

print("\nGrooming occurrences")
print("--------------------")

for pet, task in scheduler.filter_tasks(pet_name=cat.name):
    if task.category == "grooming":
        due = (
            task.scheduled_start.strftime("%Y-%m-%d %H:%M")
            if task.scheduled_start is not None
            else "Unscheduled"
        )
        status = "Completed" if task.is_completed() else "Unfinished"
        print(f"{pet.name}: {task.name} | {due} | {status}")



overlapping_task = Task(
    name="Grooming appointment",
    category="grooming",
    duration_minutes=20,
    priority=2,
    scheduled_start=walk.scheduled_start,
)

cat.add_task(overlapping_task)


print("\nConflict warnings")
print("-----------------")

warnings = scheduler.detect_conflicts()

if warnings:
    for warning in warnings:
        print(warning)
else:
    print("No scheduling conflicts found.")