# AutoThink AI Career Strategist v2

Multi-agent resume analysis and optimization powered by Gemini and LangChain.

## Setup

```bash
cd AutoThink-Resume
pip install -r requirements.txt
cp .env.example .env
# Add GEMINI_API_KEY to .env
streamlit run app.py
```

## Features

- 9 agents: Parser, Analyzer, Solver, ATS, Recruiter, Critic, Improver, Career Coach, Finalizer
- Live agent logs with timestamps
- ATS dashboard with section progress bars
- Before/after diff viewer
- Multi-role mode (AI Engineer, Backend Developer, Data Analyst)
- LaTeX + PDF generation (pdflatex fallback to .tex)
- Demo mode without API key
- CrewAI / LangChain framework toggle

## CLI

```bash
python main.py --demo
python main.py --resume data/sample_resume.txt --job-desc data/sample_job.txt
```

## Author

Prajwal Kedari — [GitHub](https://github.com/prajwalkedari) | [LinkedIn](https://www.linkedin.com/in/prajwalkedari/) | [Portfolio](https://prajwalkedari.vercel.app/)
