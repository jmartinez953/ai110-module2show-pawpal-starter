from pawpal_system import Task , Pet


def test_task_completion():
    task = Task( name = " Morning feeding", category = "feeding", duration_minutes = 10, priority = 1)

    assert task.is_completed() == False

    task.mark_complete()

    assert task.is_completed() == True
    assert task.completed_at is not None

def test_task_addition():
    pet = Pet(name="Buddy", species="dog")
    task = Task(
        name="Morning walk",
        category="walking",
        duration_minutes=30,
        priority=2,
    )
    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
    assert pet.tasks[-1] is task
    