import streamlit as st
from database import get_latest_profile, get_courses, get_checkins


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
# LOAD PROFILE
# =========================================================

profile = get_latest_profile()


# =========================================================
# IF NO PROFILE
# =========================================================

if not profile:

    st.info(
        "👋 Welcome to StressRadar! "
        "Please create your student profile first."
    )

    st.stop()


# =========================================================
# PROFILE DETAILS
# =========================================================

student_id = profile["id"]

name = profile.get("name", "Student")
college = profile.get("college", "College")
department = profile.get("department", "Department")
year = profile.get("year", "Year")
semester = profile.get("semester", "Semester")


# =========================================================
# LOAD DATA
# =========================================================

courses = get_courses(student_id)
checkins = get_checkins(student_id)


# =========================================================
# WELCOME
# =========================================================

st.header(f"👋 Welcome back, {name}")

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

    latest_stress = latest.get("stress_score")

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


    st.subheader("🌦️ Current Stress")

    st.metric(
        "Estimated Stress",
        f"{latest_stress}/100"
    )

    st.write(f"**Weather:** {latest_weather}")

    st.caption(message)


# =========================================================
# DASHBOARD METRICS
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
# QUICK ACTIONS
# =========================================================

st.divider()

st.subheader("⚡ Quick Actions")


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("### 📊 Daily Check-in")

    st.write(
        "Record today's workload, sleep, "
        "mood and stress."
    )


with col2:

    st.markdown("### 🌦️ Stress Forecast")

    st.write(
        "View your stress history and "
        "current status."
    )


with col3:

    st.markdown("### 📚 Study Planner")

    st.write(
        "Get a personalized study order "
        "based on your current stress."
    )


# =========================================================
# COURSES
# =========================================================

st.divider()

st.subheader("📚 Your Courses")


if courses:

    for course in courses:

        course_name = course.get(
            "course_name",
            "Course"
        )

        difficulty = course.get(
            "difficulty",
            "Not specified"
        )

        confidence = course.get(
            "confidence",
            "—"
        )

        with st.container(border=True):

            st.markdown(
                f"### 📖 {course_name}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Difficulty:** {difficulty}"
                )

            with col2:

                st.write(
                    f"**Confidence:** {confidence}/10"
                )


else:

    st.info(
        "No courses found. "
        "Create your profile to add courses."
    )


# =========================================================
# ABOUT STRESSRADAR
# =========================================================

st.divider()

st.subheader("💡 About StressRadar")

st.write(
    "StressRadar combines student-reported factors "
    "such as workload, sleep, study hours, mood and "
    "upcoming exams to provide an explainable stress "
    "estimate and personalized study guidance."
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🚀 StressRadar • Study smarter • "
    "Manage workload • Stay balanced"
)

st.caption(
    "Prototype only — stress estimates are rule-based "
    "and are not medically validated."
)