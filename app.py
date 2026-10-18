import streamlit as st
import pawpal_system
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state["owner"] = pawpal_system.Owner(owner_name)

owner = st.session_state["owner"]
owner.name = owner_name

if not owner.pets:
    owner.add_pet(pawpal_system.Pet(pet_name, species))

pet = owner.pets[0]
pet.name = pet_name
pet.species = species

st.divider()

st.subheader("Schedule a Task")
with st.form("schedule_task"):
    task_description = st.text_input("Task", value="Morning walk")
    task_time = st.time_input("Time", value=time(8, 0))
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
    submitted = st.form_submit_button("Schedule task")

if submitted:
    pet.add_task(
        pawpal_system.Task(
            description=task_description,
            time=task_time,
            frequency=frequency,
        )
    )

schedule = pawpal_system.Scheduler().organize_tasks(owner)
if schedule:
    st.write("Current schedule:")
    st.table(
        [
            {
                "Pet": pet.name,
                "Time": task.time.strftime("%H:%M"),
                "Task": task.description,
                "Frequency": task.frequency,
                "Completed": task.completed,
            }
            for task in schedule
        ]
    )
else:
    st.info("No tasks scheduled yet.")
