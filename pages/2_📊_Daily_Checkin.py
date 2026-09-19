
import streamlit as st
from datetime import date
import pandas as pd
from database import get_connection, get_checkins

st.set_page_config(
    page_title="Daily Check-in",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Daily Check-in")

st.write(
    "Record your daily workload, sleep, study hours, "
    "mood and other factors to estimate your academic stress."
)

st.divider()

# =========================================================
# CHECK STUDENT PROFILE
# =========================================================

student_id = st.session_state.get("student_id")

if not student_id:
    st.warning("⚠️ Please create your student profile first.")
    st.stop()

# =========================================================
# CHECK-IN FORM
# =========================================================

st.subheader("📝 Today's Check-in")

checkin_date = st.date_input(
    "📅 Date",
    value=date.today()
)

col1, col2 = st.columns(2)

with col1:

    workload = st.slider(
        "📚 Workload",
        1,
        10,
        5
    )

    study_hours = st.number_input(
        "⏱️ Study Hours",
        0.0,
        24.0,
        4.0,
        0.5
    )

    sleep_hours = st.number_input(
        "😴 Sleep Hours",
        0.0,
        24.0,
        7.0,
        0.5
    )

    mood = st.slider(
        "😊 Mood",
        1,
        10,
        7
    )

with col2:

    mental_tiredness = st.slider(
        "🧠 Mental Tiredness",
        1,
        10,
        5
    )

    pending_tasks = st.number_input(
        "📋 Pending Tasks",
        0,
        50,
        2,
        1
    )

    exam_soon = st.selectbox(
        "📝 Upcoming Exam?",
        ["No", "Yes"]
    )

    exam_days = 0

    if exam_soon == "Yes":

        exam_days = st.number_input(
            "📅 Days Until Exam",
            0,
            365,
            7,
            1
        )

    self_reported_stress = st.slider(
        "🌡️ Self-Reported Stress",
        1,
        10,
        5
    )

# =========================================================
# CALCULATE STRESS
# =========================================================

def calculate_stress():

    score = 0

    score += workload * 4
    score += mental_tiredness * 4
    score += min(pending_tasks * 2, 20)
    score += self_reported_stress * 4

    if sleep_hours < 5:
        score += 15
    elif sleep_hours < 6:
        score += 10
    elif sleep_hours < 7:
        score += 5

    if study_hours > 10:
        score += 10
    elif study_hours > 8:
        score += 5

    if mood <= 3:
        score += 10
    elif mood <= 5:
        score += 5

    if exam_soon == "Yes":

        if exam_days <= 2:
            score += 15
        elif exam_days <= 7:
            score += 10
        elif exam_days <= 14:
            score += 5

    return max(0, min(score, 100))

# =========================================================
# WEATHER
# =========================================================

def get_weather(score):

    if score <= 20:
        return "☀️ Sunny"

    elif score <= 40:
        return "🌤️ Clear"

    elif score <= 60:
        return "⛅ Cloudy"

    elif score <= 80:
        return "🌥️ Moody"

    else:
        return "⛈️ Stormy"

# =========================================================
# SAVE CHECK-IN
# =========================================================

if st.button(
    "💾 Save Today's Check-in",
    type="primary",
    use_container_width=True
):

    stress_score = calculate_stress()
    weather = get_weather(stress_score)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
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
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        """,
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
    )

    connection.commit()

    cursor.close()
    connection.close()

    st.session_state.stress_score = stress_score
    st.session_state.stress_forecast = weather

    st.success("✅ Check-in saved successfully!")

# =========================================================
# CURRENT RESULT
# =========================================================

if "stress_score" in st.session_state:

    st.divider()

    st.subheader("🌦️ Today's Stress Result")

    score = st.session_state.stress_score

    weather = st.session_state.get(
        "stress_forecast",
        get_weather(score)
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Estimated Stress",
            f"{score}/100"
        )

    with col2:
        st.metric(
            "Stress Weather",
            weather
        )

# =========================================================
# ALL CHECK-IN HISTORY
# =========================================================

st.divider()

st.subheader("📋 Check-in History")

checkins = get_checkins(student_id)

if checkins:

    df = pd.DataFrame(checkins)

    display_df = df.rename(
        columns={
            "checkin_date": "Date",
            "sleep_hours": "Sleep (hrs)",
            "study_hours": "Study (hrs)",
            "workload": "Workload",
            "mood": "Mood",
            "mental_tiredness": "Mental Tiredness",
            "pending_tasks": "Pending Tasks",
            "exam_soon": "Exam Soon",
            "exam_days": "Exam Days",
            "self_reported_stress": "Self Stress",
            "stress_score": "Stress Score",
            "weather": "Weather"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # STRESS GRAPH
    # =====================================================

    st.subheader("📈 Stress History")

    chart_df = df.copy()

    chart_df["checkin_date"] = pd.to_datetime(
        chart_df["checkin_date"]
    )

    chart_df = chart_df.sort_values(
        "checkin_date"
    )

    chart_df = chart_df.set_index(
        "checkin_date"
    )

    st.line_chart(
        chart_df["stress_score"]
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    st.subheader("📊 Stress Summary")

    stress_values = [
        x for x in df["stress_score"]
        if x is not None
    ]

    if stress_values:

        average_stress = round(
            sum(stress_values) / len(stress_values),
            1
        )

        highest_stress = max(stress_values)
        lowest_stress = min(stress_values)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Stress",
                f"{average_stress}/100"
            )

        with col2:
            st.metric(
                "Highest Stress",
                f"{highest_stress}/100"
            )

        with col3:
            st.metric(
                "Lowest Stress",
                f"{lowest_stress}/100"
            )

else:

    st.info(
        "📭 No check-ins yet. Complete your first check-in above."
    )

# =========================================================
# STRESS SCALE
# =========================================================

st.divider()

st.subheader("🌦️ Stress Scale")

scale_data = pd.DataFrame(
    {
        "Stress Score": [
            "0–20",
            "21–40",
            "41–60",
            "61–80",
            "81–100"
        ],
        "Weather": [
            "☀️ Sunny",
            "🌤️ Clear",
            "⛅ Cloudy",
            "🌥️ Moody",
            "⛈️ Stormy"
        ],
        "Meaning": [
            "Low stress",
            "Relatively low stress",
            "Moderate stress",
            "Elevated stress",
            "High stress"
        ]
    }
)

st.dataframe(
    scale_data,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "⚠️ StressRadar provides a rule-based estimate using "
    "self-reported academic and lifestyle factors. "
    "It is a student-support prototype and is not medically "
    "validated."
)