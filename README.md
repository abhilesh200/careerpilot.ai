# 🚀 CareerPilot AI

### AI-Powered Career Coach, Technical Mentor & Career Planning Assistant

CareerPilot AI is an **end-to-end AI career assistant** designed to help users understand their career profile, identify skill gaps, explore suitable career roles, build learning roadmaps, prepare for interviews, and get personalized technical guidance.

The application combines **AI, FastAPI, PostgreSQL, Streamlit, and Groq** into a production-style web application.

---

## 🌟 Features

### 🤖 AI Career Chatbot

CareerPilot AI provides personalized conversations using the user's career profile.

It can help with:

* Career planning
* Skill recommendations
* Career roadmaps
* Job preparation
* Interview preparation
* Project recommendations
* Technical questions
* Programming problems
* Resume-related guidance
* Learning guidance

---

### 🎯 Personalized Career Guidance

The chatbot can use information such as:

* Resume skills
* Missing skills
* Target career roles
* Career roadmap
* Previous conversation history

This allows CareerPilot to provide more personalized responses instead of only giving generic answers.

---

### 💬 Conversation History

CareerPilot maintains recent conversation context so users can ask follow-up questions naturally.

Example:

```text
User:
What should I learn next?

CareerPilot:
Statistics should be your next focus.

User:
Why?

CareerPilot:
Based on your current skill profile...
```

---

### 👤 User Authentication

The application supports:

* User registration
* User login
* User profile management
* Persistent user data

Passwords are handled by the backend authentication system and user information is stored in PostgreSQL.

---

### 🧠 AI-Powered Technical Assistance

CareerPilot can assist with:

* Python
* SQL
* Data Science
* Machine Learning
* Deep Learning
* Artificial Intelligence
* NLP
* Statistics
* FastAPI
* APIs
* Docker
* Git
* Programming
* Debugging
* Computer Science

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │   Streamlit Cloud    │
                         │      Frontend        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         │        Render        │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
          ┌──────────────────┐             ┌──────────────────┐
          │   PostgreSQL     │             │      Groq AI     │
          │     Database     │             │   AI Inference   │
          └──────────────────┘             └──────────────────┘
```

---

# 🛠️ Tech Stack

## Frontend

* Python
* Streamlit

## Backend

* Python
* FastAPI
* Uvicorn

## Database

* PostgreSQL
* psycopg2

## AI

* Groq API
* OpenAI-compatible Python SDK
* GPT-OSS model

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
│
├── api.py
│
├── llm_service.py
│
├── database.py
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

### Important Files

| File               | Description                                |
| ------------------ | ------------------------------------------ |
| `app.py`           | Streamlit frontend                         |
| `api.py`           | FastAPI backend and API endpoints          |
| `llm_service.py`   | AI/Groq integration and CareerPilot prompt |
| `database.py`      | PostgreSQL database connection and tables  |
| `requirements.txt` | Python dependencies                        |
| `README.md`        | Project documentation                      |

---

# 🔄 Application Workflow

```text
1. User opens CareerPilot
            ↓
2. User registers / logs in
            ↓
3. User career profile is loaded
            ↓
4. User asks a question
            ↓
5. Streamlit sends request to FastAPI
            ↓
6. FastAPI retrieves relevant profile data
            ↓
7. Career context is added to the AI prompt
            ↓
8. Request is sent to Groq
            ↓
9. Groq generates response
            ↓
10. CareerPilot returns personalized answer
            ↓
11. Conversation can continue using recent history
```

---

# 🔌 API

CareerPilot provides a FastAPI backend.

### Production API

```text
https://careerpilot-ai-2-qxcm.onrender.com
```

### Swagger Documentation

```text
https://careerpilot-ai-2-qxcm.onrender.com/docs
```

The Swagger interface can be used to test the backend endpoints directly.

---

# 🤖 AI Integration

CareerPilot uses Groq for cloud-based AI inference.

The application uses an OpenAI-compatible client configuration:

```python
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
```

The API key is loaded through an environment variable.

```text
GROQ_API_KEY
```

No API key is stored inside the source code.

---

# 🔐 Environment Variables

Create the following environment variables for the backend:

```text
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_postgresql_database_url
```

### Security

Never commit API keys or database credentials to GitHub.

Use environment variables instead.

Example `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

---

# 💻 Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/abhilesh200/careerpilot.ai.git
```

```bash
cd careerpilot.ai
```

---

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Set your Groq API key.

Windows CMD:

```cmd
setx GROQ_API_KEY "your_groq_api_key"
```

Set your PostgreSQL database URL:

```text
DATABASE_URL=your_database_url
```

Restart your terminal after using `setx`.

---

# ▶️ Run Backend

Start the FastAPI server:

```bash
uvicorn api:app --reload
```

The API will run at:

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

The frontend will open in your browser.

---

# 🗄️ Database

CareerPilot uses PostgreSQL for persistent data storage.

The database contains tables for:

```text
users
career_profiles
chat_messages
```

The FastAPI application initializes/verifies the required PostgreSQL tables during startup.

---

# 🌐 Deployment

## Backend — Render

The FastAPI backend is deployed using Render.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

```text
DATABASE_URL
GROQ_API_KEY
```

---

## Frontend — Streamlit Cloud

The Streamlit frontend connects to the deployed FastAPI backend.

The frontend API URL is configured as:

```python
API_URL = "https://careerpilot-ai-2-qxcm.onrender.com"
```

---

# 📊 Database Flow

```text
User
 │
 ├── Registration
 │       ↓
 │     users
 │
 ├── Career Profile
 │       ↓
 │   career_profiles
 │
 └── AI Chat
         ↓
    chat_messages
```

---

# 🧠 CareerPilot AI Prompt System

The AI receives structured career context:

```text
USER PROFILE
│
├── Resume Skills
├── Missing Skills
├── Career Roles
├── Career Roadmap
└── Recent Conversation
```

This information is combined with the current user question before sending the request to the AI model.

This enables contextual conversations such as:

```text
User:
What should I learn next?

CareerPilot:
Based on your current skills and identified gaps,
focus on...

User:
Give me a project.

CareerPilot:
A suitable project would be...
```

---

# 🚀 Future Improvements

Planned improvements include:

* Resume parsing
* Job recommendation system
* Job description analysis
* ATS resume scoring
* Skill-gap visualization
* Personalized learning plans
* Interview simulation
* Mock technical interviews
* Job application tracking
* LinkedIn profile analysis
* AI-generated project recommendations
* Real-time job search
* Advanced analytics dashboard

---

# 📈 Project Goals

CareerPilot AI aims to combine:

```text
AI
+
Career Guidance
+
Technical Mentoring
+
Resume Assistance
+
Skill Gap Analysis
+
Learning Roadmaps
+
Interview Preparation
```

into a single career development platform.

---

# 👨‍💻 Author

**Abhilesh Kumar**

Data Science | Machine Learning | AI | NLP | Python

GitHub:

```text
https://github.com/abhilesh200
```

LinkedIn:

```text
https://www.linkedin.com/in/abhilesh-kumar-2a4aa7286
```

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and portfolio purposes.
