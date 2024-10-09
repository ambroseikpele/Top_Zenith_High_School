import streamlit as st
import pandas as pd
import sqlite3

# Establish a database connection
conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

# Create the tables in the database if they don't already exist
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Parents (
                        ParentID TEXT PRIMARY KEY,
                        ParentName TEXT,
                        Gender TEXT,
                        EducationLevel TEXT,
                        StateOfOrigin TEXT,
                        NumberOfWards INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Staff (
                        StaffID TEXT PRIMARY KEY,
                        StaffName TEXT,
                        Position TEXT,
                        SubjectID TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Subjects (
                        SubjectID TEXT PRIMARY KEY,
                        SubjectName TEXT,
                        Level TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Class (
                        ClassID TEXT PRIMARY KEY,
                        ClassName TEXT,
                        StaffID TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                        StudentID TEXT PRIMARY KEY,
                        StudentName TEXT,
                        Age INTEGER,
                        Gender TEXT,
                        ParentID TEXT,
                        ClassID TEXT,
                        FOREIGN KEY (ParentID) REFERENCES Parents(ParentID),
                        FOREIGN KEY (ClassID) REFERENCES Class(ClassID))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Results (
                        StudentID TEXT,
                        ClassID TEXT,
                        SubjectID TEXT,
                        Session TEXT,
                        Term TEXT,
                        Score REAL,
                        PRIMARY KEY (StudentID, SubjectID, Session, Term),
                        FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
                        FOREIGN KEY (ClassID) REFERENCES Class(ClassID),
                        FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID))''')

    conn.commit()

# Call the create_tables function to ensure all tables are created
create_tables()

# Define sidebar for navigation
menu = ["Home", "Add Parent", "Add Staff", "Add Subject", "Add Class", "Add Student", "Add Results", "View Data"]
choice = st.sidebar.radio("Menu", menu)

# Define form for adding Parents
if choice == "Add Parent":
    st.subheader("Add Parent Information")
    with st.form(key='parent_form'):
        parent_id = st.text_input("Parent ID")
        parent_name = st.text_input("Parent Name")
        gender = st.selectbox("Gender", ["Male", "Female"])
        education_level = st.selectbox("Education Level", ["SSCE", "OND", "HND", "BSc", "MSc", "PhD"])
        state_of_origin = st.text_input("State of Origin")
        number_of_wards = st.selectbox("Number of Wards", [1, 2, 3])

        submit_button = st.form_submit_button(label='Add Parent')
        
        if submit_button:
            cursor.execute("INSERT INTO Parents (ParentID, ParentName, Gender, EducationLevel, StateOfOrigin, NumberOfWards) VALUES (?,?,?,?,?,?)",
                           (parent_id, parent_name, gender, education_level, state_of_origin, number_of_wards))
            conn.commit()
            st.success(f"Parent {parent_name} added successfully!")

# Define form for adding Staff
elif choice == "Add Staff":
    st.subheader("Add Staff Information")
    with st.form(key='staff_form'):
        staff_id = st.text_input("Staff ID")
        staff_name = st.text_input("Staff Name")
        position = st.text_input("Position")
        subject_id = st.text_input("Subject ID (if applicable)")

        submit_button = st.form_submit_button(label='Add Staff')
        
        if submit_button:
            cursor.execute("INSERT INTO Staff (StaffID, StaffName, Position, SubjectID) VALUES (?,?,?,?)",
                           (staff_id, staff_name, position, subject_id))
            conn.commit()
            st.success(f"Staff {staff_name} added successfully!")

# Define form for adding Subjects
elif choice == "Add Subject":
    st.subheader("Add Subject Information")
    with st.form(key='subject_form'):
        subject_id = st.text_input("Subject ID")
        subject_name = st.text_input("Subject Name")
        level = st.selectbox("Level", ["JSS", "SSS"])

        submit_button = st.form_submit_button(label='Add Subject')
        
        if submit_button:
            cursor.execute("INSERT INTO Subjects (SubjectID, SubjectName, Level) VALUES (?,?,?)",
                           (subject_id, subject_name, level))
            conn.commit()
            st.success(f"Subject {subject_name} added successfully!")

# Define form for adding Class
elif choice == "Add Class":
    st.subheader("Add Class Information")
    with st.form(key='class_form'):
        class_id = st.text_input("Class ID")
        class_name = st.text_input("Class Name (e.g., JSS1, JSS2, ... SS3)")
        staff_id = st.text_input("Staff ID (Class Teacher)")

        submit_button = st.form_submit_button(label='Add Class')
        
        if submit_button:
            cursor.execute("INSERT INTO Class (ClassID, ClassName, StaffID) VALUES (?,?,?)",
                           (class_id, class_name, staff_id))
            conn.commit()
            st.success(f"Class {class_name} added successfully!")

# Define form for adding Students
elif choice == "Add Student":
    st.subheader("Add Student Information")
    with st.form(key='student_form'):
        student_id = st.text_input("Student ID")
        student_name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=5, max_value=25, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        parent_id = st.text_input("Parent ID")
        class_id = st.text_input("Class ID")

        submit_button = st.form_submit_button(label='Add Student')
        
        if submit_button:
            cursor.execute("INSERT INTO Students (StudentID, StudentName, Age, Gender, ParentID, ClassID) VALUES (?,?,?,?,?,?)",
                           (student_id, student_name, age, gender, parent_id, class_id))
            conn.commit()
            st.success(f"Student {student_name} added successfully!")

# Define form for adding Results
elif choice == "Add Results":
    st.subheader("Add Results Information")
    with st.form(key='results_form'):
        student_id = st.text_input("Student ID")
        class_id = st.text_input("Class ID")
        subject_id = st.text_input("Subject ID")
        session = st.text_input("Session (e.g., 2023/2024)")
        term = st.selectbox("Term", ["1st Term", "2nd Term", "3rd Term"])
        score = st.number_input("Score", min_value=0.0, max_value=100.0, step=0.1)

        submit_button = st.form_submit_button(label='Add Result')
        
        if submit_button:
            cursor.execute("INSERT INTO Results (StudentID, ClassID, SubjectID, Session, Term, Score) VALUES (?,?,?,?,?,?)",
                           (student_id, class_id, subject_id, session, term, score))
            conn.commit()
            st.success(f"Result for Student {student_id} added successfully!")

# View Data Section
elif choice == "View Data":
    st.subheader("View Database Tables")
    view_choice = st.selectbox("Choose a Table to View", ["Parents", "Staff", "Subjects", "Class", "Students", "Results"])
    if view_choice:
        table = pd.read_sql_query(f"SELECT * FROM {view_choice}", conn)
        st.dataframe(table)

# Home section
else:
    st.title("Top Zenith High School")
    st.write("This is a Streamlit-based web application for collecting school data, including parents, staff, students, classes, and results.")

# Close the database connection when done
conn.close()
