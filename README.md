# 🧠✈️ AI Counsellor Abroad

### AI-Powered Study Abroad Guidance & University Shortlisting Platform

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql\&logoColor=white)](https://www.postgresql.org/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3-F55036)](https://groq.com/)
[![Llama](https://img.shields.io/badge/Llama-3.3-0467DF)](https://www.llama.com/)
[![gTTS](https://img.shields.io/badge/gTTS-Text%20to%20Speech-4285F4)](https://pypi.org/project/gTTS/)
[![AI](https://img.shields.io/badge/AI-Powered-8A2BE2)](https://www.python.org/)
[![Hackathon](https://img.shields.io/badge/Hackathon-Humanity%20Founders-orange)](https://github.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github\&logoColor=white)](https://github.com/)

---

## 📌 Overview

**AI Counsellor Abroad** is an AI-powered study-abroad counselling platform designed to help students make **confident, personalized, and data-driven decisions** about studying overseas.

The platform combines **AI-powered profile analysis, university shortlisting, application planning, and conversational guidance** into a single modern interface.

Instead of simply providing a list of universities, the application understands the student's profile and helps organize universities into:

* 🟢 **Dream Universities**
* 🟡 **Target Universities**
* 🔵 **Safe Universities**

Students can then **lock their preferred universities** and manage the next steps required for their applications.

> Built as a solution for the **Humanity Founders Hackathon**.

---

## 🎯 Problem Statement

Students planning to study abroad often struggle with:

* Choosing universities suitable for their academic profile.
* Understanding admission requirements.
* Comparing multiple universities.
* Evaluating their chances realistically.
* Organizing application tasks.
* Getting personalized counselling.
* Knowing which universities should be considered Dream, Target, or Safe options.

Traditional counselling can be expensive, time-consuming, and difficult to scale.

### 💡 Solution

**AI Counsellor Abroad** provides an intelligent and empathetic digital counsellor that analyzes a student's profile and assists throughout the university-selection and application-planning journey.

---

## 🚀 Key Features

### 👤 Intelligent Student Onboarding

Collect and organize important student information such as:

* Academic background
* Test scores
* Intended course
* Preferred countries
* Budget
* Career interests
* Academic preferences

---

### 🧠 AI-Powered Profile Analysis

The AI analyzes the student's profile and generates personalized guidance based on their:

* Academic performance
* Preferences
* Career goals
* Target destinations
* University requirements

---

### 🎓 Smart University Shortlisting

Universities are categorized into three levels:

| Category  | Purpose                                           |
| --------- | ------------------------------------------------- |
| 🟢 Dream  | Highly ambitious universities                     |
| 🟡 Target | Universities with realistic admission potential   |
| 🔵 Safe   | Universities offering comparatively safer options |

This helps students create a balanced application strategy.

---

### 🔒 University Locking

Students can lock selected universities after reviewing their recommendations.

This creates a focused application plan instead of repeatedly changing university choices.

---

### 📋 Application Task Management

The platform helps students track application-related activities such as:

* University applications
* Required documents
* Deadlines
* Application status
* Pending tasks

---

### 💬 AI Counselling

Students can interact with the AI counsellor to receive contextual guidance and recommendations throughout their study-abroad journey.

The system is designed to provide responses that are:

* Personalized
* Supportive
* Clear
* Student-focused
* Action-oriented

---

### 🔊 Voice Support

The application uses **gTTS (Google Text-to-Speech)** to provide voice-based output, making the counselling experience more accessible and engaging.

---

### 🎨 Modern User Interface

Built with **Streamlit**, the application provides a clean and interactive interface for:

* Student onboarding
* Profile analysis
* University recommendations
* Counselling
* Application tracking

---

## 🏗️ AI Workflow

```text
                ┌─────────────────────┐
                │   Student Onboarding│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Profile Analysis  │
                │ Academic + Goals +  │
                │ Preferences + Budget│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   AI Counsellor     │
                │ Groq + Llama 3.3    │
                └──────────┬──────────┘
                           │
                           ▼
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
         🟢 Dream      🟡 Target      🔵 Safe
        Universities  Universities  Universities
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Student Selection  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Lock Universities │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Application Tasks   │
                │ & Progress Tracking │
                └─────────────────────┘
```

---

## 🔄 User Journey

```text
Register / Start
       ↓
Student Onboarding
       ↓
Build Student Profile
       ↓
AI Profile Analysis
       ↓
University Recommendations
       ↓
Dream / Target / Safe
       ↓
Review Universities
       ↓
Lock Selected Universities
       ↓
Application Tasks
       ↓
Track Progress
       ↓
AI Counselling & Guidance
```

---

## 🧩 Technology Stack

| Layer                    | Technology                     |
| ------------------------ | ------------------------------ |
| Frontend / UI            | Streamlit                      |
| Programming Language     | Python                         |
| AI Model                 | Llama 3.3                      |
| AI Inference             | Groq                           |
| Database                 | PostgreSQL                     |
| Text-to-Speech           | gTTS                           |
| Data Processing          | Python                         |
| Application Architecture | AI + Database + Interactive UI |

---

## 🛠️ Core Technologies

### Python

Used as the primary programming language for application logic, data processing, AI integration, and backend functionality.

### Streamlit

Used to build the interactive web application and modern user interface.

### Groq + Llama 3.3

Used to power the AI counselling and natural-language reasoning experience.

### PostgreSQL

Used for persistent storage of student profiles, university information, selections, and application-related data.

### gTTS

Used to convert AI-generated counselling responses into speech.

---

## 📂 Project Structure

```text
AI_Counsellor_Abroad_APP/
│
├── app/
│   ├── pages/
│   ├── components/
│   └── utils/
│
├── data/
│   └── universities/
│
├── database/
│   ├── models/
│   └── queries/
│
├── services/
│   ├── ai_counsellor/
│   ├── university_matching/
│   └── text_to_speech/
│
├── assets/
│   ├── images/
│   └── audio/
│
├── .env.example
├── requirements.txt
├── app.py
└── README.md
```

> Adjust the structure above to match the actual repository if your folder names are different.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/syed-sadain/AI_Counsellor_Abroad_APP.git
```

### 2. Navigate to the Project

```bash
cd AI_Counsellor_Abroad_APP
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_postgresql_connection_string
```

Never commit real API keys or database credentials to GitHub.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🗄️ Database

PostgreSQL is used to persist application data.

Potential entities include:

```text
Student
   │
   ├── Academic Profile
   ├── Preferences
   ├── Test Scores
   └── Career Goals
          │
          ▼
      AI Analysis
          │
          ▼
     Universities
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
  Dream Target Safe
    │     │     │
    └─────┼─────┘
          ▼
   Locked Universities
          │
          ▼
   Application Tasks
```

---

## 🤖 AI Counselling Capabilities

The AI counsellor can be extended to support questions such as:

```text
"Which universities match my profile?"

"What are my safer university options?"

"Which countries fit my budget?"

"What documents do I need?"

"Which university should I prioritize?"

"What should I complete before the application deadline?"
```

The AI layer can use the student's stored profile and application context to provide more relevant guidance.

---

## 🎓 University Recommendation Strategy

The recommendation system is designed around three categories:

### 🟢 Dream

Highly competitive universities where admission may be challenging but potentially achievable.

### 🟡 Target

Universities where the student's academic and profile characteristics provide a more realistic opportunity.

### 🔵 Safe

Universities where the student's profile is comparatively stronger against typical admission requirements.

> These categories are intended as guidance and should not be interpreted as guaranteed admission predictions.

---

## 📊 Example Application Flow

```text
Student Profile
       ↓
Academic Score
       +
Test Scores
       +
Course Preference
       +
Country Preference
       +
Budget
       ↓
AI Profile Analysis
       ↓
University Matching
       ↓
┌────────┬────────┬────────┐
│ Dream  │ Target │  Safe  │
└────────┴────────┴────────┘
       ↓
Student Selects Universities
       ↓
Lock Choices
       ↓
Application Checklist
       ↓
Track Progress
```

---

## 💡 Use Cases

AI Counsellor Abroad can support:

* 🎓 Undergraduate students
* 🎓 Master's applicants
* 🌍 International education planning
* 🏫 University discovery
* 📊 Profile evaluation
* 📝 Application planning
* 📅 Deadline management
* 💬 AI-based counselling

---

## 🔮 Future Improvements

### 🤖 Advanced AI

* RAG-based university knowledge system
* Personalized admission probability estimation
* AI-generated SOP assistance
* AI-powered LOR guidance
* Intelligent document analysis
* Multi-agent counselling workflows

### 📊 Analytics

* University comparison dashboards
* Cost-of-study analysis
* Country comparison
* Scholarship matching
* ROI analysis
* Personalized application analytics

### 🌍 Real-Time Data

* Live university deadlines
* Tuition fee updates
* Scholarship availability
* Admission requirement updates
* Visa information
* University ranking updates

### 🔊 Multimodal Experience

* Voice-based AI counselling
* Speech-to-text interaction
* Document upload and analysis
* Personalized AI reports
* Multilingual counselling

---

## 🏆 Hackathon Context

This project was developed for the **Humanity Founders Hackathon** with a focus on using AI to make the study-abroad decision-making process more accessible, personalized, and student-friendly.

The project demonstrates the integration of:

```text
AI
+
Data
+
Personalization
+
Modern UI
+
Database
+
Automation
```

into a practical real-world application.

---

## 📌 Why This Project?

The core idea is simple:

> **Students shouldn't have to navigate the complexity of studying abroad alone.**

AI Counsellor Abroad aims to provide a structured journey from:

**Profile → Analysis → University Selection → Locked Choices → Application Tasks**

while keeping the experience personalized and empathetic.

---

## 👤 Author

### Syed Sadain

**Python Full Stack Developer | Backend Developer | AI/ML Engineer**

🔗 GitHub:
https://github.com/syed-sadain

🔗 LinkedIn:
https://www.linkedin.com/in/syed-sadain-a56ba827/

---

## ⭐ Support

If you find this project useful:

⭐ Star the repository
🍴 Fork the project
💡 Explore the implementation
🤝 Share your feedback

---

## 📜 Disclaimer

AI Counsellor Abroad is an educational and decision-support application.

University recommendations, Dream/Target/Safe classifications, and AI-generated guidance are **not guarantees of admission, scholarships, visas, or application outcomes**. Students should verify important admission and visa requirements through official university and government sources.
