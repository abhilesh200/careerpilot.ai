SKILL_RECOMMENDATIONS = {

    "python": {
        "why": "Python is widely used for data analysis, machine learning and AI development.",
        "learn": [
            "Python fundamentals",
            "Functions and OOP",
            "NumPy and Pandas",
            "File handling and APIs"
        ],
        "project": "Build an end-to-end data analysis project using Python and Pandas."
    },

    "sql": {
        "why": "SQL is essential for working with structured data and databases.",
        "learn": [
            "SELECT and WHERE",
            "JOINs",
            "GROUP BY",
            "Subqueries",
            "Window functions"
        ],
        "project": "Build a SQL-based business analytics project."
    },

    "machine learning": {
        "why": "Machine learning is a core skill for building predictive models.",
        "learn": [
            "Regression",
            "Classification",
            "Feature engineering",
            "Model evaluation",
            "Cross-validation"
        ],
        "project": "Build an end-to-end customer churn prediction system."
    },

    "deep learning": {
        "why": "Deep learning is useful for complex AI problems involving images, text and large datasets.",
        "learn": [
            "Neural networks",
            "Backpropagation",
            "CNN",
            "RNN",
            "Transformers"
        ],
        "project": "Build an image classification or text classification project."
    },

    "natural language processing": {
        "why": "NLP enables applications to understand and process human language.",
        "learn": [
            "Text preprocessing",
            "Tokenization",
            "Embeddings",
            "Text classification",
            "Transformers"
        ],
        "project": "Build a resume or sentiment analysis system."
    },

    "nlp": {
        "why": "NLP enables applications to understand and process human language.",
        "learn": [
            "Text preprocessing",
            "Embeddings",
            "Text classification",
            "Transformers"
        ],
        "project": "Build an NLP-based text classification project."
    },

    "pandas": {
        "why": "Pandas is one of the main tools for data manipulation and analysis in Python.",
        "learn": [
            "DataFrames",
            "Filtering",
            "GroupBy",
            "Merging",
            "Data cleaning"
        ],
        "project": "Build an exploratory data analysis project."
    },

    "numpy": {
        "why": "NumPy provides the numerical computing foundation for the Python data ecosystem.",
        "learn": [
            "Arrays",
            "Indexing",
            "Vectorization",
            "Linear algebra"
        ],
        "project": "Implement basic machine learning calculations using NumPy."
    },

    "power bi": {
        "why": "Power BI is widely used for interactive business intelligence and reporting.",
        "learn": [
            "Data modeling",
            "Power Query",
            "DAX",
            "Interactive dashboards"
        ],
        "project": "Build an executive sales performance dashboard."
    },

    "tableau": {
        "why": "Tableau is a popular business intelligence and data visualization platform.",
        "learn": [
            "Charts",
            "Calculated fields",
            "Filters",
            "Dashboards"
        ],
        "project": "Build an interactive business analytics dashboard."
    },

    "docker": {
        "why": "Docker helps package applications and their dependencies consistently.",
        "learn": [
            "Images",
            "Containers",
            "Dockerfile",
            "Docker Compose"
        ],
        "project": "Containerize a machine learning API."
    },

    "git": {
        "why": "Git is essential for version control and collaborative software development.",
        "learn": [
            "Repositories",
            "Branches",
            "Commits",
            "Merge",
            "Pull requests"
        ],
        "project": "Manage an end-to-end ML project using Git and GitHub."
    },

    "scikit-learn": {
        "why": "Scikit-learn provides practical tools for classical machine learning.",
        "learn": [
            "Preprocessing",
            "Pipelines",
            "Classification",
            "Regression",
            "Model evaluation"
        ],
        "project": "Build a complete classification pipeline."
    },

    "statistics": {
        "why": "Statistics helps you understand data and evaluate machine learning results.",
        "learn": [
            "Probability",
            "Distributions",
            "Hypothesis testing",
            "Correlation",
            "Regression"
        ],
        "project": "Perform statistical analysis on a real-world dataset."
    },

    "fastapi": {
        "why": "FastAPI can be used to expose machine learning models through APIs.",
        "learn": [
            "API basics",
            "GET and POST",
            "Request validation",
            "Model serving"
        ],
        "project": "Deploy a machine learning model through a FastAPI API."
    },

    "streamlit": {
        "why": "Streamlit allows data science and machine learning applications to be turned into interactive web apps quickly.",
        "learn": [
            "Widgets",
            "Layouts",
            "Session state",
            "Deployment"
        ],
        "project": "Build and deploy an interactive ML dashboard."
    }
}


