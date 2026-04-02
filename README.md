# 🤖 AI Recruitment System

An end-to-end AI-powered recruitment platform that automates resume screening, candidate ranking, interview question generation, and bias detection — built with Python and the Anthropic Claude API.


---

## 🎯 Features

| Feature | Description |
|---|---|
| 📄 **Resume Parser** | Extracts structured data (skills, experience, education) from raw resume text |
| 🏆 **Candidate Ranker** | Scores and ranks candidates against job descriptions using AI |
| 🎤 **Interview Question Generator** | Creates tailored interview questions per candidate profile |
| ⚖️ **Bias Detector** | Flags potentially biased language in job descriptions |
| 📊 **Recruitment Report** | Generates a full hiring report with recommendations |

---

## 🗂️ Project Structure

```
ai_recruitment/
├── src/
│   ├── agents/
│   │   ├── resume_parser.py        # Parses resumes into structured JSON
│   │   ├── candidate_ranker.py     # Ranks candidates vs job description
│   │   ├── interview_generator.py  # Generates interview questions
│   │   └── bias_detector.py        # Detects bias in job postings
│   ├── utils/
│   │   ├── claude_client.py        # Anthropic API wrapper
│   │   └── report_generator.py     # Generates final hiring report
│   └── models/
│       └── schemas.py              # Pydantic data models
├── data/
│   └── sample_resumes/             # Sample resumes for testing
├── tests/
│   └── test_agents.py              # Unit tests
├── main.py                         # CLI entry point
├── requirements.txt
└── .env.example
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-recruitment-system.git
cd ai-recruitment-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment
```bash
cp .env.example .env
# Add your Anthropic API key to .env
```

### 4. Run the full pipeline
```bash
python main.py
```

### 5. Run individual agents
```bash
# Parse a resume
python main.py --mode parse --file data/sample_resumes/alice.txt

# Rank candidates
python main.py --mode rank

# Detect bias in a job description
python main.py --mode bias

# Generate interview questions
python main.py --mode interview
```

---


## 🧠 How It Works

```
Job Description + Resumes
        │
        ▼
  ┌─────────────┐
  │ Resume      │  → Structured JSON per candidate
  │ Parser      │
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │ Bias        │  → Flags issues in job description
  │ Detector    │
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │ Candidate   │  → Scored & ranked list
  │ Ranker      │
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │ Interview   │  → Tailored questions per candidate
  │ Generator   │
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │ Report      │  → Final recruitment recommendation
  │ Generator   │
  └─────────────┘
```

---

## 📦 Tech Stack

- **Python 3.10+**
- **Pydantic** — Data validation & schemas
- **Rich** — Beautiful terminal output
- **python-dotenv** — Environment management

---




