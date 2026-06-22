"""Analyzer Agent: Analyzes resume content and gaps."""
from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Analyzer Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")
        job_description = input_data.get("job_description", "")

        try:
            prompt = f"""Analyzer agent: Analyze this resume:

{resume_text}

Job Description:
{job_description or 'N/A'}

Identify skills, gaps, strengths, and alignment."""
            analysis = self._generate(prompt)
            result = {
                "keywords_found": self._extract_keywords(resume_text),
                "gaps": self._identify_gaps(resume_text),
                "strengths": self._identify_strengths(resume_text),
                "alignment_score": self._calculate_alignment(resume_text, job_description),
                "full_analysis": analysis,
            }
            self._log_complete("Analysis complete")
            return {"status": "success", "analysis": result}
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}

    def _extract_keywords(self, text: str) -> List[str]:
        keywords = [
            "python", "java", "javascript", "sql", "react", "aws", "kubernetes",
            "docker", "machine learning", "tensorflow", "pytorch", "fastapi",
        ]
        return [kw for kw in keywords if kw in text.lower()]

    def _identify_gaps(self, text: str) -> List[str]:
        gaps = []
        lower = text.lower()
        if not any(char.isdigit() for char in text):
            gaps.append("Missing quantifiable metrics/achievements")
        if "project" not in lower:
            gaps.append("No projects mentioned")
        if "certification" not in lower and "certified" not in lower:
            gaps.append("No certifications listed")
        return gaps

    def _identify_strengths(self, text: str) -> List[str]:
        strengths = []
        lower = text.lower()
        if "experience" in lower:
            strengths.append("Clear experience section")
        if "skill" in lower:
            strengths.append("Well-defined skills")
        if any(char.isdigit() for char in text):
            strengths.append("Includes quantifiable data")
        return strengths

    def _calculate_alignment(self, resume: str, job_desc: str) -> float:
        if not job_desc:
            return 0.0
        resume_lower = resume.lower()
        job_words = [w for w in job_desc.lower().split() if len(w) > 3]
        if not job_words:
            return 0.0
        matches = sum(1 for word in job_words if word in resume_lower)
        return round(min(100.0, (matches / len(job_words)) * 100), 1)
