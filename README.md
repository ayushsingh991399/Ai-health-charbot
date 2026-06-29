# 🩺 Medical HealthBot: AI-Powered Patient Education System

An AI-powered healthcare chatbot built using **LangGraph**, **Cohere LLM**, **Tavily Search API**, and **Streamlit**.

## 📌 Project Overview

Medical HealthBot helps users learn about medical conditions by:
- Searching trusted medical information with Tavily
- Summarizing it into patient-friendly language
- Generating an AI quiz
- Evaluating answers
- Providing personalized feedback

## 🚀 Features

- 🔍 Tavily Search integration
- 🤖 Cohere LLM summaries
- 📖 Patient-friendly explanations
- 📝 AI-generated quizzes
- ✅ Answer evaluation
- 💬 Streamlit chatbot UI
- 🧠 LangGraph workflow

## 🛠️ Technologies

- Python
- LangGraph
- LangChain
- Cohere
- Tavily Search
- Streamlit
- python-dotenv

## 📂 Project Structure

```text
Medical-HealthBot/
│
├── main.py

├── graph.py
├── function.py
├── state.py
├── config.env
├── requirements.txt
└── README.md
```

## 🔄 Workflow

```text
START
  │
  ▼
Ask Topic
  │
  ▼
Tavily Search
  │
  ▼
Summarize
  │
  ▼
Display Summary
  │
  ▼
Ready Check
  │
  ▼
Generate Quiz
  │
  ▼
Ask Quiz
  │
  ▼
Receive Answer
  │
  ▼
Grade Answer
  │
  ▼
Display Feedback
  │
  ▼
Continue Session
  │
  ├── Yes ─► Reset State ─► Ask Topic
  └── No ─► END
```

## ⚙️ Installation

```bash
git clone https://github.com/ayushsingh991399/Ai-health-chatbot

python -m venv .venv
```

Activate:

**Windows**
```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 API Keys

Create a `config.env` file:

```env
COHERE_API_KEY=your_cohere_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## ▶️ Run

```bash
streamlit run app.py
```

## 👨‍💻 Author

**Ayush Singh**

B.Tech Computer Science Engineering

Generative AI • Machine Learning • Data Science
