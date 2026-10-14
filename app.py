from datetime import time
from pathlib import Path

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

DATA_FILE = Path(__file__).with_name("data.json")


def save_owner_name() -> None:
    """Persist the edited owner name with the current pet data."""
    current_owner: Owner = st.session_state["owner"]
    current_owner.name = st.session_state["owner_name"]
    current_owner.save_to_json(DATA_FILE)


if "owner" not in st.session_state:
    st.session_state["owner"] = (
        Owner.load_from_json(DATA_FILE) if DATA_FILE.exists() else Owner(name="Jordan")
    )
owner: Owner = st.session_state["owner"]
st.session_state.setdefault("owner_name", owner.name)

st.title("🐾 PawPal+")
st.markdown(
    """
PawPal+ helps you keep track of pet care tasks and organize them into a daily schedule.
Add your pets and their care tasks below.
"""
)

st.text_input("Owner name", key="owner_name", on_change=save_owner_name)

st.subheader("Add a pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if not pet_name.strip():
        st.error("Enter a name for your pet.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species))
        owner.save_to_json(DATA_FILE)
        st.success(f"Added {pet_name.strip()}!")

st.subheader("Your pets")
if not owner.pets:
    st.info("No pets yet. Add a pet above to get started.")
else:
    selected_pet_index = st.selectbox(
        "Choose a pet",
        options=range(len(owner.pets)),
        format_func=lambda index: (
            f"{owner.pets[index].name} ({owner.pets[index].species})"
        ),
    )
    selected_pet = owner.pets[selected_pet_index]

    st.markdown(f"### Care tasks for {selected_pet.name}")
    with st.form("add_task_form", clear_on_submit=True):
        task_description = st.text_input("Task description")
        task_time = st.time_input("Time", value=time(8, 0))
        task_frequency = st.selectbox(
            "Frequency", ["daily", "weekly", "as needed"]
        )
        duration_minutes = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        add_task = st.form_submit_button("Add task")

    if add_task:
        if not task_description.strip():
            st.error("Enter a description for the task.")
        else:
            selected_pet.add_task(
                Task(
                    description=task_description.strip(),
                    time=task_time,
                    frequency=task_frequency,
                    duration_minutes=int(duration_minutes),
                    priority=priority,
                )
            )
            owner.save_to_json(DATA_FILE)
            st.success(f"Added task for {selected_pet.name}.")

    for pet_index, pet in enumerate(owner.pets):
        with st.expander(f"{pet.name} ({pet.species})"):
            for task_index, task in enumerate(pet.tasks):
                if not task.completed and st.button(
                    f"Mark complete: {task.description}",
                    key=f"complete_{pet_index}_{task_index}",
                ):
                    next_task = Scheduler(owner).mark_task_completed(task)
                    owner.save_to_json(DATA_FILE)
                    if next_task is not None:
                        st.success(
                            f"Completed {task.description}. Next occurrence: "
                            f"{next_task.due_date.isoformat()}."
                        )
                    else:
                        st.success(f"Completed {task.description}.")

            if pet.tasks:
                st.table(
                    [
                        {
                            "Task": task.description,
                            "Due date": task.due_date.isoformat(),
                            "Time": task.time.strftime("%I:%M %p"),
                            "Frequency": task.frequency,
                            "Duration (minutes)": task.duration_minutes,
                            "Priority": {
                                "high": "🔴 High",
                                "medium": "🟡 Medium",
                                "low": "🟢 Low",
                            }[task.priority],
                            "Status": "✅ Complete" if task.completed else "⏳ Pending",
                        }
                        for task in pet.tasks
                    ]
                )
            else:
                st.write("No care tasks yet.")

    st.subheader("Find an open time")
    requested_duration = st.number_input(
        "Desired task duration (minutes)",
        min_value=1,
        max_value=240,
        value=20,
        key="slot_duration",
    )
    if st.button("Find next available slot"):
        next_slot = Scheduler(owner).find_next_available_slot(
            int(requested_duration)
        )
        if next_slot is None:
            st.warning("No open slot of that length is available between 6 AM and 10 PM.")
        else:
            st.success(f"Next available time today: {next_slot.strftime('%I:%M %p')}.")

    st.subheader("Today's schedule")
    if st.button("Generate schedule"):
        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning(
                "Some care tasks overlap. Review the tasks below and adjust "
                "their times or durations to avoid conflicts."
            )
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No task conflicts detected.")

        schedule = scheduler.organize_tasks()
        if schedule:
            st.table(
                [
                    {
                        "Time": task.time.strftime("%I:%M %p"),
                        "Pet": pet.name,
                        "Task": task.description,
                        "Duration (minutes)": task.duration_minutes,
                        "Priority": {
                            "high": "🔴 High",
                            "medium": "🟡 Medium",
                            "low": "🟢 Low",
                        }[task.priority],
                    }
                    for pet, task in schedule
                ]
            )
        else:
            st.info("No pending tasks to schedule.")
