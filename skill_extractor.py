import re


SKILL_ALIASES = {
    "py": "python",
    "python3": "python",
    "postgres": "postgresql",
    "postgre": "postgresql",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "powerbi": "power bi",
    "power-bi": "power bi",
    "nlp": "natural language processing",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "gen ai": "generative ai",
    "genai": "generative ai",
    "llms": "llm",
}


SKILLS = [
    "python", "sql", "r", "java", "c++",
    "machine learning", "deep learning", "artificial intelligence",
    "data science", "data analysis", "data analytics", "data visualization",
    "natural language processing", "nlp", "computer vision",
    "statistics", "probability", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "keras", "matplotlib", "seaborn",
    "power bi", "tableau", "excel", "aws", "azure", "gcp", "docker",
    "git", "github", "fastapi", "flask", "streamlit", "llm",
    "generative ai", "prompt engineering", "langchain", "rag",
    "mongodb", "mysql", "postgresql", "rest api", "api",
    "feature engineering", "model evaluation", "cross-validation",
    "classification", "regression", "time series", "eda",
    "exploratory data analysis", "neural networks", "lstm", "transformers",
]


def normalize_text(text):
    text = str(text).lower()
    text = text.replace("power-bi", "power bi")
    text = text.replace("powerbi", "power bi")
    text = text.replace("scikit learn", "scikit-learn")
    text = text.replace("natural-language processing", "natural language processing")
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text):
    text = normalize_text(text)
    found_skills = set()

    for skill in SKILLS:
        canonical_skill = SKILL_ALIASES.get(skill, skill)

        if skill == "c++":
            pattern = r"(?<!\w)c\+\+(?!\w)"
        elif skill == "r":
            pattern = r"(?<![a-z])r(?![a-z])"
        else:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.add(canonical_skill)

    for alias, canonical_skill in SKILL_ALIASES.items():
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        if re.search(pattern, text):
            found_skills.add(canonical_skill)

    return sorted(found_skills)
