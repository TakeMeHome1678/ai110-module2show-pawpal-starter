import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "my_owner" not in st.session_state:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "Dog", "Shiba Inu")
    luna = Pet("Luna", "Cat", "Domestic Shorthair")
    mochi.add_task(Task("Morning Walk", "07:30 AM", "daily"))
    mochi.add_task(Task("Breakfast Feeding", "08:00 AM", "daily"))
    luna.add_task(Task("Morning Feeding", "07:45 AM", "daily"))
    owner.add_pet(mochi)
    owner.add_pet(luna)
    st.session_state.my_owner = owner

owner = st.session_state.my_owner
st.title("🐾 PawPal+")

st.subheader("Your Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    breed = st.text_input("Breed (optional)")
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.error("Enter a name for your pet.")
    else:
        owner.add_pet(Pet(pet_name.strip(), species, breed.strip()))
        st.success(f"Added {pet_name.strip()} to your pets.")

pets = owner.get_pets()
if pets:
    st.table(
        [
            {"Name": pet.name, "Species": pet.species, "Breed": pet.breed or "—"}
            for pet in pets
        ]
    )
else:
    st.info("Add a pet to start scheduling care tasks.")

st.subheader("Schedule a Task")
if pets:
    with st.form("schedule_task_form", clear_on_submit=True):
        selected_pet_index = st.selectbox(
            "Pet", range(len(pets)), format_func=lambda index: pets[index].name
        )
        task_title = st.text_input("Task")
        scheduled_time = st.time_input("Time")
        recurrence = st.selectbox("Repeat", ["once", "daily", "weekly"])
        schedule_submitted = st.form_submit_button("Add task")

    if schedule_submitted:
        if not task_title.strip():
            st.error("Enter a task description.")
        else:
            selected_pet = pets[selected_pet_index]
            selected_pet.add_task(
                Task(
                    task_title.strip(),
                    scheduled_time.strftime("%I:%M %p"),
                    recurrence,
                )
            )
            st.success(f"Scheduled {task_title.strip()} for {selected_pet.name}.")

st.subheader("Complete a Task")
scheduler = Scheduler(owner)
pending_tasks = [
    (pet, task)
    for pet, task in scheduler.get_schedule()
    if task.status == "PENDING"
]
if pending_tasks:
    with st.form("complete_task_form"):
        selected_task_index = st.selectbox(
            "Task to complete",
            range(len(pending_tasks)),
            format_func=lambda index: (
                f"{pending_tasks[index][1].due_date} "
                f"{pending_tasks[index][1].scheduled_time} — "
                f"{pending_tasks[index][0].name}: {pending_tasks[index][1].title}"
            ),
        )
        completion_submitted = st.form_submit_button("Mark complete")

    if completion_submitted:
        completed_pet, completed_task = pending_tasks[selected_task_index]
        next_task = scheduler.mark_task_complete(completed_task)
        if next_task is not None:
            st.success(
                f"Completed {completed_task.title} for {completed_pet.name}. "
                f"Next occurrence: {next_task.due_date} at {next_task.scheduled_time}."
            )
        else:
            st.success(f"Completed {completed_task.title} for {completed_pet.name}.")
else:
    st.info("There are no pending tasks to complete.")

st.subheader("Schedule Conflicts")
conflicts = scheduler.check_conflicts()
if conflicts:
    for conflict in conflicts:
        st.warning(
            f"{conflict} Review the assignments and adjust one task if needed."
        )
else:
    st.success("No scheduling conflicts found.")

st.subheader("Household Schedule")
pet_filter_options = ["All pets", *[pet.name for pet in pets]]
selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options)
status_filter = st.selectbox(
    "Filter by status",
    ["All statuses", "Pending", "Completed"],
)
schedule = scheduler.filter_tasks(
    completed={
        "All statuses": None,
        "Pending": False,
        "Completed": True,
    }[status_filter],
    pet_name=None if selected_pet_filter == "All pets" else selected_pet_filter,
)
if schedule:
    st.table(
        [
            {
                "Due date": task.due_date,
                "Time": task.scheduled_time,
                "Pet": pet.name,
                "Task": task.title,
                "Repeat": task.recurrence,
                "Status": task.status,
            }
            for pet, task in schedule
        ]
    )
else:
    st.info("No tasks match those filters.")
