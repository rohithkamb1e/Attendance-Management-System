import streamlit as st
import os

students = "students.txt"
attendance = "attendance.txt"

st.title("Attendance Management System")

menu = st.sidebar.radio(
    "Menu",
    ["Add Student", "View Students", "Mark Attendance",
     "View Attendance", "Attendance %"]
)

# Add Student
if menu == "Add Student":
    name = st.text_input("Student Name")

    if st.button("Add"):
        with open(students, "a") as file:
            file.write(name + "\n")

        st.success("Student Added")

# View Students
elif menu == "View Students":
    if os.path.exists(students):
        with open(students, "r") as file:
            for line in file:
                st.write(line.strip())
    else:
        st.warning("No Students Found")

# Mark Attendance
elif menu == "Mark Attendance":
    name = st.text_input("Student Name")
    date = st.date_input("Date")
    status = st.radio("Status", ["P", "A"])

    if st.button("Submit"):
        with open(attendance, "a") as file:
            file.write(f"{name},{date},{status}\n")

        st.success("Attendance Marked")

# View Attendance
elif menu == "View Attendance":
    if os.path.exists(attendance):
        with open(attendance, "r") as file:
            for line in file:
                st.write(line.strip())
    else:
        st.warning("No Attendance Records")

# Attendance Percentage
elif menu == "Attendance %":
    name = st.text_input("Student Name")

    if st.button("Calculate"):
        total = 0
        present = 0

        if os.path.exists(attendance):
            with open(attendance, "r") as file:
                for line in file:
                    row = line.strip().split(",")

                    if row[0].lower() == name.lower():
                        total += 1

                        if row[2] == "P":
                            present += 1

        if total > 0:
            percentage = (present / total) * 100
            st.success(f"Attendance Percentage: {percentage:.2f}%")
        else:
            st.error("No Records Found")