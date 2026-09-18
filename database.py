import sqlite3
import streamlit as st


DB_FILE = "stressradar.db"


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

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

    cursor.execute("""
        INSERT INTO student_profile
        (name, country, state, college, department, year, semester)
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

    student_id = cursor.lastrowid

    for course in courses:

        # Handles dictionary format
        if isinstance(course, dict):
            course_name = course["course_name"]
            difficulty = course["difficulty"]
            confidence = course["confidence"]

        # Handles tuple/list format
        else:
            course_name = course[0]
            difficulty = course[1]
            confidence = course[2]

        cursor.execute("""
            INSERT INTO courses
            (student_id, course_name, difficulty, confidence)
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            course_name,
            difficulty,
            confidence
        ))

    connection.commit()
    connection.close()

    st.session_state["student_id"] = student_id


def get_latest_profile():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM student_profile
        ORDER BY id DESC
        LIMIT 1
    """)

    profile = cursor.fetchone()

    connection.close()

    if profile:
        return dict(profile)

    return None


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


create_tables()