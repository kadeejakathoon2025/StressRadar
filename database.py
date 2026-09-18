import sqlite3
import streamlit as st

DB_FILE = "stressradar.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Student Profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            state TEXT,
            college TEXT,
            department TEXT,
            year TEXT,
            semester TEXT
        )
    """)

    # Daily Check-ins
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            checkin_date TEXT,
            sleep_hours REAL,
            study_hours REAL,
            workload INTEGER,
            mood TEXT,
            mental_tiredness INTEGER,
            pending_tasks INTEGER,
            exam_soon TEXT,
            exam_days INTEGER,
            self_reported_stress INTEGER,
            stress_score INTEGER,
            weather TEXT
        )
    """)

    # Marks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course TEXT,
            assessment TEXT,
            marks_obtained REAL,
            total_marks REAL,
            percentage REAL
        )
    """)

    # Courses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_name TEXT,
            difficulty TEXT,
            confidence INTEGER
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# SAVE STUDENT PROFILE
# =========================================================

def save_profile(
    name,
    country,
    state,
    college,
    department,
    year,
    semester,
    courses
):

    connection = get_connection()
    cursor = connection.cursor()

    # Save student profile
    cursor.execute("""
        INSERT INTO student_profile
        (
            name,
            country,
            state,
            college,
            department,
            year,
            semester
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        country,
        state,
        college,
        department,
        year,
        semester
    ))

    # Get the ID of the newly created student
    student_id = cursor.lastrowid

    # Save courses
    for course in courses:

        # Dictionary format
        if isinstance(course, dict):

            course_name = course["course_name"]
            difficulty = course["difficulty"]
            confidence = course["confidence"]

        # Tuple / list format
        else:

            course_name = course[0]
            difficulty = course[1]
            confidence = course[2]

        cursor.execute("""
            INSERT INTO courses
            (
                student_id,
                course_name,
                difficulty,
                confidence
            )
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            course_name,
            difficulty,
            confidence
        ))

    connection.commit()
    connection.close()

    # IMPORTANT:
    # Keep the student ID for the current user/session
    st.session_state["student_id"] = student_id

    # IMPORTANT:
    # Return the ID to My_Profile.py
    return student_id


# =========================================================
# GET CURRENT USER PROFILE
# =========================================================

def get_latest_profile():

    # Get the current user's student ID
    student_id = st.session_state.get("student_id")

    # No profile created in this session
    if not student_id:
        return None

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM student_profile
        WHERE id = ?
        LIMIT 1
    """, (student_id,))

    profile = cursor.fetchone()

    connection.close()

    if profile:
        return dict(profile)

    return None


# =========================================================
# GET COURSES
# =========================================================

def get_courses(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM courses
        WHERE student_id = ?
    """, (student_id,))

    courses = cursor.fetchall()

    connection.close()

    return [dict(course) for course in courses]


# =========================================================
# SAVE DAILY CHECK-IN
# =========================================================

def save_checkin(
    student_id,
    checkin_date,
    sleep_hours,
    study_hours,
    workload,
    mood,
    mental_tiredness,
    pending_tasks,
    exam_soon,
    exam_days,
    self_reported_stress,
    stress_score,
    weather
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO daily_checkins
        (
            student_id,
            checkin_date,
            sleep_hours,
            study_hours,
            workload,
            mood,
            mental_tiredness,
            pending_tasks,
            exam_soon,
            exam_days,
            self_reported_stress,
            stress_score,
            weather
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        str(checkin_date),
        sleep_hours,
        study_hours,
        workload,
        mood,
        mental_tiredness,
        pending_tasks,
        exam_soon,
        exam_days,
        self_reported_stress,
        stress_score,
        weather
    ))

    connection.commit()
    connection.close()


# =========================================================
# GET DAILY CHECK-INS
# =========================================================

def get_checkins(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM daily_checkins
        WHERE student_id = ?
        ORDER BY checkin_date
    """, (student_id,))

    checkins = cursor.fetchall()

    connection.close()

    return [dict(checkin) for checkin in checkins]


# =========================================================
# SAVE MARK
# =========================================================

def save_mark(
    student_id,
    course,
    assessment,
    marks_obtained,
    total_marks,
    percentage
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO marks
        (
            student_id,
            course,
            assessment,
            marks_obtained,
            total_marks,
            percentage
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        course,
        assessment,
        marks_obtained,
        total_marks,
        percentage
    ))

    connection.commit()
    connection.close()


# =========================================================
# GET MARKS
# =========================================================

def get_marks(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM marks
        WHERE student_id = ?
        ORDER BY id
    """, (student_id,))

    marks = cursor.fetchall()

    connection.close()

    return [dict(mark) for mark in marks]


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

create_tables()