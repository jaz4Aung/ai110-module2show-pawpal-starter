import streamlit as st

from owner import Owner
from pet import Pet
from scheduler import Scheduler
from task import Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**. Use the form below to add tasks, set how much time you have,
and generate a schedule with the built-in scheduler.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What the scheduler does", expanded=False):
    st.markdown(
        """
- Sorts tasks by **priority** (high → medium → low), then by your **preferred task order**
  when priorities tie.
- **Packs** tasks greedily into your **available minutes** until the budget runs out.
- Lists anything that did not fit under **Not scheduled**.
"""
    )

st.divider()

st.subheader("Owner & pet")
col_a, col_b = st.columns(2)
with col_a:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_b:
    available_minutes = st.number_input(
        "Available minutes (today)", min_value=1, max_value=1440, value=120
    )

col_c, col_d = st.columns(2)
with col_c:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_d:
    species = st.selectbox("Species", ["dog", "cat", "other"])

preferred_raw = st.text_area(
    "Preferred task order (optional)",
    height=100,
    placeholder="One task title per line, most preferred first.\nExample:\nMorning walk\nFeed breakfast",
    help="Used to break ties when two tasks have the same priority.",
)

st.markdown("### Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build schedule")

if "last_plan" not in st.session_state:
    st.session_state.last_plan = None

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task first.")
        st.session_state.last_plan = None
    else:
        preferred_task_order = [
            line.strip() for line in preferred_raw.splitlines() if line.strip()
        ]
        owner = Owner(owner_name, int(available_minutes), preferred_task_order)
        pet = Pet(pet_name, species)
        task_objs = [
            Task(t["title"], t["duration_minutes"], t["priority"])
            for t in st.session_state.tasks
        ]
        st.session_state.last_plan = Scheduler().schedule(owner, pet, task_objs)

if st.session_state.last_plan is not None:
    plan = st.session_state.last_plan
    st.success(plan.summary)

    if plan.scheduled_items:
        rows = []
        for item in plan.scheduled_items:
            rows.append(
                {
                    "#": item.order,
                    "Task": item.task.title,
                    "Start (min)": item.start_minute,
                    "Duration (min)": item.task.duration_minutes,
                    "Priority": item.task.priority,
                    "Why": item.reason,
                }
            )
        st.markdown("**Scheduled**")
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Nothing was scheduled (check your time budget and tasks).")

    if plan.not_scheduled:
        st.markdown("**Not scheduled** (did not fit the budget)")
        st.table(
            [
                {
                    "title": t.title,
                    "duration_minutes": t.duration_minutes,
                    "priority": t.priority,
                }
                for t in plan.not_scheduled
            ]
        )
