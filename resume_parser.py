from pypdf import PdfReader
from docx import Document
import re


def extract_pdf_text(file):
    reader = PdfReader(file)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_docx_text(file):
    document = Document(file)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_resume_text(file):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file)

    elif filename.endswith(".docx"):
        return extract_docx_text(file)

    else:
        raise ValueError(
            "Only PDF and DOCX files are supported."
        )


def analyze_resume_structure(text):

    result = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "experience": [],
        "projects": [],
        "skills": [],
        "positions_of_responsibility": [],
        "achievements": [],
        "languages": []
    }

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # -------------------------------------------------
    # PROFILE
    # -------------------------------------------------

    if lines:
        result["name"] = lines[0]

    email_match = re.search(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        text
    )

    if email_match:
        result["email"] = email_match.group(0)

    phone_match = re.search(
        r"(?:\+91[\s-]?)?\d{10}",
        text
    )

    if phone_match:
        result["phone"] = phone_match.group(0)

    # -------------------------------------------------
    # SECTION DETECTION
    # -------------------------------------------------

    section_names = {
        "education": "education",
        "technical skills": "technical skills",
        "ai / ml projects": "projects",
        "projects": "projects",
        "experience": "experience",
        "positions of responsibility":
            "positions_of_responsibility",
        "achievements": "achievements",
        "languages": "languages"
    }

    sections = {}
    current_section = None

    for line in lines:

        normalized = line.lower().strip()

        if normalized in section_names:

            current_section = section_names[normalized]
            sections[current_section] = []

            continue

        if current_section:
            sections[current_section].append(line)

    # -------------------------------------------------
    # EDUCATION
    # -------------------------------------------------

    education_lines = sections.get(
        "education",
        []
    )

    current_education = None

    for line in education_lines:

        year_match = re.search(
            r"(20\d{2})\s*[–-]\s*(20\d{2})",
            line
        )

        if year_match:

            if current_education:
                result["education"].append(
                    current_education
                )

            current_education = {
                "institution": line,
                "degree": "",
                "year": (
                    f"{year_match.group(1)} - "
                    f"{year_match.group(2)}"
                ),
                "details": ""
            }

        elif current_education:

            if not current_education["degree"]:
                current_education["degree"] = line

            else:
                current_education["details"] += (
                    " " + line
                )

    if current_education:
        result["education"].append(
            current_education
        )

    # -------------------------------------------------
    # PROJECTS
    # -------------------------------------------------

    project_lines = sections.get(
        "projects",
        []
    )

    current_project = None

    for line in project_lines:

        if not line.startswith(
            ("•", "-", "*")
        ):

            if current_project:
                result["projects"].append(
                    current_project
                )

            project_name = line
            technologies = []

            if "Python" in line:
                technologies.append("Python")

            if "Machine Learning" in line:
                technologies.append(
                    "Machine Learning"
                )

            if "NLP" in line:
                technologies.append("NLP")

            current_project = {
                "name": project_name,
                "technologies": technologies,
                "description": []
            }

        elif current_project:

            description = line.lstrip(
                "•-* "
            ).strip()

            if description:
                current_project[
                    "description"
                ].append(description)

    if current_project:
        result["projects"].append(
            current_project
        )

    # -------------------------------------------------
    # EXPERIENCE
    # -------------------------------------------------

    experience_lines = sections.get(
        "experience",
        []
    )

    current_experience = None

    for line in experience_lines:

        if not line.startswith(
            ("•", "-", "*")
        ):

            if current_experience:
                result["experience"].append(
                    current_experience
                )

            current_experience = {
                "organization": line,
                "role": "",
                "description": []
            }

        elif current_experience:

            description = line.lstrip(
                "•-* "
            ).strip()

            if description:
                current_experience[
                    "description"
                ].append(description)

    if current_experience:
        result["experience"].append(
            current_experience
        )

    # -------------------------------------------------
    # TECHNICAL SKILLS
    # -------------------------------------------------

    skill_lines = sections.get(
        "technical skills",
        []
    )

    for line in skill_lines:

        clean_line = line.lstrip(
            "•-* "
        ).strip()

        if ":" in clean_line:

            category, skills_text = (
                clean_line.split(":", 1)
            )

            skills = [
                skill.strip()
                for skill in skills_text.split(",")
                if skill.strip()
            ]

            result["skills"].append(
                {
                    "category": category.strip(),
                    "skills": skills
                }
            )

        elif clean_line:

            result["skills"].append(
                {
                    "category": "Other",
                    "skills": [clean_line]
                }
            )

    # -------------------------------------------------
    # POSITIONS OF RESPONSIBILITY
    # -------------------------------------------------

    por_lines = sections.get(
        "positions_of_responsibility",
        []
    )

    current_por = None

    for line in por_lines:

        if not line.startswith(
            ("•", "-", "*")
        ):

            if current_por:
                result[
                    "positions_of_responsibility"
                ].append(current_por)

            current_por = {
                "organization": line,
                "role": "",
                "description": []
            }

        elif current_por:

            description = line.lstrip(
                "•-* "
            ).strip()

            if description:
                current_por[
                    "description"
                ].append(description)

    if current_por:
        result[
            "positions_of_responsibility"
        ].append(current_por)

    # -------------------------------------------------
    # ACHIEVEMENTS
    # -------------------------------------------------

    for line in sections.get(
        "achievements",
        []
    ):

        achievement = line.lstrip(
            "•-* "
        ).strip()

        if achievement:
            result["achievements"].append(
                achievement
            )

    # -------------------------------------------------
    # LANGUAGES
    # -------------------------------------------------

    language_lines = sections.get(
        "languages",
        []
    )

    for line in language_lines:

        clean_line = line.lstrip(
            "•-* "
        ).strip()

        if clean_line:

            result["languages"].extend(
                [
                    language.strip()
                    for language in clean_line.split(",")
                    if language.strip()
                ]
            )

    return result