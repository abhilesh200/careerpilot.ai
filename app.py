import streamlit as st
import requests


import streamlit as st
import requests


# ==================================================
# CONFIGURATION
# ==================================================

API_URL = "https://careerpilot-ai-2-qxcm.onrender.com"

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)


# ==================================================
# TEST API CONNECTION
# ==================================================

try:
    test_response = requests.get(
        f"{API_URL}/docs",
        timeout=30
    )

    if test_response.status_code == 200:
        st.sidebar.success("✅ CareerPilot API connected")

    else:
        st.sidebar.warning(
            f"⚠️ API responded with status {test_response.status_code}"
        )

except Exception as e:
    st.sidebar.error("❌ CareerPilot API connection failed")
    st.sidebar.code(str(e))


# ==================================================
# SESSION STATE
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "career_report" not in st.session_state:
    st.session_state.career_report = None

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []

if "career_roles" not in st.session_state:
    st.session_state.career_roles = []

if "roadmap" not in st.session_state:
    st.session_state.roadmap = []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==================================================
# AUTHENTICATION
# ==================================================

if not st.session_state.authenticated:

    st.title("🚀 CareerPilot AI")
    st.write("AI-powered career assistant for students and job seekers.")
    st.divider()

    login_tab, register_tab = st.tabs(["🔐 Login", "📝 Register"])

    with login_tab:

        st.subheader("Welcome Back")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("🔐 Login", use_container_width=True):

            if not login_email.strip() or not login_password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/v1/auth/login",
                        json={
                            "email": login_email.strip(),
                            "password": login_password
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()

                        user_id = result.get("user_id")

                        if not user_id:
                            st.error("Login response did not contain user_id.")
                        else:
                            st.session_state.authenticated = True
                            st.session_state.user = result

                            # Load saved chat history from the database
                            try:
                                history_response = requests.get(
                                    f"{API_URL}/v1/chat/history/{user_id}",
                                    timeout=30
                                )

                                if history_response.status_code == 200:
                                    history_data = history_response.json()
                                    st.session_state.chat_history = [
                                        {
                                            "role": message.get("role", "assistant"),
                                            "content": message.get("content", "")
                                        }
                                        for message in history_data.get("messages", [])
                                        if message.get("content")
                                    ]
                                else:
                                    st.session_state.chat_history = []

                            except requests.exceptions.RequestException:
                                st.session_state.chat_history = []

                            st.success("Login successful!")
                            st.rerun()
                    else:
                        try:
                            detail = response.json().get(
                                "detail",
                                "Invalid email or password."
                            )
                        except Exception:
                            detail = "Invalid email or password."

                        st.error(detail)

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Could not connect to CareerPilot API. "
                        "Make sure FastAPI is running."
                    )
                except requests.exceptions.Timeout:
                    st.error("Login request timed out.")
                except Exception as e:
                    st.error(f"Login error: {e}")

    with register_tab:

        st.subheader("Create Your CareerPilot Account")

        register_name = st.text_input(
            "Name",
            key="register_name"
        )

        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button("📝 Create Account", use_container_width=True):

            if not register_name.strip():
                st.warning("Please enter your name.")
            elif not register_email.strip():
                st.warning("Please enter your email.")
            elif len(register_password) < 6:
                st.warning("Password must contain at least 6 characters.")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/v1/auth/register",
                        json={
                            "name": register_name.strip(),
                            "email": register_email.strip(),
                            "password": register_password
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        st.success(
                            "Account created successfully. "
                            "Please log in."
                        )
                    else:
                        try:
                            detail = response.json().get(
                                "detail",
                                "Registration failed."
                            )
                        except Exception:
                            detail = "Registration failed."

                        st.error(detail)

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Could not connect to CareerPilot API. "
                        "Make sure FastAPI is running."
                    )
                except requests.exceptions.Timeout:
                    st.error("Registration request timed out.")
                except Exception as e:
                    st.error(f"Registration error: {e}")

    st.stop()


