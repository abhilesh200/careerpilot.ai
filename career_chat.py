import re


def _normalize(text):
    """Normalize user input for reliable intent matching."""
    text = str(text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _has_any(message, phrases):
    return any(phrase in message for phrase in phrases)


def _format_skills(skills):
    if not skills:
        return "No skills have been detected yet."

    return ", ".join(
        skill.title() for skill in sorted(set(skills))
    )


def _role_names(career_roles):
    roles = []

    for role in career_roles or []:
        if isinstance(role, dict):
            name = role.get("role")
            if name:
                roles.append(name)

    return roles


def _find_role(career_roles, message):
    for role in career_roles or []:
        if not isinstance(role, dict):
            continue

        role_name = role.get("role", "")

        if role_name and role_name.lower() in message:
            return role

    return None


def _career_summary(career_roles):
    if not career_roles:
        return (
            "I don't have your career analysis yet. "
            "Generate your Career Report first."
        )

    lines = []

    for role in career_roles:
        if not isinstance(role, dict):
            continue

        name = role.get("role")
        percentage = role.get("match_percentage")

        if not name:
            continue

        try:
            percentage = float(percentage)
            lines.append(f"• {name}: {percentage:.1f}%")
        except (TypeError, ValueError):
            lines.append(f"• {name}")

    if not lines:
        return "I don't have enough career-role information yet."

    return (
        "Your current CareerPilot role analysis is:\n\n"
        + "\n".join(lines)
    )


# ============================================================
# Technical Knowledge
# ============================================================

TECH_TOPICS = {

    "tuple": (
        "A tuple is an ordered and immutable collection in Python.\n\n"
        "Example:\n"
        "numbers = (10, 20, 30)\n\n"
        "Key points:\n"
        "• Ordered\n"
        "• Immutable\n"
        "• Allows duplicate values\n"
        "• Supports indexing and slicing\n\n"
        "Use a tuple when the collection should not be changed."
    ),

    "list": (
        "A list is an ordered and mutable collection in Python.\n\n"
        "Example:\n"
        "numbers = [10, 20, 30]\n\n"
        "Unlike a tuple, a list can be modified after creation.\n"
        "For example, you can append, remove or update elements."
    ),

    "set": (
        "A set is an unordered collection of unique elements in Python.\n\n"
        "Example:\n"
        "skills = {'Python', 'SQL', 'Python'}\n\n"
        "The duplicate Python value is removed.\n\n"
        "Sets are useful when you need uniqueness and fast membership checks."
    ),

    "dictionary": (
        "A dictionary stores data as key-value pairs in Python.\n\n"
        "Example:\n"
        "student = {'name': 'Abhilesh', 'skill': 'Python'}\n\n"
        "You can access a value using its key:\n"
        "student['name']"
    ),

    "dataframe": (
        "A DataFrame is a two-dimensional table-like data structure "
        "provided by Pandas.\n\n"
        "It contains rows and columns and is commonly used for "
        "data cleaning, analysis and feature preparation.\n\n"
        "Example:\n"
        "import pandas as pd\n"
        "df = pd.read_csv('data.csv')"
    ),

    "python": (
        "Python is a high-level programming language widely used in "
        "data analysis, machine learning, AI, automation and backend development.\n\n"
        "For your CareerPilot career path, useful Python areas include:\n"
        "• Functions and OOP\n"
        "• NumPy and Pandas\n"
        "• Scikit-learn\n"
        "• APIs with FastAPI\n"
        "• Data processing and automation"
    ),

    "machine learning": (
        "Machine Learning is a field of AI where models learn patterns "
        "from data and use those patterns to make predictions or decisions.\n\n"
        "A practical ML workflow is:\n"
        "1. Collect data\n"
        "2. Clean and explore the data\n"
        "3. Engineer features\n"
        "4. Split the data\n"
        "5. Train a model\n"
        "6. Evaluate the model\n"
        "7. Deploy and monitor it"
    ),

    "deep learning": (
        "Deep Learning is a branch of machine learning based on neural "
        "networks with multiple layers.\n\n"
        "It is commonly used for:\n"
        "• Computer vision\n"
        "• Natural language processing\n"
        "• Speech processing\n"
        "• Generative AI\n\n"
        "Popular frameworks include TensorFlow and PyTorch."
    ),

    "nlp": (
        "Natural Language Processing (NLP) is a field of AI focused on "
        "working with human language.\n\n"
        "Common NLP tasks include:\n"
        "• Text classification\n"
        "• Sentiment analysis\n"
        "• Named entity recognition\n"
        "• Question answering\n"
        "• Text generation\n"
        "• Summarization"
    ),

    "sql": (
        "SQL is used to store, retrieve and analyze data in relational databases.\n\n"
        "Important SQL topics for data roles include:\n"
        "• SELECT and filtering\n"
        "• GROUP BY and aggregations\n"
        "• JOINs\n"
        "• Subqueries\n"
        "• Window functions\n"
        "• CTEs"
    ),

    "regression": (
        "Regression is a supervised machine-learning problem where the "
        "target is usually a continuous numerical value.\n\n"
        "Examples include predicting:\n"
        "• House prices\n"
        "• Sales\n"
        "• Revenue\n"
        "• Delivery time\n\n"
        "Common algorithms include Linear Regression, Random Forest "
        "Regression and Gradient Boosting."
    ),

    "classification": (
        "Classification is a supervised machine-learning problem where "
        "the model predicts a category or class.\n\n"
        "Examples:\n"
        "• Spam vs non-spam\n"
        "• Fraud vs non-fraud\n"
        "• Disease vs no disease\n\n"
        "Common algorithms include Logistic Regression, Decision Trees, "
        "Random Forest and Support Vector Machines."
    ),

    "docker": (
        "Docker is a platform for packaging an application and its "
        "dependencies into containers.\n\n"
        "For an ML project, Docker can package:\n"
        "• Python environment\n"
        "• Dependencies\n"
        "• FastAPI application\n"
        "• Model files\n\n"
        "This makes deployment more reproducible."
    ),

    "fastapi": (
        "FastAPI is a Python framework for building APIs.\n\n"
        "It is useful for ML projects because you can expose a trained "
        "model through REST endpoints and validate incoming requests "
        "using Python type hints and Pydantic."
    ),

    "api": (
        "An API is an interface that allows software systems to communicate.\n\n"
        "For example, your CareerPilot Streamlit frontend sends a request "
        "to your FastAPI backend, and the backend returns JSON data.\n\n"
        "Your project uses endpoints such as:\n"
        "• /v1/resume/analyze\n"
        "• /v1/career/report\n"
        "• /v1/career/roadmap\n"
        "• /v1/chat/completions"
    ),

    "statistics": (
        "Statistics helps you understand data and make evidence-based conclusions.\n\n"
        "Important topics for data science include:\n"
        "• Mean, median and variance\n"
        "• Probability\n"
        "• Distributions\n"
        "• Correlation\n"
        "• Hypothesis testing\n"
        "• Confidence intervals"
    ),

    "pandas": (
        "Pandas is a Python library for data manipulation and analysis.\n\n"
        "Common operations include:\n"
        "• Reading CSV files\n"
        "• Filtering rows\n"
        "• Selecting columns\n"
        "• Handling missing values\n"
        "• Grouping data\n"
        "• Merging datasets"
    ),

    "numpy": (
        "NumPy is a Python library for numerical computing.\n\n"
        "It provides efficient arrays and mathematical operations and "
        "is widely used underneath libraries such as Pandas and Scikit-learn."
    ),

    "scikit-learn": (
        "Scikit-learn is a Python machine-learning library.\n\n"
        "It provides tools for:\n"
        "• Classification\n"
        "• Regression\n"
        "• Clustering\n"
        "• Feature preprocessing\n"
        "• Model selection\n"
        "• Model evaluation"
    ),

    "transformers": (
        "Transformers are neural-network architectures designed to work "
        "efficiently with sequential or language data using attention mechanisms.\n\n"
        "They are central to modern NLP and many large language models."
    ),

    "llm": (
        "An LLM, or Large Language Model, is a neural-network model trained "
        "on large amounts of text to understand and generate language.\n\n"
        "LLM applications can include:\n"
        "• Chatbots\n"
        "• Question answering\n"
        "• Summarization\n"
        "• Code assistance\n"
        "• Document analysis"
    ),

    "git": (
        "Git is a distributed version-control system used to track code changes.\n\n"
        "Important commands include:\n"
        "• git clone\n"
        "• git status\n"
        "• git add\n"
        "• git commit\n"
        "• git pull\n"
        "• git push"
    )
}


def _technical_answer(message):
    # Most specific topics first.
    ordered_topics = [
        "machine learning",
        "deep learning",
        "scikit-learn",
        "natural language processing",
        "transformers",
        "classification",
        "regression",
        "dataframe",
        "statistics",
        "dictionary",
        "python",
        "pandas",
        "numpy",
        "docker",
        "fastapi",
        "tuple",
        "list",
        "set",
        "sql",
        "nlp",
        "llm",
        "git",
        "api"
    ]

    for topic in ordered_topics:
        if topic in message:
            return TECH_TOPICS[topic]

    return None



def _context_skill_list(skills):
    return [str(skill).strip() for skill in (skills or []) if str(skill).strip()]


def _missing_skill_response(missing_skills, career_roles):
    if not missing_skills:
        return (
            "Your current CareerPilot analysis does not show any major "
            "missing skills."
        )

    response = (
        "Based on your current CareerPilot analysis, "
        "you should develop:\n\n"
        + "\n".join(
            f"• {skill.title()}"
            for skill in sorted(set(missing_skills))
        )
    )

    if career_roles:
        response += (
            "\n\nThese skills can help strengthen your fit for the "
            "career roles identified in your analysis."
        )

    return response


def _why_skill_response(skill, resume_skills, missing_skills, career_roles):
    skill_lower = skill.lower()

    resume_lower = {
        str(item).lower().strip()
        for item in (resume_skills or [])
    }

    missing_lower = {
        str(item).lower().strip()
        for item in (missing_skills or [])
    }

    role_matches = []

    for role in career_roles or []:
        if not isinstance(role, dict):
            continue

        role_name = role.get("role")
        role_missing = {
            str(item).lower().strip()
            for item in role.get("missing_skills", [])
        }

        if skill_lower in role_missing and role_name:
            role_matches.append(role_name)

    if skill_lower in missing_lower:
        response = (
            f"{skill.title()} is currently identified as a skill "
            "you should develop based on your CareerPilot analysis."
        )
    elif skill_lower in resume_lower:
        response = (
            f"You already have {skill.title()} detected in your resume. "
            "You can focus on strengthening it through practical projects "
            "and deeper application."
        )
    else:
        response = (
            f"{skill.title()} is a useful skill to consider for your "
            "career development."
        )

    if role_matches:
        response += (
            "\n\nCareer roles where this skill is currently relevant:\n"
            + "\n".join(f"• {role}" for role in role_matches)
        )

    skill_projects = {
        "docker": (
            "Learn images, containers, Dockerfiles and Docker Compose, "
            "then containerize your FastAPI ML application."
        ),
        "fastapi": (
            "Learn API endpoints, request validation and model serving, "
            "then expose one of your ML models through FastAPI."
        ),
        "statistics": (
            "Focus on probability, distributions, hypothesis testing, "
            "correlation and regression, then apply them to a data-analysis project."
        ),
        "power bi": (
            "Learn data modeling, Power Query, DAX and interactive dashboards, "
            "then build a business analytics dashboard."
        ),
        "tableau": (
            "Learn charts, calculated fields, filters and dashboards, "
            "then create an interactive analytics dashboard."
        ),
        "transformers": (
            "Learn attention, transformer architecture and practical NLP usage, "
            "then build a text-classification or question-answering project."
        ),
        "rest api": (
            "Learn HTTP methods, request/response structure and API validation, "
            "then build and test an endpoint for your ML application."
        )
    }

    if skill_lower in skill_projects:
        response += "\n\nRecommended next step:\n" + skill_projects[skill_lower]

    return response


def _roadmap_context_response(roadmap):
    if not roadmap:
        return None

    response = "Based on your current CareerPilot roadmap:\n\n"

    for phase in roadmap:
        if not isinstance(phase, dict):
            continue

        phase_name = phase.get("phase", "Learning Phase")
        duration = phase.get("duration", "")
        skills = phase.get("skills", [])
        goal = phase.get("goal", "")

        response += f"• {phase_name}"

        if duration:
            response += f" ({duration})"

        response += "\n"

        if skills:
            response += (
                "  Skills: "
                + ", ".join(skills)
                + "\n"
            )

        if goal:
            response += f"  Goal: {goal}\n"

        response += "\n"

    return response.strip()


def _top_role_context(career_roles):
    if not career_roles:
        return None

    valid_roles = []

    for role in career_roles:
        if not isinstance(role, dict):
            continue

        name = role.get("role")

        if not name:
            continue

        try:
            percentage = float(
                role.get("match_percentage", 0)
            )
        except (TypeError, ValueError):
            percentage = 0

        valid_roles.append(
            (name, percentage)
        )

    if not valid_roles:
        return None

    top_role = max(
        valid_roles,
        key=lambda item: item[1]
    )

    return (
        f"Your current CareerPilot analysis shows "
        f"{top_role[0]} at {top_role[1]:.1f}% skill match."
    )



# ============================================================
# Main CareerPilot Chat
# ============================================================

def career_chat(
    message,
    resume_skills=None,
    missing_skills=None,
    career_roles=None,
    roadmap=None,
    conversation_history=None
):
    conversation_history = conversation_history or []

    previous_user_message = ""

    previous_assistant_message = ""

    for item in reversed(conversation_history):

        if hasattr(item, "role"):
            role = item.role
            content = item.content
        else:
            role = item.get("role", "")
            content = item.get("content", "")

        if role == "assistant" and not previous_assistant_message:
            previous_assistant_message = content

        elif role == "user" and content != message:
            previous_user_message = content

        if previous_user_message and previous_assistant_message:
            break
    """
    CareerPilot local career assistant.

    This version is rule-based and does not require an external
    LLM or OpenAI API.
    """

    message = _normalize(message)

    resume_skills = resume_skills or []
    missing_skills = missing_skills or []
    career_roles = career_roles or []
    roadmap = roadmap or []

    # --------------------------------------------------------
    # Greeting
    # --------------------------------------------------------

    if _has_any(
        message,
        ["hello", "hi", "hey", "good morning", "good afternoon"]
    ):
        return (
            "Hello! I'm CareerPilot AI.\n\n"
            "I can help you with:\n"
            "• Resume analysis\n"
            "• Skills and skill gaps\n"
            "• Career roles\n"
            "• Learning roadmap\n"
            "• Python, SQL and ML concepts\n"
            "• AI / NLP\n"
            "• Projects\n"
            "• Interview preparation\n"
            "• Deployment\n\n"
            "Ask me a question such as "
            "\"What is a tuple?\" or "
            "\"What skills am I missing?\""
        )

    # --------------------------------------------------------
    # My Skills
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "what skills do i have",
            "what are my skills",
            "my skills",
            "show my skills",
            "resume skills",
            "skills in my resume"
        ]
    ):
        if resume_skills:
            return (
                "Based on your uploaded resume, CareerPilot detected "
                f"{len(set(resume_skills))} skills:\n\n"
                + _format_skills(resume_skills)
            )

        return (
            "I don't have your resume skills yet. "
            "Please upload and analyze your resume first."
        )

    # --------------------------------------------------------
    # Missing Skills
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "missing skills",
            "missing skill",
            "skill gap",
            "skill gaps",
            "what am i missing",
            "what skills am i missing",
            "skills should i develop"
        ]
    ):
        return _missing_skill_response(
            missing_skills,
            career_roles
        )

    # --------------------------------------------------------
    # Why Should I Learn a Skill?
    # --------------------------------------------------------

    why_skill_match = re.search(
        r"(?:why should i learn|why do i need|why learn|why should i study) "
        r"(.+?)(?:\?|$)",
        message
    )

    if why_skill_match:
        skill = why_skill_match.group(1).strip()

        return _why_skill_response(
            skill,
            resume_skills,
            missing_skills,
            career_roles
        )

    # --------------------------------------------------------
    # Technical Questions
    # --------------------------------------------------------

    technical = _technical_answer(message)

    if technical:
        return technical

    # --------------------------------------------------------
    # What Should I Learn Next?
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "what should i learn next",
            "what do i learn next",
            "what should i focus on",
            "what should i study next",
            "next skill",
            "next step"
        ]
    ):
        if roadmap:
            first_phase = roadmap[0]

            if isinstance(first_phase, dict):
                phase_name = first_phase.get(
                    "phase",
                    "your next learning phase"
                )
                phase_skills = first_phase.get(
                    "skills",
                    []
                )
                duration = first_phase.get(
                    "duration",
                    ""
                )

                response = (
                    f"Based on your current CareerPilot roadmap, "
                    f"your next focus should be {phase_name}."
                )

                if phase_skills:
                    response += (
                        "\n\nSkills to focus on:\n• "
                        + "\n• ".join(phase_skills)
                    )

                if duration:
                    response += (
                        f"\n\nSuggested duration: {duration}"
                    )

                return response

        if missing_skills:
            return (
                "Based on your current skill gaps, your next focus "
                "should be:\n\n"
                + _format_skills(missing_skills)
            )

        return (
            "Upload and analyze your resume first so I can "
            "identify your personalized next learning step."
        )

    # --------------------------------------------------------
    # Why This Career Role?
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "why this career",
            "why this role",
            "why this career path",
            "why should i choose",
            "why should i become"
        ]
    ):
        role = _find_role(
            career_roles,
            message
        )

        if role:
            name = role.get("role", "this role")
            percentage = role.get(
                "match_percentage",
                0
            )

            matched = role.get(
                "matched_skills",
                []
            )

            missing = role.get(
                "missing_skills",
                []
            )

            response = (
                f"CareerPilot currently shows {name} at "
                f"{float(percentage):.1f}% skill match."
            )

            if matched:
                response += (
                    "\n\nYour matching skills include:\n• "
                    + "\n• ".join(
                        skill.title()
                        for skill in matched
                    )
                )

            if missing:
                response += (
                    "\n\nThe main skills to develop for this role are:\n• "
                    + "\n• ".join(
                        skill.title()
                        for skill in missing
                    )
                )

            return response

        top_role = _top_role_context(career_roles)

        if top_role:
            return top_role

        return (
            "I need your CareerPilot career analysis to explain "
            "how a specific role relates to your profile."
        )

    # --------------------------------------------------------
    # Career Report / Career Roles
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "career report",
            "career analysis",
            "career roles",
            "what roles",
            "which roles",
            "job roles",
            "what jobs"
        ]
    ):
        return _career_summary(career_roles)

    # --------------------------------------------------------
    # Specific Role
    # --------------------------------------------------------

    role = _find_role(career_roles, message)

    if role:
        name = role.get("role", "this role")
        percentage = role.get("match_percentage", 0)
        matched = role.get("matched_skills", [])
        missing = role.get("missing_skills", [])

        response = f"{name} has a current skill match of {float(percentage):.1f}%."

        if matched:
            response += (
                "\n\nMatching skills:\n• "
                + "\n• ".join(
                    skill.title() for skill in matched
                )
            )

        if missing:
            response += (
                "\n\nSkills to develop:\n• "
                + "\n• ".join(
                    skill.title() for skill in missing
                )
            )

        return response

    # --------------------------------------------------------
    # Career Path
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "career path",
            "career option",
            "career options",
            "career choice",
            "career",
            "job",
            "role"
        ]
    ):
        if career_roles:
            return _career_summary(career_roles)

        return (
            "CareerPilot can analyze roles such as:\n\n"
            "• Data Scientist\n"
            "• Data Analyst\n"
            "• Machine Learning Engineer\n"
            "• AI / NLP Engineer\n\n"
            "Upload your resume to get a personalized career analysis."
        )

    # --------------------------------------------------------
    # Roadmap
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "roadmap",
            "learning roadmap",
            "how should i learn"
        ]
    ):
        roadmap_response = _roadmap_context_response(
            roadmap
        )

        if roadmap_response:
            return roadmap_response

        return (
            "A personalized roadmap requires your resume analysis. "
            "Upload your resume first so CareerPilot can build "
            "the learning sequence from your current skills."
        )

    # --------------------------------------------------------
    # Interview
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "interview",
            "interview preparation",
            "prepare for interview",
            "interview questions",
            "technical interview"
        ]
    ):
        return (
            "CareerPilot can help you prepare for interviews using:\n\n"
            "• Technical questions\n"
            "• Project questions\n"
            "• Missing-skill questions\n"
            "• Behavioral questions\n"
            "• Answer evaluation\n\n"
            "You can generate interview questions from your resume "
            "and practice your answers."
        )

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "project",
            "projects",
            "project idea",
            "project ideas"
        ]
    ):
        return (
            "For a strong fresher portfolio, build projects that "
            "demonstrate an end-to-end workflow.\n\n"
            "For your current profile, useful project types include:\n"
            "• End-to-end machine-learning project\n"
            "• NLP application\n"
            "• AI career assistant\n"
            "• Data analytics dashboard\n"
            "• ML model deployed with FastAPI and Docker\n\n"
            "Each project should explain the problem, data, approach, "
            "technologies, evaluation and final result."
        )

    # --------------------------------------------------------
    # Deployment
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "deploy",
            "deployment",
            "deploy model",
            "deploy ml model",
            "rest api"
        ]
    ):
        return (
            "For ML deployment, focus on this workflow:\n\n"
            "1. Train and save the model\n"
            "2. Create a FastAPI endpoint\n"
            "3. Validate requests with Pydantic\n"
            "4. Load the model inside the API\n"
            "5. Test the endpoint\n"
            "6. Create a Dockerfile\n"
            "7. Build and run the container\n\n"
            "Your current CareerPilot project is already using "
            "FastAPI, so this is a useful next area to strengthen."
        )

    # --------------------------------------------------------
    # Resume
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "resume",
            "cv",
            "my resume"
        ]
    ):
        return (
            "CareerPilot can analyze your resume and extract "
            "technical skills. It can then compare those skills "
            "with career roles, identify skill gaps and generate "
            "a personalized learning roadmap."
        )

    # --------------------------------------------------------
    # Help
    # --------------------------------------------------------

    if _has_any(
        message,
        [
            "help",
            "what can you do",
            "how can you help"
        ]
    ):
        return (
            "I can help you with:\n\n"
            "Career:\n"
            "• Career analysis\n"
            "• Role comparison\n"
            "• Skill gaps\n"
            "• Learning roadmap\n\n"
            "Technical:\n"
            "• Python\n"
            "• SQL\n"
            "• Machine Learning\n"
            "• Deep Learning\n"
            "• NLP\n"
            "• Pandas / NumPy\n"
            "• APIs / FastAPI\n"
            "• Docker\n"
            "• Git\n\n"
            "Interview:\n"
            "• Technical questions\n"
            "• Project questions\n"
            "• Behavioral questions\n"
            "• Answer practice"
        )

    # --------------------------------------------------------
    # Default
    # --------------------------------------------------------

    return (
        "I can help with career development and technical questions.\n\n"
        "Try asking:\n"
        "• What is a tuple?\n"
        "• What is machine learning?\n"
        "• What skills do I have?\n"
        "• What skills am I missing?\n"
        "• What career roles fit me?\n"
        "• What should I learn next?\n"
        "• Help me prepare for an interview.\n"
        "• Give me project ideas."
    )
