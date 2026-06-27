import streamlit as st
import os

USERS = "users.txt"
ATTENDANCE = "attendance.txt"

st.set_page_config(page_title="Attendance Management System")

st.title("Attendance Management System")

# ---------------- SESSION ----------------

if "user" not in st.session_state:
    st.session_state.user = ""
    st.session_state.role = ""

# ---------------- LOGIN FUNCTION ----------------

def login(username, password):

    if not os.path.exists(USERS):
        return None

    with open(USERS, "r") as file:

        for line in file:

            if line.strip() == "":
                continue

            role, user, pwd = line.strip().split(",")

            if user == username and pwd == password:
                return role

    return None


# ---------------- LOGIN PAGE ----------------

if st.session_state.user == "":

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    if st.button("Login"):

        role = login(username, password)

        if role:

            st.session_state.user = username
            st.session_state.role = role

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Username or Password")

# ---------------- AFTER LOGIN ----------------

else:

    st.sidebar.write("Logged in as")

    st.sidebar.success(st.session_state.user)

    if st.sidebar.button("Logout"):

        st.session_state.user = ""
        st.session_state.role = ""

        st.rerun()

    # ================= FACULTY =================

    if st.session_state.role == "faculty":

        menu = st.sidebar.radio(
            "Menu",
            [
                "Add Student",
                "View Students",
                "Mark Attendance",
                "View Attendance",
                "Search Student",
                "Filter By Date"
            ]
        )

        # ------------ ADD STUDENT ------------

        if menu == "Add Student":

            st.header("Add Student")

            name = st.text_input("Student Name")

            password = st.text_input("Password")

            if st.button("Add Student"):

                if name.strip() == "" or password.strip() == "":

                    st.warning("Fill all fields")

                else:

                    found = False

                    if os.path.exists(USERS):

                        with open(USERS, "r") as file:

                            for line in file:

                                if line.strip() == "":
                                    continue

                                role, user, pwd = line.strip().split(",")

                                if user.lower() == name.lower():

                                    found = True

                                    break

                    if found:

                        st.error("Student already exists")

                    else:

                        with open(USERS, "a") as file:

                            file.write(
                                f"student,{name},{password}\n"
                            )

                        st.success("Student Added Successfully")

        # ------------ VIEW STUDENTS ------------

        elif menu == "View Students":

            st.header("Student List")

            students = []

            if os.path.exists(USERS):

                with open(USERS, "r") as file:

                    for line in file:

                        if line.strip() == "":
                            continue

                        role, user, pwd = line.strip().split(",")

                        if role == "student":

                            students.append(user)

            if len(students) == 0:

                st.warning("No Students Found")

            else:

                for i, student in enumerate(students, start=1):

                    st.write(f"{i}. {student}")

        # ------------ MARK ATTENDANCE ------------

        elif menu == "Mark Attendance":

            st.header("Mark Attendance")

            students = []

            if os.path.exists(USERS):

                with open(USERS, "r") as file:

                    for line in file:

                        if line.strip() == "":
                            continue

                        role, user, pwd = line.strip().split(",")

                        if role == "student":
                            students.append(user)

            if len(students) == 0:

                st.warning("No Students Found")

            else:

                student = st.selectbox("Select Student", students)

                date = str(st.date_input("Date"))

                status = st.radio("Status", ["Present", "Absent"])

                if st.button("Submit"):

                    already_marked = False

                    if os.path.exists(ATTENDANCE):

                        with open(ATTENDANCE, "r") as file:

                            for line in file:

                                if line.strip() == "":
                                    continue

                                name, d, s = line.strip().split(",")

                                if name == student and d == date:
                                    already_marked = True
                                    break

                    if already_marked:

                        st.error("Attendance already marked for this date.")

                    else:

                        if status == "Present":
                            status = "P"
                        else:
                            status = "A"

                        with open(ATTENDANCE, "a") as file:

                            file.write(f"{student},{date},{status}\n")

                        st.success("Attendance Marked Successfully")

        # ------------ VIEW ATTENDANCE ------------

        elif menu == "View Attendance":

            st.header("Attendance Records")

            if os.path.exists(ATTENDANCE):

                with open(ATTENDANCE, "r") as file:

                    records = file.readlines()

                if len(records) == 0:

                    st.warning("No Attendance Records")

                else:

                    for line in records:

                        if line.strip() == "":
                            continue

                        parts = line.strip().split(",")

                        if len(parts) != 3:
                            continue

                        name, date, status = parts

                        if status == "P":
                            status = "Present"
                        else:
                            status = "Absent"

                        st.write(
                            f"Student: {name} | Date: {date} | Status: {status}"
                        )

            else:

                st.warning("Attendance File Not Found")

        # ------------ SEARCH STUDENT ------------

        elif menu == "Search Student":

            st.header("Search Student")

            search = st.text_input("Enter Student Name")

            if search:

                found = False

                if os.path.exists(ATTENDANCE):

                    with open(ATTENDANCE, "r") as file:

                        for line in file:

                            if line.strip() == "":
                                continue

                            parts = line.strip().split(",")

                            if len(parts) != 3:
                                continue

                            name, date, status = parts

                            if search.lower() in name.lower():

                                if status == "P":
                                    status = "Present"
                                else:
                                    status = "Absent"

                                st.write(
                                    f"Student: {name} | Date: {date} | Status: {status}"
                                )

                                found = True

                if not found:

                    st.warning("Student Not Found")

        # ------------ FILTER BY DATE ------------

        elif menu == "Filter By Date":

            st.header("Attendance By Date")

            selected_date = str(st.date_input("Select Date"))

            found = False

            if os.path.exists(ATTENDANCE):

                with open(ATTENDANCE, "r") as file:

                    for line in file:

                        if line.strip() == "":
                            continue

                        parts = line.strip().split(",")

                        if len(parts) != 3:
                            continue

                        name, date, status = parts

                        if date == selected_date:

                            if status == "P":
                                status = "Present"
                            else:
                                status = "Absent"

                            st.write(
                                f"Student: {name} | Status: {status}"
                            )

                            found = True

            if not found:

                st.warning("No Attendance Found")

    # ================= STUDENT =================

    else:

        st.header(f"Welcome, {st.session_state.user}")

        total = 0
        present = 0

        if os.path.exists(ATTENDANCE):

            with open(ATTENDANCE, "r") as file:

                for line in file:

                    if line.strip() == "":
                        continue

                    parts = line.strip().split(",")

                    if len(parts) != 3:
                        continue

                    name, date, status = parts

                    if name.lower() == st.session_state.user.lower():

                        total += 1

                        if status == "P":

                            display = "Present"
                            present += 1

                        else:

                            display = "Absent"

                        st.write(
                            f"Date: {date} | Status: {display}"
                        )

        if total > 0:

            percentage = (present / total) * 100

            st.success(
                f"Attendance Percentage: {percentage:.2f}%"
            )

            st.info(
                f"Present: {present}   |   Total Classes: {total}"
            )

        else:

            st.warning("No Attendance Records Found")
