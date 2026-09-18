import streamlit as st
import pandas as pd
from database import get_connection, get_marks

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Exams & Marks",
    page_icon="📝",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "marks" not in st.session_state:
    st.session_state.marks = []


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📝 Exams & Marks")

st.write(
    "Track your assessment performance and understand "
    "your academic progress."
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
# LOAD MARKS
# --------------------------------------------------

try:

    saved_marks = get_marks(student_id)

    st.session_state.marks = saved_marks

except Exception as e:

    st.error(
        f"Could not load your marks: {e}"
    )


# ==================================================
# ADD MARKS
# ==================================================

st.subheader("➕ Add Assessment")

col1, col2 = st.columns(2)

with col1:

    course = st.text_input(
        "📚 Course",
        placeholder="Example: Mathematics"
    )

    assessment = st.selectbox(
        "📝 Assessment",
        [
            "Quiz",
            "CAT 1",
            "CAT 2",
            "FAT",
            "Assignment",
            "Lab",
            "Other"
        ]
    )

with col2:

    marks_obtained = st.number_input(
        "Marks obtained",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    total_marks = st.number_input(
        "Total marks",
        min_value=1.0,
        value=100.0,
        step=1.0
    )


if st.button(
    "💾 Save Assessment",
    type="primary",
    use_container_width=True
):

    if course.strip() == "":

        st.error(
            "Please enter a course name."
        )

    elif marks_obtained > total_marks:

        st.error(
            "Marks obtained cannot be greater than total marks."
        )

    else:

        percentage = (
            marks_obtained / total_marks
        ) * 100

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO marks
                (
                    student_id,
                    course,
                    assessment,
                    marks_obtained,
                    total_marks,
                    percentage
                )
                VALUES
                (%s, %s, %s, %s, %s, %s)
                """,
                (
                    student_id,
                    course.strip(),
                    assessment,
                    marks_obtained,
                    total_marks,
                    percentage
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            st.success(
                "✅ Assessment saved successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Could not save assessment: {e}"
            )


st.divider()


# ==================================================
# MARKS SUMMARY
# ==================================================

st.subheader("📊 Academic Summary")

marks_data = st.session_state.marks

if not marks_data:

    st.info(
        "No marks recorded yet. Add your first assessment above."
    )

else:

    df = pd.DataFrame(marks_data)

    average_percentage = round(
        df["percentage"].mean(),
        1
    )

    highest_percentage = round(
        df["percentage"].max(),
        1
    )

    total_assessments = len(df)


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📈 Average",
            f"{average_percentage}%"
        )

    with col2:

        st.metric(
            "🏆 Highest",
            f"{highest_percentage}%"
        )

    with col3:

        st.metric(
            "📝 Assessments",
            total_assessments
        )


    st.divider()


    # --------------------------------------------------
    # PERFORMANCE CHART
    # --------------------------------------------------

    st.subheader("📈 Performance Overview")

    chart_data = df[
        ["assessment", "percentage"]
    ].copy()

    chart_data = chart_data.set_index(
        "assessment"
    )

    st.bar_chart(
        chart_data,
        y="percentage"
    )


    st.divider()


    # --------------------------------------------------
    # HISTORY
    # --------------------------------------------------

    st.subheader("📋 Assessment History")

    display_df = df[
        [
            "course",
            "assessment",
            "marks_obtained",
            "total_marks",
            "percentage"
        ]
    ].copy()

    display_df["percentage"] = (
        display_df["percentage"]
        .round(1)
        .astype(str)
        + "%"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# NOTE
# --------------------------------------------------

st.divider()

st.caption(
    "Use this section to track academic performance "
    "alongside your StressRadar check-in history."
)