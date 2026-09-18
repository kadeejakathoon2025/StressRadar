import streamlit as st
from database import save_profile


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("👤 My Student Profile")

st.write(
    "Let's set up your profile so StressRadar can "
    "personalize your study and stress management."
)

st.divider()


# ---------------------------------------------------------
# STUDENT INFORMATION
# ---------------------------------------------------------

st.subheader("🎓 Student Information")

name = st.text_input(
    "Your Name"
)


# ---------------------------------------------------------
# COUNTRY
# ---------------------------------------------------------

country = st.selectbox(
    "🌍 Country",
    [
        "Select Country",
        "India",
        "Other"
    ]
)


# ---------------------------------------------------------
# STATE / UT
# ---------------------------------------------------------

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

    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry",

    "Other"
]


if country == "India":

    state = st.selectbox(
        "📍 State / Union Territory",
        states
    )

else:

    state = "Other"


# ---------------------------------------------------------
# COLLEGE DATABASE
# ---------------------------------------------------------

college_data = {

    "Andhra Pradesh": [
        "Andhra University",
        "JNTU Anantapur",
        "JNTU Kakinada",
        "Sri Venkateswara University",
        "KL University",
        "VIT-AP University",
        "GITAM University",
        "Other"
    ],

    "Arunachal Pradesh": [
        "North Eastern Regional Institute of Science and Technology (NERIST)",
        "Rajiv Gandhi University",
        "National Institute of Technology Arunachal Pradesh",
        "Other"
    ],

    "Assam": [
        "Indian Institute of Technology Guwahati",
        "Assam University",
        "Gauhati University",
        "Dibrugarh University",
        "Tezpur University",
        "National Institute of Technology Silchar",
        "Other"
    ],

    "Bihar": [
        "Indian Institute of Technology Patna",
        "National Institute of Technology Patna",
        "Patna University",
        "Aryabhatta Knowledge University",
        "Other"
    ],

    "Chhattisgarh": [
        "Indian Institute of Technology Bhilai",
        "National Institute of Technology Raipur",
        "Pt. Ravishankar Shukla University",
        "Other"
    ],

    "Goa": [
        "Goa University",
        "National Institute of Technology Goa",
        "Goa Institute of Management",
        "Other"
    ],

    "Gujarat": [
        "Indian Institute of Technology Gandhinagar",
        "Indian Institute of Information Technology Vadodara",
        "Gujarat Technological University",
        "Nirma University",
        "Dhirubhai Ambani Institute of Information and Communication Technology",
        "The Maharaja Sayajirao University of Baroda",
        "Sardar Vallabhbhai National Institute of Technology Surat",
        "Other"
    ],

    "Haryana": [
        "Indian Institute of Technology Delhi - Haryana campus",
        "National Institute of Technology Kurukshetra",
        "Kurukshetra University",
        "Ashoka University",
        "Manav Rachna International Institute of Research and Studies",
        "Other"
    ],

    "Himachal Pradesh": [
        "Indian Institute of Technology Mandi",
        "National Institute of Technology Hamirpur",
        "Himachal Pradesh University",
        "Other"
    ],

    "Jharkhand": [
        "Indian Institute of Technology (ISM) Dhanbad",
        "National Institute of Technology Jamshedpur",
        "Birla Institute of Technology Mesra",
        "Ranchi University",
        "Other"
    ],

    "Karnataka": [
        "Indian Institute of Science Bengaluru",
        "Indian Institute of Technology Dharwad",
        "National Institute of Technology Karnataka",
        "Visvesvaraya Technological University",
        "Bangalore University",
        "Bangalore Institute of Technology",
        "RV College of Engineering",
        "BMS College of Engineering",
        "Manipal Academy of Higher Education",
        "Christ University",
        "Other"
    ],

    "Kerala": [
        "University of Kerala",
        "Mahatma Gandhi University",
        "University of Calicut",
        "Kannur University",
        "APJ Abdul Kalam Technological University",
        "Indian Institute of Technology Palakkad",
        "National Institute of Technology Calicut",
        "Indian Institute of Science Education and Research Thiruvananthapuram",
        "College of Engineering Trivandrum",
        "Government Engineering College Thrissur",
        "Government Engineering College Kozhikode",
        "Government Engineering College Palakkad",
        "TKM College of Engineering",
        "Model Engineering College",
        "NSS College of Engineering",
        "Rajagiri School of Engineering & Technology",
        "Amrita Vishwa Vidyapeetham",
        "SCMS School of Engineering and Technology",
        "Saintgits College of Engineering",
        "Federal Institute of Science and Technology",
        "Mar Baselios College of Engineering and Technology",
        "LBS Institute of Technology for Women",
        "Jyothi Engineering College",
        "Christ College of Engineering",
        "Adi Shankara Institute of Engineering and Technology",
        "Sahrdaya College of Engineering and Technology",
        "Vidya Academy of Science and Technology",
        "Amal Jyothi College of Engineering",
        "Muthoot Institute of Technology and Science",
        "College of Engineering Chengannur",
        "College of Engineering Attingal",
        "College of Engineering Karunagappally",
        "Other"
    ],

    "Madhya Pradesh": [
        "Indian Institute of Technology Indore",
        "Maulana Azad National Institute of Technology Bhopal",
        "Indian Institute of Information Technology Design and Manufacturing Jabalpur",
        "Barkatullah University",
        "Devi Ahilya Vishwavidyalaya",
        "Other"
    ],

    "Maharashtra": [
        "Indian Institute of Technology Bombay",
        "Indian Institute of Information Technology Pune",
        "National Institute of Technology Nagpur",
        "University of Mumbai",
        "Savitribai Phule Pune University",
        "Visvesvaraya National Institute of Technology",
        "College of Engineering Pune",
        "VJTI Mumbai",
        "Symbiosis International University",
        "Amity University Mumbai",
        "Other"
    ],

    "Manipur": [
        "National Institute of Technology Manipur",
        "Manipur University",
        "Indian Institute of Information Technology Senapati",
        "Other"
    ],

    "Meghalaya": [
        "North-Eastern Hill University",
        "National Institute of Technology Meghalaya",
        "Other"
    ],

    "Mizoram": [
        "Mizoram University",
        "National Institute of Technology Mizoram",
        "Other"
    ],

    "Nagaland": [
        "Nagaland University",
        "National Institute of Technology Nagaland",
        "Other"
    ],

    "Odisha": [
        "Indian Institute of Technology Bhubaneswar",
        "National Institute of Technology Rourkela",
        "Utkal University",
        "KIIT University",
        "Siksha 'O' Anusandhan",
        "Other"
    ],

    "Punjab": [
        "Indian Institute of Technology Ropar",
        "National Institute of Technology Jalandhar",
        "Panjab University",
        "Lovely Professional University",
        "Thapar Institute of Engineering and Technology",
        "Other"
    ],

    "Rajasthan": [
        "Indian Institute of Technology Jodhpur",
        "Malaviya National Institute of Technology Jaipur",
        "University of Rajasthan",
        "Birla Institute of Technology and Science Pilani",
        "Manipal University Jaipur",
        "Amity University Rajasthan",
        "Other"
    ],

    "Sikkim": [
        "National Institute of Technology Sikkim",
        "Sikkim University",
        "Other"
    ],

    "Tamil Nadu": [
        "Indian Institute of Technology Madras",
        "National Institute of Technology Tiruchirappalli",
        "Anna University",
        "University of Madras",
        "Coimbatore Institute of Technology",
        "PSG College of Technology",
        "Vellore Institute of Technology",
        "SRM Institute of Science and Technology",
        "Amrita Vishwa Vidyapeetham - Coimbatore",
        "Other"
    ],

    "Telangana": [
        "Indian Institute of Technology Hyderabad",
        "International Institute of Information Technology Hyderabad",
        "National Institute of Technology Warangal",
        "University of Hyderabad",
        "Osmania University",
        "BITS Pilani Hyderabad Campus",
        "Other"
    ],

    "Tripura": [
        "National Institute of Technology Agartala",
        "Tripura University",
        "Other"
    ],

    "Uttar Pradesh": [
        "Indian Institute of Technology Kanpur",
        "Indian Institute of Technology Banaras Hindu University",
        "Indian Institute of Technology Noida",
        "National Institute of Technology Allahabad",
        "Aligarh Muslim University",
        "Banaras Hindu University",
        "University of Lucknow",
        "Amity University Noida",
        "Shiv Nadar University",
        "Other"
    ],

    "Uttarakhand": [
        "Indian Institute of Technology Roorkee",
        "National Institute of Technology Uttarakhand",
        "University of Petroleum and Energy Studies",
        "Graphic Era University",
        "Other"
    ],

    "West Bengal": [
        "Indian Institute of Technology Kharagpur",
        "Indian Institute of Engineering Science and Technology Shibpur",
        "National Institute of Technology Durgapur",
        "Jadavpur University",
        "University of Calcutta",
        "University of Burdwan",
        "Other"
    ],

    "Delhi": [
        "Indian Institute of Technology Delhi",
        "University of Delhi",
        "Jawaharlal Nehru University",
        "Jamia Millia Islamia",
        "Indraprastha Institute of Information Technology Delhi",
        "Delhi Technological University",
        "National Institute of Technology Delhi",
        "Other"
    ],

    "Jammu and Kashmir": [
        "Indian Institute of Technology Jammu",
        "National Institute of Technology Srinagar",
        "University of Jammu",
        "University of Kashmir",
        "Other"
    ],

    "Ladakh": [
        "University of Ladakh",
        "Other"
    ],

    "Chandigarh": [
        "Panjab University",
        "Post Graduate Institute of Medical Education and Research",
        "Other"
    ],

    "Puducherry": [
        "Pondicherry University",
        "National Institute of Technology Puducherry",
        "Other"
    ],

    "Andaman and Nicobar Islands": [
        "Andaman and Nicobar Islands Institute of Technology",
        "Other"
    ],

    "Dadra and Nagar Haveli and Daman and Diu": [
        "Government College of Engineering, Daman",
        "Other"
    ],

    "Lakshadweep": [
        "Other"
    ],

    "Other": [
        "Other"
    ]
}


