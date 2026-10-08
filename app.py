import streamlit as st 
# Combine the date and time chosen by the owner into a task's start datetime.
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Add pets and care tasks, filter your task list, and view scheduled tasks in time order with overlap warnings.
"""
)

st.divider()

st.subheader("Owner and pets")
owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name,
        available_minutes=60,
    )

owner = st.session_state.owner
owner.name = owner_name
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])



if st.button("Add pet"):
    if pet_name.strip():
        pet = Pet(name=pet_name.strip(), species=species)
        owner.add_pet(pet)
        st.success(f"Added pet: {pet.name}")
    else:
        st.warning("Please enter a valid pet name.")

st.subheader("Your pets")

if owner.pets:
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")
        



st.markdown("### Tasks")
st.caption("Add care tasks with a date and start time.")
selected_pet_index = st.selectbox(
    "Choose a pet for this task",
    options=range(len(owner.pets)),
    format_func=lambda index: (
        f"{index + 1}. {owner.pets[index].name} "
        f"({owner.pets[index].species})"
    ),
)


category = st.selectbox(
    "Task category",
    ["walking", "feeding", "grooming", "medication", "other"],
)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# Let the owner choose when this task should begin.
scheduled_date = st.date_input("Task date")
scheduled_time = st.time_input("Task start time", value="08:00")


if st.button("Add task"):
    if selected_pet_index is None:
        st.warning("Please add a pet first.")
    elif not task_title.strip():
        st.warning("Please enter a task title.")
    else:
        priority_values = {"high": 1, "medium": 2, "low": 3}

        task = Task(
            name=task_title.strip(),
            category=category,
            duration_minutes=int(duration),
            priority=priority_values[priority],
            # Combine the selected date and time into this task's scheduled start.
            scheduled_start=datetime.combine(scheduled_date, scheduled_time),
        )

        selected_pet = owner.pets[selected_pet_index]
        selected_pet.add_task(task)
        st.success(f"Added {task.name} for {selected_pet.name}!")


# A blank name includes all pets; a name limits the report to matching pets.
pet_name_filter = st.text_input(
    "Filter by pet name",
    help="Leave blank to show all pets. Names are matched without regard to capitalization.",
)

# Let the owner choose which completion statuses appear in the report.
status_choice = st.selectbox(
    "Show tasks",
    ["All tasks", "Unfinished", "Completed"],
)

# Translate the displayed choice into the backend's optional Boolean filter.
status_filters = {
    "All tasks": None,
    "Unfinished": False,
    "Completed": True,
}

# Retrieve matching tasks and pass them to the existing table below.
report_scheduler = Scheduler(owner)

# Pass both filters to Scheduler; None means no pet-name restriction.
all_tasks = report_scheduler.filter_tasks(
    pet_name=pet_name_filter.strip() or None,
    completed=status_filters[status_choice],
)





if all_tasks:
    st.write("Current tasks:")
    task_rows = []

    for pet, task in all_tasks:
        task_rows.append({
            "Pet": pet.name,
            "Task": task.name,
            # Show the completion status used by the report filter.
            "Status": "Completed" if task.is_completed() else "Unfinished",
            # Show the date and time; older tasks may have no scheduled start.
            "Scheduled start": (
                task.scheduled_start.strftime("%Y-%m-%d %H:%M")
                if task.scheduled_start is not None
                else "Unscheduled"),
            "Category": task.category,
            "Duration (minutes)": task.duration_minutes,
            "Priority": task.priority,
        })

    st.table(task_rows)
else:
    # An empty result may mean existing tasks did not match the filters.
    st.info("No tasks match the selected filters.")

st.divider()

st.subheader("Build Schedule")
st.caption("Show unfinished tasks in scheduled date and time order.")

if st.button("Generate schedule"):
    # Collect the owner's unfinished tasks, then sort them by start time.
    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    sorted_tasks = scheduler.sort_by_time()

    if sorted_tasks:
        schedule_rows = []

        # Turn each sorted pet-task pair into a readable table row.
        for pet, task in sorted_tasks:
            schedule_rows.append({
                "Pet": pet.name,
                "Task": task.name,
                "Scheduled start": (
                    task.scheduled_start.strftime("%Y-%m-%d %H:%M")
                    if task.scheduled_start is not None
                    else "Unscheduled"
                ),
                "Duration (minutes)": task.duration_minutes,
                "Priority": task.priority,
                "Status": "Completed" if task.is_completed() else "Unfinished", 
            })

        st.table(schedule_rows)

        # Check unfinished tasks across all pets for overlapping times.
        conflicts = scheduler.detect_conflicts()

        if conflicts:
            # Display each conflicting pair so the owner can identify it.
            for message in conflicts:
                st.warning(message)
        else:
            st.success("No time overlaps found among scheduled unfinished tasks.")


    else:
        st.info("No unfinished tasks to schedule.")