# ==================================================
# LOGGED-IN USER HEADER
# ==================================================

with st.sidebar:

    user = st.session_state.get("user") or {}

    st.markdown("### 👤 Account")
    st.write(user.get("name", "User"))
    st.caption(user.get("email", ""))

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.page = "home"
        st.session_state.career_report = None
        st.session_state.resume_skills = []
        st.session_state.missing_skills = []
        st.session_state.career_roles = []
        st.session_state.roadmap = []
        st.rerun()


# ==================================================
# HELPER FUNCTION
# ==================================================

def display_roadmap(roadmap):
    """Display roadmap returned by CareerPilot API."""

    if not roadmap:
        st.info("No learning roadmap available.")
        return

    if isinstance(roadmap, dict):

        for key, value in roadmap.items():

            title = str(key).replace("_", " ").title()

            st.markdown(f"**{title}**")

            if isinstance(value, list):

                for item in value:
                    st.write(f"• {item}")

            else:
                st.write(value)

        return

    if isinstance(roadmap, list):

        for index, step in enumerate(
            roadmap,
            start=1
        ):

            if isinstance(step, dict):

                title = (
                    step.get("title")
                    or step.get("step")
                    or step.get("phase")
                    or step.get("name")
                )

                description = (
                    step.get("description")
                    or step.get("details")
                    or step.get("goal")
                )

                topics = (
                    step.get("topics")
                    or step.get("learn")
                    or step.get("skills")
                )

                if title:

                    st.markdown(
                        f"**Step {index}: {title}**"
                    )

                if description:
                    st.write(description)

                if isinstance(topics, list):

                    for topic in topics:
                        st.write(f"• {topic}")

                elif topics:

                    st.write(f"• {topics}")

                st.divider()

            else:

                st.write(f"• {step}")

        return

    st.write(roadmap)


# ==================================================
# HOME PAGE
# ==================================================

