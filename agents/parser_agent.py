"""Parser Agent: Extracts structured data from resume text."""
import re
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from models.resume_model import Experience, ResumeData


class ParserAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Parser Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")

        if not resume_text.strip():
            self._log_error("No resume text provided")
            return {"status": "error", "message": "No resume text provided"}

        try:
            prompt = f"""Parser agent: Extract structured resume data from:

{resume_text}

Return name, email, phone, summary, experience bullets, skills, education."""
            self._generate(prompt)
            resume_data = self._parse_heuristic(resume_text)
            self._log_complete(f"Parsed {resume_data.personal_info.name or 'resume'}")
            return {
                "status": "success",
                "data": resume_data.to_dict(),
                "raw_text": resume_text,
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}

    def _parse_heuristic(self, resume_text: str) -> ResumeData:
        resume_data = ResumeData()
        lines = [line.strip() for line in resume_text.split("\n") if line.strip()]

        for line in lines[:5]:
            if len(line) < 80 and line.isupper():
                resume_data.personal_info.name = line.title()
                break
        if not resume_data.personal_info.name and lines:
            resume_data.personal_info.name = lines[0][:80]

        email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", resume_text)
        if email_match:
            resume_data.personal_info.email = email_match.group(0)

        phone_match = re.search(r"\+?\d[\d\s\-().]{7,}\d", resume_text)
        if phone_match:
            resume_data.personal_info.phone = phone_match.group(0).strip()

        for line in lines:
            if 50 < len(line) < 350 and "@" not in line:
                resume_data.summary = line
                break

        skill_keywords = [
            "python", "java", "sql", "javascript", "react", "aws", "docker",
            "kubernetes", "tensorflow", "pytorch", "pandas", "tableau",
        ]
        lower = resume_text.lower()
        resume_data.skills = [kw.title() for kw in skill_keywords if kw in lower]

        bullets = [
            line.lstrip("-•* ").strip()
            for line in lines
            if line.startswith(("-", "•", "*")) and len(line) > 10
        ]
        if bullets:
            resume_data.experience.append(
                Experience(
                    company="Recent Role",
                    title="Professional Experience",
                    duration="",
                    description=bullets[:6],
                )
            )

        return resume_data
