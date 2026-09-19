import streamlit as st
import pandas as pd
from database import get_checkins

st.set_page_config(
    page_title="Stress Forecast",
    page_icon="🌦️",
    layout="wide"
)

if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "stress_score" not in st.session_state:
    st.session_state.stress_score = None

if "stress_forecast" not in st.session_state:
    st.session_state.stress_forecast = None

st.title("🌦️ Stress Forecast")

st.write(
    "Understand your current estimated stress level "
    "and how it changes over time."
)

st.divider()

student_id = st.session_state.get("student_id")

if student_id is None:

    st.warning(
        "Please create your student profile first."
    )

    st.stop()

try:

    checkins = get_checkins(student_id)

except Exception as e:

    st.error(
        f"Could not load your check-in history: {e}"
    )

    st.stop()

if not checkins:

    st.info(
        "📊 You haven't completed a Daily Check-in yet."
    )

    st.markdown(
        """
        ### What happens after your first check-in?

        StressRadar will show:

        - 🌩️ Your estimated stress score
        - 🌦️ Weather-style stress forecast
        - 📈 Stress history
        - 📊 Average, highest and lowest stress
        - 💡 Insights based on your check-in data
        """
    )

    st.stop()

df = pd.DataFrame(checkins)

df["checkin_date"] = pd.to_datetime(
    df["checkin_date"]
)

latest = df.iloc[-1]

latest_score = int(
    latest["stress_score"]
)

latest_weather = latest["weather"]

if latest_score <= 20:

    icon = "☀️"
    status = "Sunny"
    message = (
        "Your estimated stress level is low. "
        "This may be a good time for focused study."
    )

elif latest_score <= 40:

    icon = "🌤️"
    status = "Clear"
    message = (
        "Your estimated stress level is relatively low. "
        "You can maintain your regular study routine."
    )

elif latest_score <= 60:

    icon = "☁️"
    status = "Cloudy"
    message = (
        "Your estimated stress level is moderate. "
        "Balance study sessions with regular breaks."
    )

elif latest_score <= 80:

    icon = "🌧️"
    status = "Moody"
    message = (
        "Your estimated stress level is elevated. "
        "Consider shorter study sessions and manageable tasks."
    )

else:

    icon = "⛈️"
    status = "Stormy"
    message = (
        "Your estimated stress level is high. "
        "Prioritize manageable tasks, breaks and basic self-care."
    )

st.subheader("🌩️ Current Stress")

col1, col2 = st.columns([1, 2])

with col1:

    st.metric(
        "Estimated Stress",
        f"{latest_score}/100"
    )

with col2:

    st.markdown(
        f"""
        ## {icon} {status}

        {message}
        """
    )

st.divider()

st.subheader("📊 Your Stress Summary")

average_score = round(
    df["stress_score"].mean()
)

highest_score = int(
    df["stress_score"].max()
)

lowest_score = int(
    df["stress_score"].min()
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📈 Average",
        f"{average_score}/100"
    )

with col2:

    st.metric(
        "🔴 Highest",
        f"{highest_score}/100"
    )

with col3:

    st.metric(
        "🟢 Lowest",
        f"{lowest_score}/100"
    )

st.divider()

st.subheader("📈 Stress History")

chart_data = df[
    ["checkin_date", "stress_score"]
].copy()

chart_data = chart_data.set_index(
    "checkin_date"
)

st.line_chart(
    chart_data,
    y="stress_score"
)

st.caption(
    "Stress scores shown here are rule-based estimates "
    "calculated from your Daily Check-in responses."
)

st.divider()

st.subheader("🔍 Latest Check-in")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "😴 Sleep",
        f"{latest['sleep_hours']} hrs"
    )

    st.metric(
        "📚 Study",
        f"{latest['study_hours']} hrs"
    )

with col2:

    st.metric(
        "📋 Workload",
        f"{latest['workload']}/10"
    )

    st.metric(
        "🧠 Mental Tiredness",
        f"{latest['mental_tiredness']}/10"
    )

with col3:

    st.metric(
        "📝 Pending Tasks",
        latest["pending_tasks"]
    )

    if str(latest["exam_soon"]).lower() == "yes":

        st.metric(
            "📝 Exam",
            f"{latest['exam_days']} days"
        )

    else:

        st.metric(
            "📝 Exam",
            "Not soon"
        )

st.divider()

st.subheader("🌈 Stress Scale")

scale_data = pd.DataFrame(
    {
        "Level": [
            "☀️ Sunny",
            "🌤️ Clear",
            "☁️ Cloudy",
            "🌧️ Moody",
            "⛈️ Stormy"
        ],
        "Score": [
            "0–20",
            "21–40",
            "41–60",
            "61–80",
            "81–100"
        ]
    }
)

st.table(scale_data)

st.divider()

st.info(
    """
    **Important:** StressRadar provides a rule-based estimate
    using self-reported student information. It is not a
    medical diagnosis or clinically validated stress measurement.
    """
)