if st.session_state.page == "home":

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.title("🚀 CareerPilot AI")

    st.write(
        "AI-powered career assistant for students and job seekers."
    )

    st.divider()


    # --------------------------------------------------
    # Resume Upload
    # --------------------------------------------------

    st.subheader("📄 Upload Your Resume")

    resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"]
    )


    # --------------------------------------------------
    # Job Description
    # --------------------------------------------------

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=250
    )


    # --------------------------------------------------
    # Generate Career Report
    # --------------------------------------------------

    if st.button(
        "🚀 Generate Career Report",
        use_container_width=True
    ):

        if resume is None:

            st.warning(
                "Please upload your resume."
            )

        elif not job_description.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            try:

                with st.spinner(
                    "🚀 CareerPilot AI is analyzing your resume..."
                ):

                    # ==============================================
                    # 1. RESUME ANALYSIS
                    # ==============================================

                    file_payload = {
                        "file": (
                            resume.name,
                            resume.getvalue(),
                            resume.type
                        )
                    }

                    resume_response = requests.post(
                        f"{API_URL}/v1/resume/analyze",
                        files=file_payload,
                        timeout=120
                    )

                    if resume_response.status_code != 200:

                        st.error(
                            f"Resume API Error: "
                            f"{resume_response.status_code}"
                        )

                        st.code(
                            resume_response.text
                        )

                        st.stop()

                    resume_result = (
                        resume_response.json()
                    )

                    if resume_result.get(
                        "status"
                    ) != "success":

                        st.error(
                            "Resume analysis failed."
                        )

                        st.stop()

                    resume_data = (
                        resume_result["data"]
                    )

                    resume_text = (
                        resume_data["text"]
                    )

                    skills = resume_data.get(
                        "skills",
                        []
                    )


                    # ==============================================
                    # 2. JOB DESCRIPTION MATCH
                    # ==============================================

                    match_response = requests.post(
                        f"{API_URL}/v1/career/analyze",
                        json={
                            "resume_text": resume_text,
                            "job_description": job_description
                        },
                        timeout=120
                    )

                    if match_response.status_code != 200:

                        st.error(
                            f"Career Match API Error: "
                            f"{match_response.status_code}"
                        )

                        st.code(
                            match_response.text
                        )

                        st.stop()

                    match_result = (
                        match_response.json()
                    )

                    if match_result.get(
                        "status"
                    ) != "success":

                        st.error(
                            "Career matching failed."
                        )

                        st.stop()

                    match_data = (
                        match_result["data"]
                    )


                    # ==============================================
                    # 3. CAREER REPORT
                    # ==============================================

                    report_file_payload = {
                        "file": (
                            resume.name,
                            resume.getvalue(),
                            resume.type
                        )
                    }

                    report_response = requests.post(
                        f"{API_URL}/v1/resume/career-report",
                        files=report_file_payload,
                        timeout=120
                    )

                    if report_response.status_code != 200:

                        st.error(
                            f"Career Report API Error: "
                            f"{report_response.status_code}"
                        )

                        st.code(
                            report_response.text
                        )

                        st.stop()

                    report_result = (
                        report_response.json()
                    )

                    if report_result.get(
                        "status"
                    ) != "success":

                        st.error(
                            "Career report generation failed."
                        )

                        st.stop()

                    career_data = (
                        report_result["data"]
                    )


                    # ==============================================
                    # 4. PERSONALIZED ROADMAP
                    # ==============================================

                    roadmap_response = requests.post(
                        f"{API_URL}/v1/career/roadmap",
                        json={
                            "resume_skills": skills
                        },
                        timeout=120
                    )

                    if roadmap_response.status_code != 200:

                        st.error(
                            f"Career Roadmap API Error: "
                            f"{roadmap_response.status_code}"
                        )

                        st.code(
                            roadmap_response.text
                        )

                        st.stop()

                    roadmap_result = (
                        roadmap_response.json()
                    )

                    if roadmap_result.get(
                        "status"
                    ) != "success":

                        st.error(
                            "Career roadmap generation failed."
                        )

                        st.stop()

                    roadmap_data = (
                        roadmap_result["data"]["roadmap"]
                    )


                    # ==============================================
                    # 5. INTERVIEW QUESTIONS
                    # ==============================================

                    interview_response = requests.post(
                        f"{API_URL}/v1/interview/questions",
                        json={
                            "resume_skills": skills,
                            "job_description": job_description
                        },
                        timeout=120
                    )

                    if interview_response.status_code != 200:

                        st.error(
                            f"Interview API Error: "
                            f"{interview_response.status_code}"
                        )

                        st.code(
                            interview_response.text
                        )

                        st.stop()

                    interview_result = (
                        interview_response.json()
                    )

                    if interview_result.get(
                        "status"
                    ) != "success":

                        st.error(
                            "Interview preparation generation failed."
                        )

                        st.stop()

                    interview_data = (
                        interview_result["data"]["questions"]
                    )


                # ==============================================
                # SAVE REPORT
                # ==============================================

                st.session_state.career_report = {

                    "skills": skills,

                    "match_data": match_data,

                    "career_data": career_data,

                    "roadmap_data": roadmap_data,

                    "interview_data": interview_data,

                    "job_description": job_description
                }


                # ==============================================
                # SAVE CHAT CONTEXT
                # ==============================================

                st.session_state.resume_skills = skills

                st.session_state.missing_skills = (
                    career_data.get(
                        "skills_to_develop",
                        []
                    )
                )

                st.session_state.career_roles = (
                    career_data.get(
                        "recommendations",
                        []
                    )
                )

                st.session_state.roadmap = roadmap_data


                # ==============================================
                # SAVE CAREER PROFILE TO DATABASE
                # ==============================================

                user = st.session_state.get("user") or {}
                user_id = user.get("user_id")

                if user_id:

                    profile_response = requests.post(
                        f"{API_URL}/v1/profile/save",
                        json={
                            "user_id": user_id,
                            "resume_skills": skills,
                            "missing_skills": career_data.get(
                                "skills_to_develop",
                                []
                            ),
                            "career_roles": career_data.get(
                                "recommendations",
                                []
                            ),
                            "roadmap": roadmap_data,
                            "resume_text": resume_text
                        },
                        timeout=30
                    )

                    if profile_response.status_code == 200:
                        st.success(
                            "✅ Career profile saved to your account."
                        )
                    else:
                        st.warning(
                            "Career report generated, but the profile "
                            "could not be saved."
                        )


                st.success(
                    "✅ Resume and job description successfully analyzed!"
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to CareerPilot API. "
                    "Make sure FastAPI is running on "
                    "http://127.0.0.1:8000."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "❌ The API request timed out. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    f"❌ Error generating career report: {e}"
                )


    # ==================================================
    # DISPLAY CAREER REPORT
    # ==================================================

    report = st.session_state.career_report

    if report:

        skills = report["skills"]

        match_data = report["match_data"]

        career_data = report["career_data"]

        roadmap_data = report["roadmap_data"]

        interview_data = report["interview_data"]


        # ==============================================
        # RESUME SKILLS
        # ==============================================

        st.divider()

        st.header(
            "🧠 Skills Found in Resume"
        )

        if skills:

            st.write(
                ", ".join(
                    skill.title()
                    for skill in skills
                )
            )

            st.metric(
                "Total Skills",
                len(skills)
            )

        else:

            st.warning(
                "No skills detected in resume."
            )


        # ==============================================
        # JOB DESCRIPTION MATCH
        # ==============================================

        st.divider()

        st.header(
            "📊 Job Description Match"
        )

        match_percentage = match_data.get(
            "match_percentage",
            0
        )

        matched_skills = match_data.get(
            "matched_skills",
            []
        )

        missing_skills = match_data.get(
            "missing_skills",
            []
        )

        extra_skills = match_data.get(
            "extra_skills",
            []
        )


        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Job Skill Match",
                f"{match_percentage:.1f}%"
            )

        with col2:

            st.metric(
                "Matched Skills",
                len(matched_skills)
            )

        with col3:

            st.metric(
                "Missing Skills",
                len(missing_skills)
            )


        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                "**✅ Matched Skills**"
            )

            if matched_skills:

                st.write(
                    ", ".join(
                        skill.title()
                        for skill in matched_skills
                    )
                )

            else:

                st.write("None")


        with col2:

            st.markdown(
                "**⚠️ Missing Skills**"
            )

            if missing_skills:

                st.write(
                    ", ".join(
                        skill.title()
                        for skill in missing_skills
                    )
                )

            else:

                st.write("None")


        with col3:

            st.markdown(
                "**➕ Additional Resume Skills**"
            )

            if extra_skills:

                st.write(
                    ", ".join(
                        skill.title()
                        for skill in extra_skills
                    )
                )

            else:

                st.write("None")


        # ==============================================
        # CAREER FIT
        # ==============================================

        st.divider()

        st.subheader(
            "🎯 Career Fit"
        )

        st.info(
            "Career Fit is based on your resume skills "
            "compared with the skills required for "
            "different career roles."
        )

        top_role = career_data.get(
            "top_role",
            {}
        )


        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Top Career Role",
                top_role.get(
                    "role",
                    "Not available"
                )
            )

        with col2:

            st.metric(
                "Resume-to-Role Fit",
                f"{top_role.get('match_percentage', 0):.1f}%"
            )


        # ==============================================
        # CURRENT JOB MATCH
        # ==============================================

        st.divider()

        st.subheader(
            "📊 Current Job Match"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Job Skill Match",
                f"{match_percentage:.1f}%"
            )

        with col2:

            st.metric(
                "Matched Skills",
                len(matched_skills)
            )

        with col3:

            st.metric(
                "Missing Skills",
                len(missing_skills)
            )


        if matched_skills:

            st.success(
                "Matched Skills: "
                + ", ".join(
                    skill.title()
                    for skill in matched_skills
                )
            )


        if missing_skills:

            st.warning(
                "Skills to Develop: "
                + ", ".join(
                    skill.title()
                    for skill in missing_skills
                )
            )


        # ==============================================
        # CAREER RECOMMENDATIONS
        # ==============================================

        st.divider()

        st.header(
            "🚀 Career Recommendations"
        )

        recommendations = career_data.get(
            "recommendations",
            []
        )

        if recommendations:

            for recommendation in recommendations:

                role = recommendation.get(
                    "role",
                    "Unknown Role"
                )

                match = recommendation.get(
                    "match_percentage",
                    0
                )

                matched = recommendation.get(
                    "matched_skills",
                    []
                )

                missing = recommendation.get(
                    "missing_skills",
                    []
                )

                role_roadmap = recommendation.get(
                    "roadmap",
                    []
                )


                st.subheader(
                    f"💼 {role}"
                )

                st.metric(
                    "Skill Match",
                    f"{match:.1f}%"
                )


                if matched:

                    st.markdown(
                        "**Matched Skills:**"
                    )

                    st.write(
                        ", ".join(
                            skill.title()
                            for skill in matched
                        )
                    )


                if missing:

                    st.markdown(
                        "**Skills to Develop:**"
                    )

                    for skill in missing:

                        st.warning(
                            f"⚠️ {skill.title()}"
                        )


                if role_roadmap:

                    st.markdown(
                        "**Learning Roadmap:**"
                    )

                    display_roadmap(
                        role_roadmap
                    )


                st.divider()


        else:

            st.info(
                "No career recommendations available."
            )


        # ==============================================
        # PERSONALIZED ROADMAP
        # ==============================================

        st.divider()

        st.header(
            "🗺️ Personalized Career Roadmap"
        )

        st.info(
            "A step-by-step learning plan based "
            "on the skills detected in your resume."
        )


        if roadmap_data:

            for phase in roadmap_data:

                phase_name = phase.get(
                    "phase",
                    "Learning Phase"
                )

                duration = phase.get(
                    "duration",
                    "Not specified"
                )

                phase_skills = phase.get(
                    "skills",
                    []
                )

                goal = phase.get(
                    "goal",
                    ""
                )

                project = phase.get(
                    "project",
                    ""
                )

                outcome = phase.get(
                    "outcome",
                    ""
                )


                st.subheader(
                    f"📍 {phase_name}"
                )

                st.caption(
                    f"⏱️ Duration: {duration}"
                )


                if phase_skills:

                    st.markdown(
                        "**📚 Skills to Learn:**"
                    )

                    for skill in phase_skills:

                        st.write(
                            f"• {skill}"
                        )


                if goal:

                    st.markdown(
                        f"**🎯 Goal:** {goal}"
                    )


                if project:

                    st.markdown(
                        f"**🛠️ Recommended Project:** {project}"
                    )


                if outcome:

                    st.markdown(
                        f"**✅ Expected Outcome:** {outcome}"
                    )


                st.divider()


        else:

            st.success(
                "Your current skill set already covers "
                "the roadmap requirements."
            )


        # ==============================================
        # INTERVIEW PREPARATION
        # ==============================================

        st.divider()

        st.header(
            "🎤 Interview Preparation"
        )

        st.info(
            "Practice interview questions generated "
            "from your resume and target job."
        )


        # ==============================================
        # START INTERVIEW BUTTON
        # ==============================================

        if st.button(
            "🎤 Start Interview Answer Practice",
            use_container_width=True
        ):

            st.session_state.page = "interview"

            st.rerun()


        # ==============================================
        # QUESTION PREVIEW
        # ==============================================

        technical_questions = interview_data.get(
            "technical",
            []
        )

        if technical_questions:

            st.subheader(
                "💻 Technical Questions"
            )

            for index, question in enumerate(
                technical_questions,
                start=1
            ):

                st.markdown(
                    f"**{index}. {question}**"
                )


        project_questions = interview_data.get(
            "project",
            []
        )

        if project_questions:

            st.subheader(
                "🚀 Project Questions"
            )

            for index, question in enumerate(
                project_questions,
                start=1
            ):

                st.markdown(
                    f"**{index}. {question}**"
                )


        missing_skill_questions = interview_data.get(
            "missing_skills",
            []
        )

        if missing_skill_questions:

            st.subheader(
                "⚠️ Missing Skill Questions"
            )

            for index, question in enumerate(
                missing_skill_questions,
                start=1
            ):

                st.markdown(
                    f"**{index}. {question}**"
                )


        behavioral_questions = interview_data.get(
            "behavioral",
            []
        )

        if behavioral_questions:

            st.subheader(
                "🧠 Behavioral Questions"
            )

            for index, question in enumerate(
                behavioral_questions,
                start=1
            ):

                st.markdown(
                    f"**{index}. {question}**"
                )


        # ==============================================
        # JOB-SPECIFIC SKILLS
        # ==============================================

        st.divider()

        st.header(
            "🎯 Job-Specific Skills to Develop"
        )

        if missing_skills:

            for skill in missing_skills:

                st.warning(
                    f"📌 {skill.title()}"
                )

        else:

            st.success(
                "Your resume covers all detected job skills."
            )


        # ==============================================
        # CAREER DEVELOPMENT SKILLS
        # ==============================================

        st.header(
            "📚 Career Development Skills"
        )

        skills_to_develop = career_data.get(
            "skills_to_develop",
            []
        )

        if skills_to_develop:

            for skill in skills_to_develop:

                st.warning(
                    f"📌 {skill.title()}"
                )

        else:

            st.success(
                "No additional skills to develop "
                "were identified."
            )


        # ==============================================
        # SUMMARY
        # ==============================================

        st.divider()

        st.header(
            "📈 Career Analysis Summary"
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Roles Analyzed",
                career_data.get(
                    "total_roles_analyzed",
                    0
                )
            )


        with col2:

            st.metric(
                "Resume Skills",
                len(skills)
            )


        with col3:

            st.metric(
                "Matched Job Skills",
                len(matched_skills)
            )


        with col4:

            st.metric(
                "Missing Job Skills",
                len(missing_skills)
            )


