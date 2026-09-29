import uuid
import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

import career_engine

from skill_extractor import extract_skills

from career_recommender import (
    recommend_career_roles,
    generate_career_report,
    generate_career_roadmap,
    generate_interview_questions
)

from resume_parser import (
    extract_resume_text,
    analyze_resume_structure
)

from llm_service import generate_ai_response

from database import (
    create_user,
    get_user_by_email,
    hash_password,
    verify_password,
    save_career_profile,
    get_career_profile,
    save_chat_message,
    get_chat_history,
    clear_chat_history
)
from fastapi import FastAPI
from database import create_tables

app = FastAPI(
    title="CareerPilot API",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    create_tables()


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="CareerPilot AI API",
    description=(
        "AI-powered career intelligence API for "
        "resume analysis, skill matching, career planning "
        "and interview preparation."
    ),
    version="1.0.0"
)


# =========================================================
# DATA MODELS
# =========================================================


class Message(BaseModel):

    role: str = Field(
        ...,
        description="system, user or assistant"
    )

    content: str


class ChatCompletionRequest(BaseModel):

    user_id: int

    model: str = "careerpilot"

    messages: List[Message]

    resume_skills: List[str] = Field(
        default_factory=list
    )

    missing_skills: List[str] = Field(
        default_factory=list
    )

    career_roles: List[dict] = Field(
        default_factory=list
    )

    roadmap: List[dict] = Field(
        default_factory=list
    )

    temperature: float = 0.7

    max_tokens: Optional[int] = 1000


class ChatMessageRequest(BaseModel):

    user_id: int

    role: str

    content: str


class CareerAnalysisRequest(BaseModel):

    resume_text: str

    job_description: str


class SkillExtractionRequest(BaseModel):

    text: str


class CareerRecommendationRequest(BaseModel):

    resume_skills: List[str]


class InterviewQuestionsRequest(BaseModel):

    resume_skills: List[str]

    job_description: str = ""


class InterviewAnswerRequest(BaseModel):

    question: str

    answer: str

    resume_skills: List[str] = Field(
        default_factory=list
    )


class RegisterRequest(BaseModel):

    name: str

    email: str

    password: str


class LoginRequest(BaseModel):

    email: str

    password: str


class CareerProfileRequest(BaseModel):

    user_id: int

    resume_skills: List[str] = Field(
        default_factory=list
    )

    missing_skills: List[str] = Field(
        default_factory=list
    )

    career_roles: List[dict] = Field(
        default_factory=list
    )

    roadmap: List[dict] = Field(
        default_factory=list
    )

    resume_text: str = ""


# =========================================================
# HEALTH CHECK
# =========================================================


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "CareerPilot AI",
        "version": "1.0.0"
    }


# =========================================================
# ROOT
# =========================================================


@app.get("/")
def root():

    return {
        "name": "CareerPilot AI",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "models": "/v1/models",
        "chat": "/v1/chat/completions"
    }


# =========================================================
# MODELS ENDPOINT
# =========================================================


@app.get("/v1/models")
def list_models():

    return {
        "object": "list",

        "data": [
            {
                "id": "careerpilot",
                "object": "model",
                "owned_by": "careerpilot"
            }
        ]
    }


# =========================================================
# AUTHENTICATION
# =========================================================