# ---------------------------------------------------------
# COLLEGE SELECTION
# ---------------------------------------------------------

if country == "India":

    if state == "Select State / Union Territory":

        college = "Select College"

        st.info(
            "📍 Select your state to see colleges and universities."
        )

    else:

        available_colleges = college_data.get(
            state,
            ["Other"]
        )

        college = st.selectbox(
            "🏫 College / University",
            [
                "Select College",
                *available_colleges
            ]
        )

else:

    college = st.text_input(
        "🏫 College / University",
        placeholder="Enter your college or university"
    )


# ---------------------------------------------------------
# OTHER COLLEGE
# ---------------------------------------------------------

if college == "Other":

    custom_college = st.text_input(
        "✏️ Enter your College / University",
        placeholder="Type your institution name"
    )

    if custom_college.strip():

        college = custom_college.strip()


# ---------------------------------------------------------
# DEPARTMENT
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# YEAR
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# SEMESTER
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# COURSES
# ---------------------------------------------------------

st.divider()

st.subheader("📚 Your Courses")

st.caption(
    "Enter the subjects you are studying this semester."
)

course1 = st.text_input("Course 1")
course2 = st.text_input("Course 2")
course3 = st.text_input("Course 3")
course4 = st.text_input("Course 4")
course5 = st.text_input("Course 5")
course6 = st.text_input("Course 6")