# ==================================================
# INTERVIEW PRACTICE PAGE
# ==================================================

elif st.session_state.page == "interview":

    report = st.session_state.career_report


    # --------------------------------------------------
    # Safety Check
    # --------------------------------------------------

    if not report:

        st.session_state.page = "home"

        st.rerun()


    skills = report["skills"]

    interview_data = report["interview_data"]


    # --------------------------------------------------
    # Back to Home
    # --------------------------------------------------

    if st.button(
        "← Back to Home",
        use_container_width=True
    ):

        st.session_state.page = "home"

        st.rerun()


    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.title(
        "🎤 Interview Answer Practice"
    )

    st.write(
        "Practice answering interview questions "
        "and receive structured feedback from CareerPilot."
    )

    st.divider()


    # --------------------------------------------------
    # Combine Questions
    # --------------------------------------------------

    interview_questions = (

        interview_data.get(
            "technical",
            []
        )

        + interview_data.get(
            "project",
            []
        )

        + interview_data.get(
            "missing_skills",
            []
        )

        + interview_data.get(
            "behavioral",
            []
        )
    )


    if not interview_questions:

        st.info(
            "No interview questions are available."
        )

    else:

        # --------------------------------------------------
        # Select Question
        # --------------------------------------------------

        selected_question = st.selectbox(
            "Select an interview question",
            interview_questions
        )


        # --------------------------------------------------
        # User Answer
        # --------------------------------------------------

        user_answer = st.text_area(
            "🎤 Your Answer",
            placeholder=(
                "Type your interview answer here..."
            ),
            height=220
        )


        # --------------------------------------------------
        # Evaluate Button
        # --------------------------------------------------

        if st.button(
            "🚀 Evaluate My Answer",
            use_container_width=True
        ):

            if not user_answer.strip():

                st.warning(
                    "Please enter your answer first."
                )

            else:

                try:

                    with st.spinner(
                        "🤖 CareerPilot is evaluating your answer..."
                    ):

                        evaluation_response = requests.post(

                            f"{API_URL}/v1/interview/evaluate",

                            json={

                                "question":
                                    selected_question,

                                "answer":
                                    user_answer,

                                "resume_skills":
                                    skills
                            },

                            timeout=120
                        )


                    # --------------------------------------------------
                    # API Error
                    # --------------------------------------------------

                    if evaluation_response.status_code != 200:

                        st.error(
                            "Interview evaluation failed."
                        )

                        st.code(
                            evaluation_response.text
                        )


                    else:

                        evaluation_result = (
                            evaluation_response.json()
                        )


                        if evaluation_result.get(
                            "status"
                        ) != "success":

                            st.error(
                                "Could not evaluate your answer."
                            )


                        else:

                            evaluation = (
                                evaluation_result["data"]
                            )


                            # ==========================================
                            # EVALUATION RESULT
                            # ==========================================

                            st.divider()

                            st.header(
                                "🤖 CareerPilot Evaluation"
                            )


                            # --------------------------------------------------
                            # Answer Quality
                            # --------------------------------------------------

                            st.metric(
                                "⭐ Answer Quality",
                                evaluation.get(
                                    "answer_quality",
                                    "Not available"
                                )
                            )


                            # --------------------------------------------------
                            # Score Breakdown
                            # --------------------------------------------------

                            st.subheader(
                                "📊 Interview Performance"
                            )


                            score_breakdown = evaluation.get(
                                "score_breakdown",
                                {}
                            )


                            col1, col2 = st.columns(2)


                            with col1:

                                st.metric(
                                    "🎯 Overall Score",
                                    f"{evaluation.get('overall_score', 0)}/100"
                                )

                                st.metric(
                                    "🧠 Technical Understanding",
                                    f"{score_breakdown.get('technical_understanding', 0)}/100"
                                )


                            with col2:

                                st.metric(
                                    "🎯 Relevance",
                                    f"{score_breakdown.get('relevance', 0)}/100"
                                )

                                st.metric(
                                    "💬 Clarity",
                                    f"{score_breakdown.get('clarity', 0)}/100"
                                )


                            st.metric(
                                "📝 Completeness",
                                f"{score_breakdown.get('completeness', 0)}/100"
                            )


                            # --------------------------------------------------
                            # Answer Length
                            # --------------------------------------------------

                            st.write(
                                "**Answer Length:**",
                                evaluation.get(
                                    "word_count",
                                    0
                                ),
                                "words"
                            )


                            # --------------------------------------------------
                            # Strengths
                            # --------------------------------------------------

                            st.subheader(
                                "✅ What You Did Well"
                            )


                            for item in evaluation.get(
                                "what_you_did_well",
                                []
                            ):

                                st.write(
                                    f"• {item}"
                                )


                            # --------------------------------------------------
                            # Improvements
                            # --------------------------------------------------

                            st.subheader(
                                "⚠️ What Could Be Improved"
                            )


                            for item in evaluation.get(
                                "what_could_be_improved",
                                []
                            ):

                                st.write(
                                    f"• {item}"
                                )


                            # --------------------------------------------------
                            # Suggested Better Answer
                            # --------------------------------------------------

                            st.subheader(
                                "💡 Suggested Better Answer"
                            )


                            st.info(
                                evaluation.get(
                                    "suggested_better_answer",
                                    "No suggestion available."
                                )
                            )


                            # --------------------------------------------------
                            # Follow-up Question
                            # --------------------------------------------------

                            st.subheader(
                                "📌 Follow-up Question"
                            )


                            st.success(
                                evaluation.get(
                                    "follow_up_question",
                                    "No follow-up question available."
                                )
                            )


                            # --------------------------------------------------
                            # Mentioned Skills
                            # --------------------------------------------------

                            mentioned_skills = evaluation.get(
                                "mentioned_resume_skills",
                                []
                            )


                            if mentioned_skills:

                                st.subheader(
                                    "✅ Skills Mentioned"
                                )

                                st.write(
                                    ", ".join(
                                        mentioned_skills
                                    )
                                )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to CareerPilot API. "
                        "Make sure FastAPI is running."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "CareerPilot API request timed out."
                    )

                except Exception as e:

                    st.error(
                        f"Could not evaluate your answer: {e}"
                    )


