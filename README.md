# 🚀 CareerPilot AI

### AI-Powered Career Coach & Technical Assistant

<p align="center">
  <b>Personalized career guidance powered by AI, FastAPI, PostgreSQL, Streamlit & Groq</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql)
![Groq](https://img.shields.io/badge/Groq-AI-orange)
![Render](https://img.shields.io/badge/Render-Deployment-46E3B7)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)

</p>

---

## 🌐 Live Project

### 🚀 CareerPilot AI

**Frontend:**
Add your Streamlit Cloud URL here.

**Backend API:**
https://careerpilot-ai-2-qxcm.onrender.com

**API Documentation:**
https://careerpilot-ai-2-qxcm.onrender.com/docs

---

# 📌 Overview

**CareerPilot AI** is an end-to-end AI-powered career assistant designed to help users understand their career profile, identify skill gaps, explore career roles, create learning roadmaps, prepare for interviews, and receive technical guidance.

The application combines a modern web frontend with a REST API, persistent PostgreSQL storage, and cloud-based AI inference through Groq.

The project demonstrates how to build and deploy a complete AI application rather than only a standalone machine-learning model.

---

# ✨ Key Features

### 🤖 AI Career Assistant

Users can interact with CareerPilot using natural language.

The assistant can help with:

* Career planning
* Skill recommendations
* Career roadmaps
* Job preparation
* Interview preparation
* Project ideas
* Technical questions
* Programming
* Data Science
* Machine Learning
* AI & NLP
* Resume-related guidance

---

### 🎯 Personalized Responses

CareerPilot can use information from the user's profile, including:

```text
Resume Skills
      ↓
Missing Skills
      ↓
Career Roles
      ↓
Career Roadmap
      ↓
Recent Conversation
      ↓
Personalized AI Response
```

This allows the chatbot to provide context-aware career guidance.

---

### 💬 Conversational AI

CareerPilot maintains recent conversation context so users can ask follow-up questions.

Example:

```text
User:
What should I learn next?

CareerPilot:
Based on your current profile, focus on...

User:
Why?

CareerPilot:
Because those skills address your current gaps...

User:
Give me a project.

CareerPilot:
Here is a project aligned with those skills...
```

---

### 👤 Authentication

The backend supports:

* User registration
* User login
* User identification
* Persistent user data

---

### 🗄️ PostgreSQL Database

CareerPilot stores application data using PostgreSQL.

Current database tables include:

```text
users
career_profiles
chat_messages
```

---

### ⚡ FastAPI Backend

The application exposes REST API endpoints through FastAPI.

Interactive API documentation is available through Swagger UI.

```text
https://careerpilot-ai-2-qxcm.onrender.com/docs
```

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │    User / Browser   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit Cloud   │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               │ HTTP Requests
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │       Render        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌─────────────────┐           ┌─────────────────┐
       │   PostgreSQL    │           │     Groq AI     │
       │     Database    │           │  Model Inference│
       └─────────────────┘           └─────────────────┘
```

---

# 🔄 Application Workflow

```text
                    User
                     │
                     ▼
              Register / Login
                     │
                     ▼
              Career Profile
                     │
                     ▼
                Ask Question
                     │
                     ▼
             Streamlit Frontend
                     │
                     ▼
               FastAPI API
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
      PostgreSQL             Groq AI
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
            Personalized Response
                     │
                     ▼
                   User
```

---

# 🛠️ Technology Stack

## Frontend

* Python
* Streamlit

## Backend

* Python
* FastAPI
* Uvicorn

## AI

* Groq API
* OpenAI-compatible Python SDK
* GPT-OSS model

## Database

* PostgreSQL
* psycopg2

## Deployment

* GitHub
* Render
* Streamlit Cloud

---

# 📂 Project Structure

```text
careerpilot.ai/
│
├── app.py
│   └── Streamlit frontend
│
├── api.py
│   └── FastAPI backend
│
├── llm_service.py
│   └── Groq AI integration
│
├── database.py
│   └── PostgreSQL connection & tables
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│
└── .gitignore
```

---

# 🧠 AI Architecture

The AI service builds a structured context before sending a request to Groq.

```text
User Profile
│
├── Resume Skills
├── Missing Skills
├── Career Roles
├── Career Roadmap
└── Conversation History
        │
        ▼
   CareerPilot Prompt
        │
        ▼
      Groq API
        │
        ▼
   AI Generated Response
```

The AI service is separated into `llm_service.py`, making the LLM layer easier to modify independently from the API and frontend.

---

# 🔌 API

## Production Backend

```text
https://careerpilot-ai-2-qxcm.onrender.com
```

## Swagger UI

```text
https://careerpilot-ai-2-qxcm.onrender.com/docs
```

Swagger can be used to test available API endpoints directly.

---

# 🔐 Environment Variables

The application uses environment variables for sensitive configuration.

Required backend variables:

```text
DATABASE_URL=your_postgresql_url
GROQ_API_KEY=your_groq_api_key
```

### Security

API keys and database credentials are **never stored directly in the source code**.

Example `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

---

# 💻 Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/abhilesh200/careerpilot.ai.git
```

```bash
cd careerpilot.ai
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Set your Groq API key:

```cmd
setx GROQ_API_KEY "your_groq_api_key"
```

Configure your PostgreSQL database:

```text
DATABASE_URL=your_database_url
```

Restart your terminal after using `setx`.

---

# ▶️ Run Backend

Start FastAPI:

```bash
uvicorn api:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Run Frontend

Start Streamlit:

```bash
streamlit run app.py
```

---

# ☁️ Deployment

## Backend — Render

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

### Environment Variables

```text
DATABASE_URL
GROQ_API_KEY
```

---

## Frontend — Streamlit Cloud

The Streamlit application communicates with the deployed FastAPI backend.

Backend URL:

```python
API_URL = "https://careerpilot-ai-2-qxcm.onrender.com"
```

---

# 📊 Database Design

CareerPilot currently uses three primary tables:

```text
┌──────────────────────┐
│        users         │
├──────────────────────┤
│ id                   │
│ name                 │
│ email                │
│ password             │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   career_profiles    │
├──────────────────────┤
│ user_id              │
│ resume skills        │
│ missing skills       │
│ career roles         │
│ roadmap              │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    chat_messages     │
├──────────────────────┤
│ user_id              │
│ role                 │
│ message              │
│ timestamp            │
└──────────────────────┘
```

---

# 🧪 Example Interaction

### User

```text
I want to become a Data Scientist. What should I learn?
```

### CareerPilot

```text
Based on your current profile, you should focus on
strengthening Python, SQL, statistics and machine learning.

A practical next step would be to build an end-to-end
machine learning project...
```

The actual response is generated dynamically using the user's available CareerPilot context.

---

# 🚀 Engineering Highlights

This project demonstrates practical experience with:

* REST API development
* FastAPI
* PostgreSQL
* Database integration
* AI API integration
* Prompt engineering
* Conversational AI
* Environment variable management
* Cloud deployment
* Streamlit application development
* Git/GitHub workflow
* Backend/frontend integration

---

# 📈 Future Improvements

Potential future extensions:

* Resume PDF parsing
* Automated skill extraction
* Job-description analysis
* ATS-style resume analysis
* Job recommendation
* Interview simulation
* Technical interview mode
* Learning progress tracking
* Career analytics dashboard
* Job application tracking
* More advanced profile-based recommendations

---

# 🎯 Project Objective

CareerPilot AI was built to demonstrate how modern AI applications can combine:

```text
Artificial Intelligence
        +
Backend Engineering
        +
Database Systems
        +
Frontend Development
        +
Cloud Deployment
```

into a single end-to-end application.

---

# 👨‍💻 Author

## Abhilesh Kumar

**Data Science | Machine Learning | AI | NLP | Python**

### GitHub

https://github.com/abhilesh200

### LinkedIn

https://www.linkedin.com/in/abhilesh-kumar-2a4aa7286

---

# ⭐ If You Like This Project

Consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.
