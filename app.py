import streamlit as st
import pandas as pd
import os
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Productivity Coach", layout="centered")

st.title("🧠 AI Productivity Coach")
st.write("Plan tasks, track progress, and get smart productivity insights.")

# ---------------- FILE SETUP ----------------
FILE = "tasks.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Date", "Task", "Priority", "Status"])
    df.to_csv(FILE, index=False)

df = pd.read_csv(FILE)

# ---------------- ADD TASK ----------------
st.subheader("➕ Add New Task")

task_date = st.date_input("Task Date", date.today())
task_name = st.text_input("Task Name")
priority = st.selectbox("Priority", ["High", "Medium", "Low"])

if st.button("Add Task"):
    if task_name.strip() == "":
        st.warning("Please enter a task.")
    else:
        new_task = {
            "Date": task_date,
            "Task": task_name,
            "Priority": priority,
            "Status": "Pending"
        }
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Task added successfully!")

# ---------------- UPDATE TASK STATUS ----------------
st.subheader("✅ Update Task Status")

if not df.empty:
    task_index = st.selectbox("Select Task", df.index)
    new_status = st.selectbox("Status", ["Pending", "Completed"])

    if st.button("Update Status"):
        df.loc[task_index, "Status"] = new_status
        df.to_csv(FILE, index=False)
        st.success("Task updated!")

# ---------------- PRODUCTIVITY ANALYSIS ----------------
st.subheader("📊 Productivity Dashboard")

total_tasks = len(df)
completed_tasks = len(df[df["Status"] == "Completed"])

if total_tasks > 0:
    productivity_score = int((completed_tasks / total_tasks) * 100)
else:
    productivity_score = 0

st.metric("Productivity Score (%)", productivity_score)

# Smart AI-like suggestions
if productivity_score >= 80:
    st.success("🔥 Excellent productivity! Keep it up.")
elif productivity_score >= 50:
    st.info("🙂 Good progress. Try focusing on high-priority tasks.")
else:
    st.warning("⚠️ Low productivity. Break tasks into smaller steps.")

# ---------------- TASK TABLE ----------------
st.write("### 📋 All Tasks")
st.dataframe(df)
