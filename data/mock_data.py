"""Mock data for demo mode."""

def get_mock_resume() -> str:
    return """
JOHN DOE
San Francisco, CA | john.doe@email.com | +1-555-0123 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced Machine Learning Engineer with 5+ years of expertise in deep learning and NLP.
Passionate about building scalable AI systems and solving complex problems.

EXPERIENCE

Senior ML Engineer | TechCorp Inc. | San Francisco, CA | 2022 - Present
- Designed transformer-based NLP model improving accuracy from 87% to 94%
- Led team of 3 engineers to develop recommendation system handling 10M+ requests/day
- Optimized inference pipeline reducing latency by 50%

ML Engineer | DataCo Solutions | San Francisco, CA | 2020 - 2022
- Developed computer vision pipeline for image classification (95% accuracy)
- Built monitoring system detecting 15+ data drift issues

SKILLS
Python, SQL, TensorFlow, PyTorch, AWS, Docker, Kubernetes, MLflow

EDUCATION
B.S. in Computer Science | Stanford University | 2018

PROJECTS
- RAG System for Enterprise Search improving search relevance by 35%
- Time Series Forecasting LSTM model with 72% directional accuracy
"""


def get_mock_job_description() -> str:
    return """
Senior ML Engineer - AI/ML Platform

Required Qualifications:
- 5+ years in machine learning and software engineering
- Expert Python and SQL
- TensorFlow and PyTorch experience
- Cloud platforms (AWS, GCP)
- Distributed computing and MLOps
- NLP/LLM experience preferred
- Kubernetes and containerization
"""
