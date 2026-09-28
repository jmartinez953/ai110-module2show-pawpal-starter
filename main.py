from pawpal_system import Owner, Pet, Task, Scheduler


owner = Owner(name="Juan", available_minutes=60)

dog = Pet(name= "Buddy", species="dog")
cat = Pet(name = "Luna", species = "cat")


owner.add_pet(dog)
owner.add_pet(cat)


walk = Task(name="Morning walk", category= "walking", duration_minutes=30, priority=2)

feeding = Task(name="Morning Feed", category="feeding", duration_minutes=10, priority=1)

grooming = Task(name="Brush fur", category="grooming", duration_minutes=15, priority=3)

dog.add_task(walk)
dog.add_task(feeding)
cat.add_task(grooming)

scheduler = Scheduler(owner)
scheduler.generate_plan()




print("Today's schedule")
print("-----------------")
for pet, task in scheduler.daily_plan:
    print(f"{pet.name} ({pet.species}) - {task.name} ({task.category}) - Duration: {task.duration_minutes} minutes - Priority: {task.priority}")