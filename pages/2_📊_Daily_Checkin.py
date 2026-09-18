import streamlit as st
from datetime import date
from database import get_connection

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Daily Check-in",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "stress_score" not in st.session_state:
    st.session_state.stress_score = None

if "stress_forecast" not in st.session_state:
    st.session_state.stress_forecast = None


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 Daily Check-in")

st.write(
    "Tell StressRadar how your day is going. "
    "Your responses are used to generate an explainable stress estimate."
)

st.divider()


# --------------------------------------------------
# STUDENT CHECK
# --------------------------------------------------

student_id = st.session_state.get("student_id")

if student_id is None:

    st.warning(
        "⚠️ Please create your student profile first."
    )

    st.stop()


# --------------------------------------------------
# INTRO CARD
# --------------------------------------------------

st.info(
    "💡 Be honest with your answers. There are no right or wrong answers."
)


# ==================================================
# TODAY
# ==================================================

st.subheader("📅 Today's Check-in")

checkin_date = st.date_input(
    "Check-in date",
    value=date.today()
)


# ==================================================
# DAILY HABITS
# ==================================================

st.subheader("😴 Daily Habits")

col1, col2 = st.columns(2)

with col1:

    sleep_hours = st.slider(
        "😴 How many hours did you sleep?",
        min_value=0.0,
        max_value=12.0,
        value=7.0,
        step=0.5
    )

with col2:

    study_hours = st.slider(
        "📚 How many hours did you study?",
        min_value=0.0,
        max_value=16.0,
        value=4.0,
        step=0.5
    )


# ==================================================
# WORKLOAD & MENTAL STATE
# ==================================================

st.subheader("🧠 Current State")

col1, col2 = st.columns(2)

with col1:

    workload = st.slider(
        "📋 How heavy is your current workload?",
        min_value=1,
        max_value=10,
        value=5
    )

    mental_tiredness = st.slider(
        "🧠 How mentally tired are you?",
        min_value=1,
        max_value=10,
        value=5
    )

with col2:

    mood = st.select_slider(
        "😊 How is your mood today?",
        options=[
            "Very Bad",
            "Bad",
            "Okay",
            "Good",
            "Very Good"
        ],
        value="Okay"
    )

    pending_tasks = st.number_input(
        "📝 How many tasks are pending?",
        min_value=0,
        max_value=50,
        value=3,
        step=1
    )


# ==================================================
# EXAM PRESSURE
# ==================================================

st.subheader("📝 Academic Pressure")

exam_soon = st.radio(
    "Do you have an exam approaching?",
    ["No", "Yes"],
    horizontal=True
)

exam_days = 0

if exam_soon == "Yes":

    exam_days = st.number_input(
        "📅 How many days until the exam?",
        min_value=1,
        max_value=365,
        value=7,
        step=1
    )


# ==================================================
# SELF REPORTED STRESS
# ==================================================

st.subheader("🌩️ Your Own Stress Rating")

self_reported_stress = st.slider(
    "How stressed do you personally feel right now?",
    min_value=1,
    max_value=10,
    value=5
)

st.caption(
    "1 = Not stressed at all   •   10 = Extremely stressed"
)


st.divider()


# ==================================================
# CALCULATE BUTTON
# ==================================================

if st.button(
    "🌩️ Calculate My Stress",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------
    # STRESS CALCULATION
    # --------------------------------------------------

    score = 0

    # Workload
    score += workload * 3

    # Mental tiredness
    score += mental_tiredness * 3

    # Pending tasks
    score += min(pending_tasks * 2, 20)

    # Self-reported stress
    score += self_reported_stress * 3

    # Sleep
    if sleep_hours < 5:
        score += 15
    elif sleep_hours < 6:
        score += 10
    elif sleep_hours < 7:
        score += 5

    # Study hours
    if study_hours > 10:
        score += 8
    elif study_hours > 8:
        score += 5

    # Mood
    mood_scores = {
        "Very Bad": 10,
        "Bad": 7,
        "Okay": 4,
        "Good": 1,
        "Very Good": 0
    }

    score += mood_scores[mood]

    # Exam pressure
    if exam_soon == "Yes":

        if exam_days <= 2:
            score += 15
        elif exam_days <= 7:
            score += 10
        elif exam_days <= 14:
            score += 5

    # Keep score between 0 and 100
    score = max(0, min(100, score))


    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    if score <= 20:

        weather = "Sunny"
        icon = "☀️"

    elif score <= 40:

        weather = "Clear"
        icon = "🌤️"

    elif score <= 60:

        weather = "Cloudy"
        icon = "☁️"

    elif score <= 80:

        weather = "Moody"
        icon = "🌧️"

    else:

        weather = "Stormy"
        icon = "⛈️"


    # --------------------------------------------------
    # SAVE SESSION
    # --------------------------------------------------

    st.session_state.stress_score = score
    st.session_state.stress_forecast = weather


    # --------------------------------------------------
    # SAVE TO MYSQL
    # --------------------------------------------------

    try:

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
                score,
                weather
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        database_saved = True

    except Exception as e:

        database_saved = False

        st.error(
            f"Could not save your check-in: {e}"
        )


    # ==================================================
    # RESULT
    # ==================================================

    st.divider()

    st.subheader("🌩️ Your StressRadar Result")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Estimated Stress",
            f"{score}/100"
        )

    with col2:

        st.metric(
            "Weather",
            f"{icon} {weather}"
        )


    # --------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------

    if score <= 20:

        st.success(
            "☀️ Your estimated stress is low. "
            "This may be a good time for focused study."
        )

    elif score <= 40:

        st.success(
            "🌤️ Your estimated stress is relatively low. "
            "You can continue with your regular study routine."
        )

    elif score <= 60:

        st.warning(
            "☁️ Your estimated stress is moderate. "
            "Try balancing study sessions with regular breaks."
        )

    elif score <= 80:

        st.warning(
            "🌧️ Your estimated stress is elevated. "
            "Consider manageable tasks and shorter study sessions."
        )

    else:

        st.error(
            "⛈️ Your estimated stress is high. "
            "Prioritize manageable tasks, breaks and basic self-care."
        )


    # --------------------------------------------------
    # DATABASE STATUS
    # --------------------------------------------------

    if database_saved:

        st.success(
            "✅ Today's check-in has been saved successfully."
        )


    # --------------------------------------------------
    # WHAT TO DO NEXT
    # --------------------------------------------------

    st.divider()

    st.subheader("🚀 What should you do next?")

    if score >= 61:

        st.info(
            "📚 Your study planner will prioritize manageable "
            "subjects and shorter sessions."
        )

    elif score >= 41:

        st.info(
            "📚 Your study planner will create a balanced "
            "study schedule."
        )

    else:

        st.info(
            "📚 Your study planner can prioritize difficult "
            "subjects while your estimated stress is lower."
        )


# ==================================================
# DISCLAIMER
# ==================================================

st.divider()

st.caption(
    "StressRadar provides a rule-based estimate based on "
    "self-reported information. It is not a medical diagnosis "
    "or clinically validated stress measurement."
)