@app.post("/v1/auth/register")
def register_user(
    request: RegisterRequest
):

    try:

        name = request.name.strip()

        email = request.email.strip().lower()

        password = request.password

        if not name:

            raise HTTPException(
                status_code=400,
                detail="Name cannot be empty."
            )

        if not email:

            raise HTTPException(
                status_code=400,
                detail="Email cannot be empty."
            )

        if len(password) < 6:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Password must contain "
                    "at least 6 characters."
                )
            )

        existing_user = get_user_by_email(email)

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Email already registered."
            )

        password_hash = hash_password(password)

        user_id = create_user(
            name,
            email,
            password_hash
        )

        return {
            "message": "User registered successfully.",
            "user_id": user_id,
            "name": name,
            "email": email
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# LOGIN
# =========================================================


@app.post("/v1/auth/login")
def login_user(
    request: LoginRequest
):

    try:

        email = request.email.strip().lower()

        password = request.password

        user = get_user_by_email(email)

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        if not verify_password(
            password,
            user["password_hash"]
        ):

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        return {
            "message": "Login successful.",
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# SKILL EXTRACTION
# =========================================================


@app.post("/v1/skills/extract")
def extract_skills_api(
    request: SkillExtractionRequest
):

    try:

        skills = extract_skills(
            request.text
        )

        return {
            "object": "skills.extraction",
            "status": "success",

            "data": {
                "skills": skills,
                "count": len(skills)
            }
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# OPENAI-COMPATIBLE CHAT COMPLETIONS
# =========================================================


@app.post("/v1/chat/completions")
def chat_completions(
    request: ChatCompletionRequest
):

    try:

        if not request.user_id:

            raise HTTPException(
                status_code=400,
                detail="user_id is required."
            )

        if not request.messages:

            raise HTTPException(
                status_code=400,
                detail="Messages cannot be empty."
            )

        # -----------------------------------------
        # Find Latest User Message
        # -----------------------------------------

        user_message = ""

        for message in reversed(
            request.messages
        ):

            if message.role == "user":

                user_message = message.content

                break

        if not user_message:

            raise HTTPException(
                status_code=400,
                detail="No user message found."
            )

        # -----------------------------------------
        # Save User Message
        # -----------------------------------------

        save_chat_message(
            user_id=request.user_id,
            role="user",
            content=user_message
        )

        # -----------------------------------------
        # Generate AI Response
        # -----------------------------------------

        answer = generate_ai_response(

            message=user_message,

            resume_skills=request.resume_skills,

            missing_skills=request.missing_skills,

            career_roles=request.career_roles,

            roadmap=request.roadmap,

            conversation_history=request.messages
        )

        # -----------------------------------------
        # Save Assistant Message
        # -----------------------------------------

        save_chat_message(
            user_id=request.user_id,
            role="assistant",
            content=answer
        )

        # -----------------------------------------
        # OpenAI-Compatible Response
        # -----------------------------------------

        return {

            "id": (
                f"chatcmpl-"
                f"{uuid.uuid4().hex}"
            ),

            "object": "chat.completion",

            "created": int(time.time()),

            "model": request.model,

            "choices": [

                {
                    "index": 0,

                    "message": {
                        "role": "assistant",
                        "content": answer
                    },

                    "finish_reason": "stop"
                }

            ]
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CHAT HISTORY
# =========================================================


@app.get("/v1/chat/history/{user_id}")
def chat_history(
    user_id: int
):

    try:

        messages = get_chat_history(
            user_id
        )

        return {

            "user_id": user_id,

            "messages": [

                {
                    "id": message["id"],
                    "role": message["role"],
                    "content": message["content"],
                    "created_at": message["created_at"]
                }

                for message in messages
            ]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CLEAR CHAT HISTORY
# =========================================================


@app.delete("/v1/chat/history/{user_id}")
def delete_chat_history(
    user_id: int
):

    try:

        clear_chat_history(
            user_id
        )

        return {

            "message":
                "Chat history cleared successfully.",

            "user_id": user_id
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# SAVE CHAT MESSAGE
# =========================================================


@app.post("/v1/chat/message")
def save_message(
    request: ChatMessageRequest
):

    try:

        if not request.content.strip():

            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        message_id = save_chat_message(

            user_id=request.user_id,

            role=request.role,

            content=request.content
        )

        return {

            "message":
                "Chat message saved successfully.",

            "message_id": message_id,

            "user_id": request.user_id
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CAREER ANALYSIS
# =========================================================


@app.post("/v1/career/analyze")
def career_analysis(
    request: CareerAnalysisRequest
):

    try:

        result = career_engine.analyze_career(

            resume_text=request.resume_text,

            job_description=request.job_description
        )

        return {

            "object": "career.analysis",

            "status": "success",

            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# RESUME ANALYSIS
# =========================================================


@app.post("/v1/resume/analyze")
async def resume_analysis(
    file: UploadFile = File(...)
):

    try:

        filename = file.filename or ""

        if not filename.lower().endswith(
            (".pdf", ".docx")
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only PDF and DOCX files "
                    "are supported."
                )
            )

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        from io import BytesIO

        file_object = BytesIO(
            file_content
        )

        file_object.name = filename

        # Extract resume text

        resume_text = extract_resume_text(
            file_object
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text "
                    "from resume."
                )
            )

        # Extract skills

        skills = extract_skills(
            resume_text
        )

        # Analyze resume structure

        structured_data = (
            analyze_resume_structure(
                resume_text
            )
        )

        return {

            "object": "resume.analysis",

            "status": "success",

            "data": {

                "filename": filename,

                "text": resume_text,

                "profile": {
                    "name":
                        structured_data.get(
                            "name",
                            ""
                        ),

                    "email":
                        structured_data.get(
                            "email",
                            ""
                        ),

                    "phone":
                        structured_data.get(
                            "phone",
                            ""
                        )
                },

                "education":
                    structured_data.get(
                        "education",
                        []
                    ),

                "experience":
                    structured_data.get(
                        "experience",
                        []
                    ),

                "projects":
                    structured_data.get(
                        "projects",
                        []
                    ),

                "skills": skills,

                "skill_count":
                    len(skills),

                "positions_of_responsibility":
                    structured_data.get(
                        "positions_of_responsibility",
                        []
                    ),

                "achievements":
                    structured_data.get(
                        "achievements",
                        []
                    ),

                "languages":
                    structured_data.get(
                        "languages",
                        []
                    )
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CAREER RECOMMENDATIONS
# =========================================================


@app.post("/v1/career/recommend")
def career_recommend(
    request: CareerRecommendationRequest
):

    try:

        recommendations = (
            recommend_career_roles(
                request.resume_skills
            )
        )

        return {

            "object":
                "career.recommendations",

            "status": "success",

            "data": {

                "recommendations":
                    recommendations
            }
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# RESUME CAREER RECOMMENDATIONS
# =========================================================


@app.post("/v1/resume/career-recommend")
async def resume_career_recommend(
    file: UploadFile = File(...)
):

    try:

        filename = file.filename or ""

        if not filename.lower().endswith(
            (".pdf", ".docx")
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only PDF and DOCX files "
                    "are supported."
                )
            )

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        from io import BytesIO

        file_object = BytesIO(
            file_content
        )

        file_object.name = filename

        resume_text = extract_resume_text(
            file_object
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text "
                    "from resume."
                )
            )

        skills = extract_skills(
            resume_text
        )

        recommendations = (
            recommend_career_roles(
                skills
            )
        )

        return {

            "object":
                "resume.career.recommendations",

            "status": "success",

            "data": {

                "filename": filename,

                "skills": skills,

                "skill_count":
                    len(skills),

                "recommendations":
                    recommendations
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CAREER REPORT
# =========================================================


@app.post("/v1/career/report")
def career_report(
    request: CareerRecommendationRequest
):

    try:

        report = generate_career_report(
            request.resume_skills
        )

        return {

            "object":
                "career.report",

            "status": "success",

            "data": report
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# RESUME CAREER REPORT
# =========================================================


@app.post("/v1/resume/career-report")
async def resume_career_report(
    file: UploadFile = File(...)
):

    try:

        filename = file.filename or ""

        if not filename.lower().endswith(
            (".pdf", ".docx")
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only PDF and DOCX files "
                    "are supported."
                )
            )

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        from io import BytesIO

        file_object = BytesIO(
            file_content
        )

        file_object.name = filename

        resume_text = extract_resume_text(
            file_object
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text "
                    "from resume."
                )
            )

        skills = extract_skills(
            resume_text
        )

        report = generate_career_report(
            skills
        )

        return {

            "object":
                "resume.career.report",

            "status": "success",

            "data": {

                "filename": filename,

                "skills": skills,

                "skill_count":
                    len(skills),

                "profile":
                    report.get(
                        "profile",
                        {}
                    ),

                "top_role":
                    report.get(
                        "top_role",
                        ""
                    ),

                "recommendations":
                    report.get(
                        "recommendations",
                        []
                    ),

                "skills_to_develop":
                    report.get(
                        "skills_to_develop",
                        []
                    ),

                "total_roles_analyzed":
                    report.get(
                        "total_roles_analyzed",
                        0
                    )
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CAREER ROADMAP
# =========================================================


@app.post("/v1/career/roadmap")
def career_roadmap(
    request: CareerRecommendationRequest
):

    try:

        roadmap = generate_career_roadmap(
            request.resume_skills
        )

        return {

            "object":
                "career.roadmap",

            "status": "success",

            "data": {

                "roadmap": roadmap
            }
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# INTERVIEW QUESTIONS
# =========================================================


@app.post("/v1/interview/questions")
def interview_questions(
    request: InterviewQuestionsRequest
):

    try:

        questions = (
            generate_interview_questions(

                resume_skills=
                    request.resume_skills,

                job_description=
                    request.job_description
            )
        )

        return {

            "object":
                "interview.questions",

            "status": "success",

            "data": {

                "questions": questions
            }
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# INTERVIEW ANSWER EVALUATION
# =========================================================


@app.post("/v1/interview/evaluate")
def evaluate_interview_answer(
    request: InterviewAnswerRequest
):

    try:

        answer = request.answer.strip()

        question = request.question.strip()

        if not answer:

            raise HTTPException(
                status_code=400,
                detail="Answer cannot be empty."
            )

        if not question:

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        answer_lower = answer.lower()

        # -----------------------------------------
        # Resume Skills
        # -----------------------------------------

        resume_skills = {

            skill.lower().strip()

            for skill in request.resume_skills

            if skill.strip()
        }

        mentioned_skills = []

        missing_skills = []

        for skill in resume_skills:

            if skill in answer_lower:

                mentioned_skills.append(
                    skill
                )

            else:

                missing_skills.append(
                    skill
                )

        # -----------------------------------------
        # Word Count
        # -----------------------------------------

        word_count = len(
            answer.split()
        )

        # -----------------------------------------
        # Technical Score
        # -----------------------------------------

        technical_score = 50

        if mentioned_skills:

            technical_score += min(
                len(mentioned_skills) * 5,
                25
            )

        technical_keywords = [

            "model",
            "algorithm",
            "training",
            "testing",
            "accuracy",
            "evaluation",
            "dataset",
            "prediction",
            "feature",
            "classification",
            "regression",
            "api",
            "database"
        ]

        technical_matches = sum(

            1

            for keyword
            in technical_keywords

            if keyword in answer_lower
        )

        technical_score += min(
            technical_matches * 3,
            25
        )

        technical_score = min(
            technical_score,
            100
        )

        # -----------------------------------------
        # Relevance Score
        # -----------------------------------------

        relevance_score = 50

        question_words = set(
            question.lower().split()
        )

        answer_words = set(
            answer_lower.split()
        )

        common_words = (
            question_words
            .intersection(
                answer_words
            )
        )

        if common_words:

            relevance_score += min(
                len(common_words) * 4,
                25
            )

        if mentioned_skills:

            relevance_score += min(
                len(mentioned_skills) * 5,
                25
            )

        relevance_score = min(
            relevance_score,
            100
        )

        # -----------------------------------------
        # Clarity Score
        # -----------------------------------------

        clarity_score = 50

        if word_count >= 20:

            clarity_score += 15

        if word_count >= 50:

            clarity_score += 15

        if "." in answer:

            clarity_score += 10

        if "," in answer:

            clarity_score += 10

        clarity_score = min(
            clarity_score,
            100
        )

        # -----------------------------------------
        # Completeness Score
        # -----------------------------------------

        completeness_score = 40

        completeness_keywords = [

            "problem",
            "approach",
            "solution",
            "result",
            "outcome",
            "challenge",
            "improved",
            "accuracy",
            "performance"
        ]

        completeness_matches = sum(

            1

            for keyword
            in completeness_keywords

            if keyword in answer_lower
        )

        completeness_score += min(
            completeness_matches * 6,
            40
        )

        if word_count >= 50:

            completeness_score += 10

        completeness_score = min(
            completeness_score,
            100
        )

        # -----------------------------------------
        # Overall Score
        # -----------------------------------------

        overall_score = round(

            (
                technical_score * 0.30

                + relevance_score * 0.25

                + clarity_score * 0.20

                + completeness_score * 0.25
            )
        )

        # -----------------------------------------
        # Answer Quality
        # -----------------------------------------

        if overall_score >= 80:

            answer_quality = "Excellent"

        elif overall_score >= 65:

            answer_quality = "Strong"

        elif overall_score >= 50:

            answer_quality = "Good"

        else:

            answer_quality = (
                "Needs Improvement"
            )

        # -----------------------------------------
        # Strengths
        # -----------------------------------------

        strengths = []

        if mentioned_skills:

            strengths.append(

                "You mentioned relevant "
                "resume skills: "

                + ", ".join(
                    sorted(
                        mentioned_skills
                    )
                )

                + "."
            )

        if word_count >= 50:

            strengths.append(
                "Your answer provides enough "
                "detail to explain your thinking."
            )

        if technical_matches >= 3:

            strengths.append(
                "You included several technical "
                "concepts relevant to the answer."
            )

        if completeness_matches >= 3:

            strengths.append(
                "Your answer covers multiple "
                "parts of the problem-solving process."
            )

        if not strengths:

            strengths.append(
                "You directly attempted to answer "
                "the interview question."
            )

        # -----------------------------------------
        # Improvements
        # -----------------------------------------

        improvements = []

        if technical_score < 70:

            improvements.append(
                "Add more specific technical details "
                "about the tools, algorithms or methods used."
            )

        if relevance_score < 70:

            improvements.append(
                "Keep your answer more closely connected "
                "to the interview question."
            )

        if clarity_score < 70:

            improvements.append(
                "Structure your answer clearly and explain "
                "your points in a logical order."
            )

        if completeness_score < 70:

            improvements.append(
                "Explain the problem, approach, solution "
                "and final result."
            )

        if missing_skills:

            improvements.append(

                "Consider explaining how you used "

                + ", ".join(
                    sorted(
                        missing_skills
                    )[:5]
                )

                + " in your projects."
            )

        if not improvements:

            improvements.append(
                "Add measurable results or project impact "
                "to make the answer even stronger."
            )

        # -----------------------------------------
        # Suggested Better Answer
        # -----------------------------------------

        better_answer = (

            "A stronger interview answer should follow "
            "a clear structure: first explain the problem, "
            "then describe your approach, mention the "
            "technical tools or skills you used, explain "
            "any challenges you faced, and finish with "
            "the measurable result or outcome."
        )

        # -----------------------------------------
        # Follow-up Question
        # -----------------------------------------

        follow_up = (

            "What was the biggest technical challenge "
            "you faced while working on this project, "
            "and how did you solve it?"
        )

        # -----------------------------------------
        # Final Response
        # -----------------------------------------

        return {

            "object":
                "interview.evaluation",

            "status": "success",

            "data": {

                "question":
                    question,

                "answer":
                    request.answer,

                "word_count":
                    word_count,

                "answer_quality":
                    answer_quality,

                "overall_score":
                    overall_score,

                "score_breakdown": {

                    "technical_understanding":
                        technical_score,

                    "relevance":
                        relevance_score,

                    "clarity":
                        clarity_score,

                    "completeness":
                        completeness_score
                },

                "mentioned_resume_skills":
                    sorted(
                        mentioned_skills
                    ),

                "missing_resume_skills":
                    sorted(
                        missing_skills
                    ),

                "what_you_did_well":
                    strengths,

                "what_could_be_improved":
                    improvements,

                "suggested_better_answer":
                    better_answer,

                "follow_up_question":
                    follow_up
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# SAVE CAREER PROFILE
# =========================================================


@app.post("/v1/profile/save")
def save_profile(
    request: CareerProfileRequest
):

    try:

        profile_id = save_career_profile(

            user_id=request.user_id,

            resume_skills=(
                str(request.resume_skills)
            ),

            missing_skills=(
                str(request.missing_skills)
            ),

            career_roles=(
                str(request.career_roles)
            ),

            roadmap=(
                str(request.roadmap)
            ),

            resume_text=request.resume_text
        )

        return {

            "message":
                "Career profile saved successfully.",

            "profile_id":
                profile_id,

            "user_id":
                request.user_id
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET CAREER PROFILE
# =========================================================


@app.get("/v1/profile/{user_id}")
def get_profile(
    user_id: int
):

    try:

        profile = get_career_profile(
            user_id
        )

        if not profile:

            return {

                "user_id": user_id,

                "profile": None,

                "message":
                    "No saved career profile found."
            }

        return {

            "user_id": user_id,

            "profile": {

                "id":
                    profile["id"],

                "user_id":
                    profile["user_id"],

                "resume_skills":
                    profile["resume_skills"],

                "missing_skills":
                    profile["missing_skills"],

                "career_roles":
                    profile["career_roles"],

                "roadmap":
                    profile["roadmap"],

                "resume_text":
                    profile["resume_text"],

                "created_at":
                    profile["created_at"],

                "updated_at":
                    profile["updated_at"]
            }
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
