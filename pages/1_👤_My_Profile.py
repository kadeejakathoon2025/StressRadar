
import streamlit as st
from database import (
    get_profile,
    get_courses,
    save_profile
)


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)


st.title("👤 My Student Profile")


# =========================================================
# IF STUDENT ALREADY EXISTS
# =========================================================

student_id = st.session_state.get("student_id")


if student_id:

    profile = get_profile(student_id)
    courses = get_courses(student_id)

    if profile:

        st.success(
            f"👋 This is the profile of {profile['name']}"
        )

        st.divider()

        st.subheader("🎓 Student Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Name:** {profile['name']}"
            )

            st.write(
                f"**Country:** {profile['country']}"
            )

            st.write(
                f"**State:** {profile['state']}"
            )

            st.write(
                f"**College:** {profile['college']}"
            )

        with col2:

            st.write(
                f"**Department:** {profile['department']}"
            )

            st.write(
                f"**Year:** {profile['year']}"
            )

            st.write(
                f"**Semester:** {profile['semester']}"
            )

        st.divider()

        st.subheader("📚 Your Courses")

        if courses:

            for course in courses:

                with st.container(border=True):

                    st.markdown(
                        f"### 📖 {course['course_name']}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Difficulty:** "
                            f"{course['difficulty']}"
                        )

                    with col2:

                        st.write(
                            f"**Confidence:** "
                            f"{course['confidence']}/10"
                        )

        else:

            st.info(
                "No courses found."
            )

        st.divider()

        st.info(
            "✅ Your saved profile is being used by "
            "Daily Check-in, Stress Forecast, Study Planner "
            "and Exams & Marks."
        )

        st.stop()


# =========================================================
# NEW STUDENT PROFILE
# =========================================================

st.write(
    "Create your profile to start using StressRadar."
)

st.divider()

st.subheader("🎓 Student Information")

name = st.text_input(
    "Your Name"
)

country = st.selectbox(
    "🌍 Country",
    [
        "Select Country",
        "India",
        "Other"
    ]
)

states = [
    "Select State / Union Territory",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Chandigarh",
    "Puducherry",
    "Lakshadweep",
    "Other"
]

if country == "India":

    state = st.selectbox(
        "📍 State / Union Territory",
        states
    )

else:

    state = "Other"


college = st.text_input(
    "🏫 College / University"
)


departments = [
    "Select Department",
    "Computer Science and Engineering",
    "CSE - Data Science",
    "CSE - Artificial Intelligence",
    "Information Technology",
    "Electronics and Communication Engineering",
    "Electrical and Electronics Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Biotechnology",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Commerce",
    "Management",
    "Other"
]

department = st.selectbox(
    "💻 Department",
    departments
)


year = st.selectbox(
    "📅 Year",
    [
        "Select Year",
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year",
        "5th Year"
    ]
)


if year == "1st Year":

    semesters = [
        "Select Semester",
        "Semester 1",
        "Semester 2"
    ]

elif year == "2nd Year":

    semesters = [
        "Select Semester",
        "Semester 3",
        "Semester 4"
    ]

elif year == "3rd Year":

    semesters = [
        "Select Semester",
        "Semester 5",
        "Semester 6"
    ]

elif year == "4th Year":

    semesters = [
        "Select Semester",
        "Semester 7",
        "Semester 8"
    ]

elif year == "5th Year":

    semesters = [
        "Select Semester",
        "Semester 9",
        "Semester 10"
    ]

else:

    semesters = [
        "Select Semester"
    ]


semester = st.selectbox(
    "📖 Semester",
    semesters
)


# =========================================================
# COURSES
# =========================================================

st.divider()

st.subheader("📚 Your Courses")

course_details = []

for i in range(1, 7):

    course = st.text_input(
        f"Course {i}",
        key=f"new_course_{i}"
    )

    if course.strip():

        difficulty = st.selectbox(
            f"Difficulty — {course}",
            [
                "Easy",
                "Medium",
                "Difficult"
            ],
            key=f"new_difficulty_{i}"
        )

        confidence = st.slider(
            f"Confidence — {course}",
            1,
            10,
            5,
            key=f"new_confidence_{i}"
        )

        course_details.append(
            (
                course.strip(),
                difficulty,
                confidence
            )
        )


# =========================================================
# CREATE PROFILE
# =========================================================

st.divider()

if st.button(
    "🚀 Create My Profile",
    type="primary",
    use_container_width=True
):

    if not name.strip():

        st.error("Please enter your name.")

    elif country == "Select Country":

        st.error("Please select your country.")

    elif country == "India" and state == "Select State / Union Territory":

        st.error("Please select your state.")

    elif not college.strip():

        st.error("Please enter your college.")

    elif department == "Select Department":

        st.error("Please select your department.")

    elif year == "Select Year":

        st.error("Please select your year.")

    elif semester == "Select Semester":

        st.error("Please select your semester.")

    elif not course_details:

        st.error("Please enter at least one course.")

    else:

        try:

            student_id = save_profile(
                name.strip(),
                country,
                state,
                college.strip(),
                department,
                year,
                semester,
                course_details
            )

            st.session_state.student_id = student_id

            st.success(
                "🎉 Profile created successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"❌ Could not save profile: {e}"
            )
