"""Configuration management for AutoThink Resume Generator."""
import os
from dotenv import load_dotenv

load_dotenv()

USE_CREWAI = os.getenv("USE_CREWAI", "False").lower() in ("true", "1", "yes")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

APP_TITLE = "AutoThink AI Career Strategist"
APP_ICON = "🚀"

ROLE_TEMPLATES = {
    "AI Engineer": {
        "keywords": [
            "machine learning", "deep learning", "pytorch", "tensorflow",
            "transformers", "llm", "nlp",
        ],
        "skills": ["Python", "CUDA", "distributed training", "model optimization"],
        "projects_suggested": ["LLM fine-tuning", "RAG system", "AI agent development"],
    },
    "Backend Developer": {
        "keywords": [
            "rest api", "microservices", "database design", "docker",
            "kubernetes", "nodejs", "python",
        ],
        "skills": ["System design", "Database optimization", "DevOps", "API design"],
        "projects_suggested": ["Scalable API", "Microservices", "CI/CD pipeline"],
    },
    "Data Analyst": {
        "keywords": [
            "sql", "tableau", "power bi", "pandas", "statistics",
            "data visualization", "business intelligence",
        ],
        "skills": ["SQL", "Python/R", "Data visualization", "Statistical analysis"],
        "projects_suggested": ["Dashboard development", "ETL pipeline", "Predictive analytics"],
    },
}

LATEX_OUTPUT_DIR = "generated_resumes"
LATEX_COMPILER = "pdflatex"

ATS_SECTIONS = ["header", "summary", "experience", "skills", "education", "projects"]
ATS_WEIGHTS = {
    "header": 5,
    "summary": 15,
    "experience": 30,
    "skills": 25,
    "education": 15,
    "projects": 10,
}

LOG_MAX_ITEMS = 100
LOG_LEVEL = "INFO"
DEMO_MODE = os.getenv("DEMO_MODE", "False").lower() in ("true", "1", "yes")

AUTHOR = "Prajwal Kedari"
GITHUB_URL = "https://github.com/prajwalkedari"
LINKEDIN_URL = "https://www.linkedin.com/in/prajwalkedari/"
PORTFOLIO_URL = "https://prajwalkedari.vercel.app/"

AGENT_TIMEOUT = 30
MAX_TOKENS = 2048
API_KEY_FILE = ".gemini_key"
