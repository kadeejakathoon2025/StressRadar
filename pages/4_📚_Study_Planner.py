import streamlit as st

st.set_page_config(
    page_title="Study Planner",
    page_icon="📚",
    layout="wide"
)

if "profile" not in st.session_state:
    st.session_state.profile = None

if "stress_score" not in st.session_state:
    st.session_state.stress_score = None

st.title("📚 Smart Study Planner")

st.write(
    "StressRadar adapts your study plan according to "
    "your current estimated stress level."
)

st.divider()

profile = st.session_state.get("profile")

if profile is None:
    st.warning(
        "⚠️ Please create your student profile first."
    )
    st.stop()

stress_score = st.session_state.get("stress_score")

if stress_score is None:
    st.info(
        "🌩️ Complete your Daily Check-in first so "
        "StressRadar can personalize your study plan."
    )
    st.stop()

if stress_score >= 61:

    mode = "🌧️ Recovery Study Mode"

    description = (
        "Your estimated stress is elevated. "
        "StressRadar prioritizes manageable subjects "
        "and shorter study sessions."
    )

    session_time = 25
    break_time = 5

    difficulty_order = {
        "Easy": 1,
        "Medium": 2,
        "Difficult": 3
    }

elif stress_score >= 41:

    mode = "☁️ Balanced Study Mode"

    description = (
        "Your estimated stress is moderate. "
        "StressRadar creates a balanced study schedule."
    )

    session_time = 40
    break_time = 10

    difficulty_order = {
        "Medium": 1,
        "Easy": 2,
        "Difficult": 3
    }

else:

    mode = "☀️ Deep Focus Mode"

    description = (
        "Your estimated stress is relatively low. "
        "StressRadar prioritizes more challenging subjects."
    )

    session_time = 50
    break_time = 10

    difficulty_order = {
        "Difficult": 1,
        "Medium": 2,
        "Easy": 3
    }

st.subheader("🌩️ Your Current Study Mode")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Estimated Stress",
        f"{stress_score}/100"
    )

with col2:

    st.markdown(f"### {mode}")

    st.caption(description)

st.divider()

course_details = profile.get(
    "course_details",
    {}
)

course_list = []

for course_name in profile.get("courses", []):

    details = course_details.get(
        course_name,
        {}
    )

    difficulty = details.get(
        "difficulty",
        "Medium"
    )

    confidence = details.get(
        "confidence",
        5
    )

    course_list.append(
        {
            "name": course_name,
            "difficulty": difficulty,
            "confidence": confidence
        }
    )

course_list.sort(
    key=lambda x: (
        difficulty_order.get(
            x["difficulty"],
            2
        ),
        x["confidence"]
    )
)

st.subheader("🗓️ Your Personalized Study Plan")

if not course_list:

    st.info(
        "No courses are available. Add courses from My Profile."
    )

else:

    for index, course in enumerate(course_list):

        st.markdown(
            f"### {index + 1}. 📖 {course['name']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                f"**Difficulty:** {course['difficulty']}"
            )

        with col2:

            st.write(
                f"**Confidence:** {course['confidence']}/10"
            )

        with col3:

            st.write(
                f"⏱️ **Study:** {session_time} min"
            )

        if index < len(course_list) - 1:

            st.info(
                f"☕ Take a {break_time}-minute break before "
                f"starting the next subject."
            )

        st.divider()

st.subheader("💡 StressRadar Tip")

if stress_score >= 61:

    st.warning(
        "Don't try to finish everything at once. "
        "Start with one manageable subject, study for "
        f"{session_time} minutes, then take a break."
    )

elif stress_score >= 41:

    st.info(
        "Keep a balanced pace. Study for "
        f"{session_time} minutes and take a "
        f"{break_time}-minute break between sessions."
    )

else:

    st.success(
        "Your current estimated stress is relatively low. "
        "Use this period for focused work on your more "
        "challenging subjects."
    )

st.divider()

st.caption(
    "StressRadar creates a rule-based study recommendation "
    "using your estimated stress and course difficulty."
)