import streamlit as st

st.set_page_config(
    page_title="Wellness",
    page_icon="🌿",
    layout="wide"
)

if "stress_score" not in st.session_state:
    st.session_state.stress_score = None

st.title("🌿 Wellness")

st.write(
    "Small habits can help you manage academic pressure "
    "and maintain a healthier study routine."
)

st.divider()

stress_score = st.session_state.get(
    "stress_score"
)

st.subheader("🌩️ Your Current Status")

if stress_score is None:

    st.info(
        "Complete a Daily Check-in to see "
        "wellness suggestions based on your current estimate."
    )

else:

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Estimated Stress",
            f"{stress_score}/100"
        )

    with col2:

        if stress_score >= 81:

            st.write("### ⛈️ Take a step back")

            st.caption(
                "Your estimated stress is high. "
                "Focus on manageable tasks and recovery."
            )

        elif stress_score >= 61:

            st.write("### 🌧️ Slow down")

            st.caption(
                "Your estimated stress is elevated. "
                "Consider shorter study sessions and breaks."
            )

        elif stress_score >= 41:

            st.write("### ☁️ Maintain balance")

            st.caption(
                "Your estimated stress is moderate. "
                "Balance focused study with regular breaks."
            )

        else:

            st.write("### ☀️ Keep going")

            st.caption(
                "Your estimated stress is relatively low. "
                "Maintain healthy study habits."
            )

st.divider()

st.subheader("🌱 Simple Wellness Habits")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 😴 Sleep")

    st.write(
        "Try to maintain a consistent sleep schedule "
        "and give your body enough time to recover."
    )

with col2:

    st.markdown("### 🚶 Movement")

    st.write(
        "Take short walks or stretch between long "
        "study sessions."
    )

with col3:

    st.markdown("### 💧 Hydration")

    st.write(
        "Keep water nearby during study sessions "
        "and remember to take regular breaks."
    )

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 🧘 Breaks")

    st.write(
        "Short breaks can help you reset before "
        "starting the next study session."
    )

with col2:

    st.markdown("### 📱 Reduce Distractions")

    st.write(
        "Keep unnecessary notifications and "
        "distractions away during focused study."
    )

with col3:

    st.markdown("### 👥 Connect")

    st.write(
        "Talk to a trusted friend, family member, "
        "teacher or counselor when you need support."
    )

st.divider()

st.subheader("🌿 5-Minute Reset")

st.info(
    """
    **Try this simple reset:**

    1. Put your study material aside.
    2. Take a few slow breaths.
    3. Drink some water.
    4. Stretch or walk for a few minutes.
    5. Return to one small, manageable task.
    """
)

st.divider()

st.warning(
    """
    **Important:** StressRadar is a student wellness and
    study-support tool. Its stress score is a rule-based
    estimate from self-reported information. It is not a
    medical diagnosis or a replacement for professional help.
    """
)

st.caption(
    "🌿 StressRadar • Take care of yourself while you work toward your goals."
)