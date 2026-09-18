import streamlit as st
import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"])
    )
    return connection


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

    cursor.execute(
        """
        INSERT INTO student_profile
        (name, country, state, college, department, year, semester)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (name, country, state, college, department, year, semester)
    )

    student_id = cursor.lastrowid

    for course_name, difficulty, confidence in courses:
        cursor.execute(
            """
            INSERT INTO courses
            (student_id, course_name, difficulty, confidence)
            VALUES (%s, %s, %s, %s)
            """,
            (student_id, course_name, difficulty, confidence)
        )

    connection.commit()
    cursor.close()
    connection.close()

    return student_id


def get_latest_profile():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM student_profile
        ORDER BY id DESC
        LIMIT 1
        """
    )

    profile = cursor.fetchone()

    cursor.close()
    connection.close()

    return profile


def get_courses(student_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT course_name, difficulty, confidence
        FROM courses
        WHERE student_id = %s
        """,
        (student_id,)
    )

    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return courses


def get_checkins(student_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
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
        FROM daily_checkins
        WHERE student_id = %s
        ORDER BY checkin_date
        """,
        (student_id,)
    )

    checkins = cursor.fetchall()

    cursor.close()
    connection.close()

    return checkins


def get_marks(student_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            course,
            assessment,
            marks_obtained,
            total_marks,
            percentage
        FROM marks
        WHERE student_id = %s
        ORDER BY id
        """,
        (student_id,)
    )

    marks = cursor.fetchall()

    cursor.close()
    connection.close()

    return marks