# ==================================================
# CAREERPILOT AI CHAT
# ==================================================

st.markdown("---")
st.header("🤖 CareerPilot AI Chat")

# --------------------------------------------------
# Initialize Chat History
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.chat_history:
    role = message.get("role", "assistant")
    content = message.get("content", "")

    if content:
        with st.chat_message(role):
            st.write(content)

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

user_message = st.chat_input(
    "Ask CareerPilot about your career..."
)

if user_message:

    # --------------------------------------------------
    # Get Logged-In User
    # --------------------------------------------------

    user = st.session_state.get("user") or {}
    user_id = user.get("user_id")

    if not user_id:
        st.error(
            "User ID not found. Please logout and login again."
        )
        st.stop()

    # --------------------------------------------------
    # Get Career Context
    # --------------------------------------------------

    resume_skills = st.session_state.get(
        "resume_skills",
        []
    )

    missing_skills = st.session_state.get(
        "missing_skills",
        []
    )

    career_roles = st.session_state.get(
        "career_roles",
        []
    )

    roadmap = st.session_state.get(
        "roadmap",
        []
    )

    # --------------------------------------------------
    # Save User Message Locally
    # --------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # --------------------------------------------------
    # Build Full Conversation History
    # --------------------------------------------------

    messages = [
        {
            "role": message.get("role", "assistant"),
            "content": message.get("content", "")
        }
        for message in st.session_state.chat_history
        if message.get("content")
    ]

    # --------------------------------------------------
    # API Payload
    # --------------------------------------------------

    payload = {
        "user_id": user_id,
        "model": "careerpilot",
        "messages": messages,
        "resume_skills": resume_skills,
        "missing_skills": missing_skills,
        "career_roles": career_roles,
        "roadmap": roadmap
    }

    # --------------------------------------------------
    # Send Request To API
    # --------------------------------------------------

    try:

        response = requests.post(
               f"{API_URL}/v1/chat/completions",
    json=payload,
    timeout=120

        )

        # --------------------------------------------------
        # Successful Response
        # --------------------------------------------------

        if response.status_code == 200:

            result = response.json()

            choices = result.get("choices", [])

            if not choices:
                raise ValueError(
                    "API response did not contain choices."
                )

            answer = (
                choices[0]
                .get("message", {})
                .get("content", "")
            )

            if not answer:
                raise ValueError(
                    "API response did not contain an assistant answer."
                )

            # Save assistant response locally.
            # Do NOT read user_id/name/email from the chat response.
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            # --------------------------------------------------
            # Display New Messages
            # --------------------------------------------------

            with st.chat_message("user"):
                st.write(user_message)

            with st.chat_message("assistant"):
                st.write(answer)

        # --------------------------------------------------
        # API Error
        # --------------------------------------------------

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.code(response.text)

            # Remove failed user message
            if st.session_state.chat_history:
                st.session_state.chat_history.pop()

    # --------------------------------------------------
    # Connection Error
    # --------------------------------------------------

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to CareerPilot API. "
            "Make sure FastAPI is running on http://127.0.0.1:8000."
        )

        if st.session_state.chat_history:
            st.session_state.chat_history.pop()

    # --------------------------------------------------
    # Timeout
    # --------------------------------------------------

    except requests.exceptions.Timeout:

        st.error(
            "CareerPilot API request timed out."
        )

        if st.session_state.chat_history:
            st.session_state.chat_history.pop()

    # --------------------------------------------------
    # Other Error
    # --------------------------------------------------

    except Exception as e:

        st.error(
            f"Chat error: {e}"
        )

        if st.session_state.chat_history:
            st.session_state.chat_history.pop()
