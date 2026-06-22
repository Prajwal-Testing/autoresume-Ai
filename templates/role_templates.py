"""Role-specific resume templates and guidance."""
from config import ROLE_TEMPLATES


def get_role_template(role: str) -> dict:
    return ROLE_TEMPLATES.get(role, ROLE_TEMPLATES["AI Engineer"])


def get_role_descriptions() -> dict:
    return {
        "AI Engineer": "Machine learning, deep learning, and AI systems",
        "Backend Developer": "Scalable APIs, microservices, and system design",
        "Data Analyst": "Data visualization, analytics, and business intelligence",
    }


def get_bullet_point_examples(role: str) -> list:
    examples = {
        "AI Engineer": [
            "Deployed transformer NLP model improving accuracy by 23%",
            "Built RAG system reducing inference latency by 40%",
        ],
        "Backend Developer": [
            "Architected microservices reducing API latency from 2s to 200ms",
            "Implemented Kubernetes CI/CD reducing deployment time by 80%",
        ],
        "Data Analyst": [
            "Built Tableau dashboards analyzing 5M+ records for real-time insights",
            "Developed ETL pipeline processing 1B+ records daily at 99.8% accuracy",
        ],
    }
    return examples.get(role, examples["AI Engineer"])
