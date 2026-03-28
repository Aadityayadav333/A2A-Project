# 🤖 A2A Project — Agent-to-Agent Communication

<!-- VIDEO DEMO -->
## 📽️ Demo

[![Watch Demo](https://img.shields.io/badge/▶%20Watch%20Demo-red?style=for-the-badge&logo=youtube)](YOUR_VIDEO_URL_HERE)


https://github.com/user-attachments/assets/d3dd46f4-32b4-41fc-9135-2a6ab8e0738b



---

## 🎯 What It Does

Three AI agents coordinate autonomously to organize a **badminton game**:

- **Elon Agent** (Host) asks Jeff and Mark about their availability
- **Jeff Agent** & **Mark Agent** check their own calendars and respond
- Elon finds a common time, checks court availability, and books it

A real-world demo of multi-framework Agent-to-Agent (A2A) communication.

---

## 🏗️ Architecture

```
User → Elon Agent (Google ADK)
              ↓ A2A Protocol
      ┌───────┴───────┐
  Jeff Agent      Mark Agent
  (LangChain)     (CrewAI)
      └───────┬───────┘
              ↓
     Find common slot → Book court
```

| Agent | Framework | Port | Role |
|-------|-----------|------|------|
| Elon | Google ADK | 8000 | Host / Coordinator |
| Jeff | LangChain + LangGraph | 10004 | Jeff's Scheduling Assistant |
| Mark | CrewAI | 10005 | Mark's Scheduling Assistant |

---

## 🛠️ Tech Stack

- **A2A SDK** — Agent-to-Agent protocol
- **Google ADK** — Elon's conversational agent
- **LangChain / LangGraph** — Jeff's agent with memory
- **CrewAI** — Mark's agent
- **Google Gemini** — LLM backbone
- **UV** — Fast Python package manager

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/Aadityayadav333/A2A-Project.git
cd A2A-Project
```

### 2. Add your API key
Create a `.env` file in the root:
```env
GOOGLE_API_KEY=your_google_api_key_here
```
Get one at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 3. Install dependencies (per agent)
```bash
cd elon_agent && uv sync
cd ../jeff_agent && uv sync
cd ../mark_agent && uv sync
```

---

## 🚀 Running

Open **3 terminals**:

```bash
# Terminal 1 — Jeff Agent
cd jeff_agent && uv run python __main__.py

# Terminal 2 — Mark Agent
cd mark_agent && uv run python __main__.py

# Terminal 3 — Elon Agent (Web UI)
cd elon_agent && uv run adk web
```

Then open **http://127.0.0.1:8000**, select `elon` agent, and try:

> *"Can you organize a badminton game with Jeff and Mark?"*

---

## 📁 Project Structure

```
a2a-project/
├── .env
├── elon_agent/        # Google ADK — coordinator
│   └── elon/
│       ├── agent.py
│       └── tools.py
├── jeff_agent/        # LangChain — Jeff's assistant
│   ├── agent.py
│   ├── tools.py
│   └── __main__.py
└── mark_agent/        # CrewAI — Mark's assistant
    ├── agent.py
    ├── tools.py
    └── __main__.py
```

---

## 👥 Credits

Built by **Aaditya Yadav** & **Hassan Mahmood**

---

