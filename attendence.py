import streamlit as st
import os

USERS = "users.txt"
ATTENDANCE = "attendance.txt"

st.title("Attendance Management System")

if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# --- Login ---
if not st.session_state.user:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = None
        if os.path.exists(USERS):
            for line in open(USERS):
                r, u, p = line.strip().split(",")
                if u == username and p == password:
                    role = r
                    break

        if role:
            st.session_state.user = username
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid credentials")

# --- After Login ---
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # === FACULTY ===
    if st.session_state.role == "faculty":
        menu = st.sidebar.radio("Menu", ["Add Student", "Mark Attendance", "View Attendance", "Search Student", "Filter By Date"])

        if menu == "Add Student":
            name = st.text_input("Student Name")
            pwd = st.text_input("Password")
            if st.button("Add") and name and pwd:
                with open(USERS, "a") as f:
                    f.write(f"student,{name},{pwd}\n")
                st.success("Student added!")

        elif menu == "Mark Attendance":
            name = st.text_input("Student Name")
            date = st.date_input("Date")
            status = st.radio("Status", ["P", "A"])
            if st.button("Submit") and name:
                with open(ATTENDANCE, "a") as f:
                    f.write(f"{name},{date},{status}\n")
                st.success("Attendance saved!")

        elif menu == "View Attendance":
            if os.path.exists(ATTENDANCE):
                for line in open(ATTENDANCE):
                    st.write(line.strip())
            else:
                st.warning("No records found")

        elif menu == "Search Student":
            search = st.text_input("Student Name")
            if search and os.path.exists(ATTENDANCE):
                results = [l.strip() for l in open(ATTENDANCE) if search.lower() in l.lower()]
                for r in results:
                    st.write(r)

        elif menu == "Filter By Date":
            date = str(st.date_input("Select Date"))
            if os.path.exists(ATTENDANCE):
                for line in open(ATTENDANCE):
                    if date in line:
                        st.write(line.strip())

    # === STUDENT ===
    else:
        st.header(f"Welcome, {st.session_state.user}")
        total = present = 0

        if os.path.exists(ATTENDANCE):
            for line in open(ATTENDANCE):
                name, date, status = line.strip().split(",")
                if name.lower() == st.session_state.user.lower():
                    st.write(f"{date} - {status}")
                    total += 1
                    present += (status == "P")

        if total > 0:
            st.success(f"Attendance: {present}/{total} ({present/total*100:.1f}%)")
        else:
            st.warning("No attendance records found")