courses = [
    course1,
    course2,
    course3,
    course4,
    course5,
    course6
]

courses = [
    course.strip()
    for course in courses
    if course.strip()
]


# ---------------------------------------------------------
# COURSE DETAILS
# ---------------------------------------------------------

course_details = {}

if courses:

    st.divider()

    st.subheader("🎯 Your Subject Details")

    for course in courses:

        st.markdown(
            f"### 📖 {course}"
        )

        difficulty = st.select_slider(
            f"How difficult is {course} for you?",
            options=[
                "Easy",
                "Medium",
                "Difficult"
            ],
            value="Medium",
            key=f"difficulty_{course}"
        )

        confidence = st.slider(
            f"How confident are you in {course}?",
            min_value=1,
            max_value=10,
            value=5,
            key=f"confidence_{course}"
        )

        course_details[course] = {
            "difficulty": difficulty,
            "confidence": confidence
        }


# ---------------------------------------------------------
# CREATE PROFILE
# ---------------------------------------------------------

st.divider()

if st.button(
    "🚀 Create My Profile",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------
    # VALIDATION
    # -----------------------------------------

    if not name.strip():

        st.error(
            "Please enter your name."
        )

    elif country == "Select Country":

        st.error(
            "Please select your country."
        )

    elif country == "India" and state == "Select State / Union Territory":

        st.error(
            "Please select your state / union territory."
        )

    elif not college or college == "Select College":

        st.error(
            "Please select or enter your college."
        )

    elif department == "Select Department":

        st.error(
            "Please select your department."
        )

    elif year == "Select Year":

        st.error(
            "Please select your year."
        )

    elif semester == "Select Semester":

        st.error(
            "Please select your semester."
        )

    elif len(courses) == 0:

        st.error(
            "Please enter at least one course."
        )

    else:

        # -----------------------------------------
        # SAVE PROFILE IN SESSION
        # -----------------------------------------

        st.session_state.profile = {

            "name": name.strip(),

            "country": country,

            "state": state,

            "college": college,

            "department": department,

            "year": year,

            "semester": semester,

            "courses": courses,

            "course_details": course_details
        }

        # -----------------------------------------
        # SAVE PROFILE IN MYSQL
        # -----------------------------------------

        try:

            course_data = []

            for course in courses:

                course_data.append(
                    (
                        course,
                        course_details[course]["difficulty"],
                        course_details[course]["confidence"]
                    )
                )

            student_id = save_profile(
                name.strip(),
                country,
                state,
                college,
                department,
                year,
                semester,
                course_data
            )

            st.session_state.student_id = student_id

            st.success(
                "🎉 Your profile has been created and saved to the database!"
            )

            st.balloons()

            st.info(
                "Your profile is ready! "
                "You can now open 📊 Daily Check-in from the sidebar."
            )

        except Exception as e:

            st.error(
                f"❌ Profile could not be saved to MySQL: {e}"
            )