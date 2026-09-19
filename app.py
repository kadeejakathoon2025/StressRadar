
import streamlit as st
from database import (
    get_profile,
    get_courses,
    get_checkins,
    get_all_profiles
)


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="StressRadar",
    page_icon="🌩️",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🌩️ StressRadar")

st.write(
    "Understand your academic stress. "
    "Plan smarter. Stay balanced."
)

st.divider()


# =========================================================
# CURRENT STUDENT
# =========================================================

student_id = st.session_state.get("student_id")


# =========================================================
# IF NO STUDENT IS SELECTED
# =========================================================

if not student_id:

    st.header("👋 Welcome to StressRadar")

    st.write(
        "Please select your profile or create a new student profile."
    )

    profiles = get_all_profiles()

    if profiles:

        st.subheader("👤 Existing Student")

        profile_options = {
            f"{p['name']} — {p['college']}": p["id"]
            for p in profiles
        }

        selected = st.selectbox(
            "Select your profile",
            list(profile_options.keys())
        )

        if st.button(
            "🚀 Continue",
            type="primary"
        ):

            st.session_state.student_id = profile_options[selected]

            profile = get_profile(
                st.session_state.student_id
            )

            st.session_state.profile = profile

            st.rerun()

        st.divider()

        st.info(
            "New student? Open 👤 My Profile from the sidebar "
            "and create your profile."
        )

    else:

        st.info(
            "No student profiles exist yet. "
            "Open 👤 My Profile and create your first profile."
        )

    st.stop()


# =========================================================
# LOAD CURRENT STUDENT
# =========================================================

profile = get_profile(student_id)

if not profile:

    st.error(
        "Student profile could not be found."
    )

    st.session_state.pop("student_id", None)

    st.stop()


# =========================================================
# PROFILE INFORMATION
# =========================================================

name = profile.get(
    "name",
    "Student"
)

college = profile.get(
    "college",
    "College"
)

department = profile.get(
    "department",
    "Department"
)

year = profile.get(
    "year",
    "Year"
)

semester = profile.get(
    "semester",
    "Semester"
)


# =========================================================
# LOAD STUDENT DATA
# =========================================================

courses = get_courses(student_id)

checkins = get_checkins(student_id)


# =========================================================
# WELCOME
# =========================================================

st.header(
    f"👋 Welcome back, {name}"
)

st.caption(
    f"{department} • {year} • {semester}"
)


# =========================================================
# CURRENT STRESS
# =========================================================

latest_stress = None
latest_weather = "No check-in yet"

if checkins:

    latest = checkins[-1]

    latest_stress = latest.get(
        "stress_score"
    )

    latest_weather = latest.get(
        "weather",
        "Unknown"
    )


if latest_stress is None:

    st.info(
        "Complete your first Daily Check-in "
        "to get your stress estimate."
    )

else:

    st.subheader("🌦️ Current Stress")

    st.metric(
        "Estimated Stress",
        f"{latest_stress}/100"
    )

    st.write(
        f"**Weather:** {latest_weather}"
    )

    if latest_stress <= 20:

        message = (
            "Your current estimate is in the Sunny range. "
            "Keep your routine steady."
        )

    elif latest_stress <= 40:

        message = (
            "Your current estimate is in the Clear range. "
            "Maintain a balanced routine."
        )

    elif latest_stress <= 60:

        message = (
            "Your current estimate is in the Cloudy range. "
            "A balanced study plan may help."
        )

    elif latest_stress <= 80:

        message = (
            "Your current estimate is in the Moody range. "
            "Consider lighter, manageable study blocks."
        )

    else:

        message = (
            "Your current estimate is in the Stormy range. "
            "Prioritize manageable tasks and recovery."
        )

    st.caption(message)


# =========================================================
# DASHBOARD
# =========================================================

st.divider()

st.subheader("📊 Your Dashboard")


if checkins:

    stress_values = [
        int(c["stress_score"])
        for c in checkins
        if c.get("stress_score") is not None
    ]

    if stress_values:

        average_stress = round(
            sum(stress_values) / len(stress_values),
            1
        )

    else:

        average_stress = "—"

else:

    average_stress = "—"


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📚 Courses",
        len(courses)
    )


with col2:

    st.metric(
        "📊 Check-ins",
        len(checkins)
    )


with col3:

    st.metric(
        "🌡️ Average Stress",
        average_stress
    )


with col4:

    st.metric(
        "🎓 Semester",
        semester
    )


# =========================================================
# COURSES
# =========================================================

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
                    f"**Difficulty:** {course['difficulty']}"
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


# =========================================================
# LOGOUT / SWITCH STUDENT
# =========================================================

st.divider()

if st.button("🔄 Switch Student"):

    st.session_state.pop(
        "student_id",
        None
    )

    st.session_state.pop(
        "profile",
        None
    )

    st.session_state.pop(
        "stress_score",
        None
    )

    st.session_state.pop(
        "stress_forecast",
        None
    )

    st.rerun()


# =========================================================
# ABOUT
# =========================================================

st.divider()

st.subheader("💡 About StressRadar")

st.write(
    "StressRadar combines student-reported factors "
    "such as workload, sleep, study hours, mood and "
    "upcoming exams to provide an explainable stress "
    "estimate and personalized study guidance."
)

st.divider()

st.caption(
    "🚀 StressRadar • Study smarter • "
    "Manage workload • Stay balanced"
)

st.caption(
    "Prototype only — stress estimates are rule-based "
    "and are not medically validated."
)