def get_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        if skill in SKILL_RECOMMENDATIONS:

            recommendations.append({
                "skill": skill,
                "why": SKILL_RECOMMENDATIONS[skill]["why"],
                "learn": SKILL_RECOMMENDATIONS[skill]["learn"],
                "project": SKILL_RECOMMENDATIONS[skill]["project"]
            })

            

    return recommendations
CAREER_ROLES = {

    "Data Scientist": {
        "skills": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "machine learning",
            "scikit-learn",
            "statistics"
        ]
    },

    "Data Analyst": {
        "skills": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "power bi",
            "tableau",
            "statistics"
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "python",
            "machine learning",
            "scikit-learn",
            "tensorflow",
            "docker",
            "fastapi",
            "git"
        ]
    },

    "AI / NLP Engineer": {
        "skills": [
            "python",
            "machine learning",
            "deep learning",
            "natural language processing",
            "tensorflow",
            "git"
        ]
    }
}

def build_career_roadmap(missing_skills):

    roadmap = []

    for skill in missing_skills:

        if skill in SKILL_RECOMMENDATIONS:
            roadmap.append({
                "skill": skill,
                "why": SKILL_RECOMMENDATIONS[skill]["why"],
                "learn": SKILL_RECOMMENDATIONS[skill]["learn"],
                "project": SKILL_RECOMMENDATIONS[skill]["project"]
            })
        else:
            roadmap.append({
                "skill": skill,
                "why": f"Learning {skill} can strengthen your preparation for this career role.",
                "learn": [
                    f"Learn {skill} fundamentals",
                    f"Practice {skill} with real-world examples",
                    f"Build a project using {skill}"
                ],
                "project": f"Build a practical project using {skill}."
            })

    return roadmap


def recommend_career_roles(resume_skills):

    SKILL_ALIASES = {
        "nlp": "natural language processing",
        "sklearn": "scikit-learn",
        "scikit learn": "scikit-learn",
        "ml": "machine learning",
        "dl": "deep learning"
    }

    normalized_skills = set()

    for skill in resume_skills:
        skill = skill.lower().strip()
        normalized_skills.add(
            SKILL_ALIASES.get(skill, skill)
        )

    recommendations = []

    for role, data in CAREER_ROLES.items():

        required_skills = set(data["skills"])

        matched_skills = sorted(
            normalized_skills.intersection(
                required_skills
            )
        )

        missing_skills = sorted(
            required_skills.difference(
                normalized_skills
            )
        )

        total_skills = len(required_skills)

        if total_skills > 0:
            match_percentage = round(
                (
                    len(matched_skills)
                    / total_skills
                ) * 100,
                2
            )
        else:
            match_percentage = 0

        roadmap = build_career_roadmap(
            missing_skills
        )

        recommendations.append({
            "role": role,
            "match_percentage": match_percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "roadmap": roadmap
        })

    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )
    return recommendations
def generate_career_report(resume_skills):

    recommendations = recommend_career_roles(
        resume_skills
    )

    if not recommendations:
        return {
            "profile": "No career profile could be generated.",
            "top_role": None,
            "recommendations": [],
            "total_roles_analyzed": 0
        }

    top_role = recommendations[0]

    all_missing_skills = set()

    for recommendation in recommendations:
        for skill in recommendation["missing_skills"]:
            all_missing_skills.add(skill)

    return {
        "profile": (
            "Your profile shows skills across "
            "programming, data analysis and AI/ML."
        ),

        "top_role": {
            "role": top_role["role"],
            "match_percentage": top_role["match_percentage"]
        },

        "recommendations": recommendations,

        "skills_to_develop": sorted(
            all_missing_skills
        ),

        "total_roles_analyzed": len(
            recommendations
        )
    } 
def generate_career_roadmap(resume_skills):
    skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    roadmap = []

    # --------------------------------------------------
    # Phase 1 — Fundamentals
    # --------------------------------------------------

    phase_1_skills = [
        skill for skill in [
            "Statistics",
            "Data Analysis"
        ]
        if skill.lower() not in skills
    ]

    if phase_1_skills:
        roadmap.append({
            "phase": "Phase 1 — Strengthen Fundamentals",
            "duration": "2–3 weeks",
            "skills": phase_1_skills,
            "goal": (
                "Build stronger foundations in statistics "
                "and data analysis."
            ),
            "project": (
                "Build a statistical data analysis project "
                "using Python and Pandas."
            ),
            "outcome": (
                "You will be able to analyze datasets, "
                "interpret statistics and support ML decisions."
            )
        })


    # --------------------------------------------------
    # Phase 2 — Machine Learning
    # --------------------------------------------------

    phase_2_skills = [
        skill for skill in [
            "Scikit-learn",
            "Feature Engineering",
            "Model Evaluation"
        ]
        if skill.lower() not in skills
    ]

    if phase_2_skills:
        roadmap.append({
            "phase": "Phase 2 — Machine Learning",
            "duration": "3–4 weeks",
            "skills": phase_2_skills,
            "goal": (
                "Develop practical machine-learning "
                "model-building and evaluation skills."
            ),
            "project": (
                "Build an end-to-end machine-learning "
                "project with feature engineering and "
                "model evaluation."
            ),
            "outcome": (
                "You will be able to build, evaluate and "
                "improve practical ML models."
            )
        })


    # --------------------------------------------------
    # Phase 3 — AI / NLP
    # --------------------------------------------------

    phase_3_skills = [
        skill for skill in [
            "Deep Learning",
            "Natural Language Processing",
            "LLM",
            "Transformers"
        ]
        if skill.lower() not in skills
    ]

    if phase_3_skills:
        roadmap.append({
            "phase": "Phase 3 — AI / NLP",
            "duration": "3–4 weeks",
            "skills": phase_3_skills,
            "goal": (
                "Build practical skills in modern AI, "
                "NLP and language models."
            ),
            "project": (
                "Build an NLP application such as a "
                "text-classification or document "
                "question-answering system."
            ),
            "outcome": (
                "You will be able to build practical "
                "AI/NLP applications using modern techniques."
            )
        })


    # --------------------------------------------------
    # Phase 4 — Deployment
    # --------------------------------------------------

    phase_4_skills = [
        skill for skill in [
            "FastAPI",
            "Docker",
            "REST API"
        ]
        if skill.lower() not in skills
    ]

    if phase_4_skills:
        roadmap.append({
            "phase": "Phase 4 — Deployment",
            "duration": "2–3 weeks",
            "skills": phase_4_skills,
            "goal": (
                "Learn how to turn ML and AI projects "
                "into deployable applications."
            ),
            "project": (
                "Deploy a machine-learning model using "
                "FastAPI and Docker."
            ),
            "outcome": (
                "You will be able to expose ML models "
                "through APIs and package applications "
                "for deployment."
            )
        })


    return roadmap
def generate_interview_questions(resume_skills, job_description=""):
    """
    Generate interview questions based on resume skills
    and the target job description.
    """

    skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    questions = {
        "technical": [],
        "project": [],
        "missing_skills": [],
        "behavioral": []
    }

    # --------------------------------------------------
    # Technical Questions
    # --------------------------------------------------

    if "python" in skills:
        questions["technical"].append(
            "Explain the difference between a list, tuple and set in Python."
        )

    if "sql" in skills:
        questions["technical"].append(
            "Explain the difference between INNER JOIN and LEFT JOIN in SQL."
        )

    if "machine learning" in skills:
        questions["technical"].append(
            "What is machine learning and how does supervised learning work?"
        )

    if "deep learning" in skills:
        questions["technical"].append(
            "What is deep learning and how is it different from traditional machine learning?"
        )

    if "natural language processing" in skills:
        questions["technical"].append(
            "What is Natural Language Processing and where is it used?"
        )

    if "tensorflow" in skills:
        questions["technical"].append(
            "What is TensorFlow and why would you use it for deep learning?"
        )

    if "scikit-learn" in skills:
        questions["technical"].append(
            "How do you evaluate a machine-learning model using Scikit-learn?"
        )

    if "pandas" in skills:
        questions["technical"].append(
            "How do you use Pandas for data analysis?"
        )

    if "statistics" in skills:
        questions["technical"].append(
            "What is the difference between correlation and causation?"
        )


    # --------------------------------------------------
    # Project Questions
    # --------------------------------------------------

    questions["project"] = [
        "Explain your most important technical project.",
        "What problem were you trying to solve?",
        "Why did you choose your particular approach?",
        "What challenges did you face during the project?",
        "How did you evaluate the performance of your solution?",
        "What would you improve if you rebuilt the project?"
    ]


    # --------------------------------------------------
    # Missing Skill Questions
    # --------------------------------------------------

    job_text = job_description.lower()

    possible_skills = [
        "python",
        "sql",
        "java",
        "c++",
        "docker",
        "fastapi",
        "power bi",
        "tableau",
        "statistics",
        "machine learning",
        "deep learning"
    ]

    for skill in possible_skills:

        if skill in job_text and skill not in skills:

            questions["missing_skills"].append(
                f"What is your current experience with {skill.title()}?"
            )


    # --------------------------------------------------
    # Behavioral Questions
    # --------------------------------------------------

    questions["behavioral"] = [
        "Tell me about yourself.",
        "Walk me through your resume.",
        "Why are you interested in this role?",
        "Describe a challenging project you worked on.",
        "Tell me about a problem you solved using data or technology.",
        "What are your strengths as a candidate?",
        "What technical skill are you currently improving?",
        "Where do you see yourself in the next few years?"
    ]


    return questions