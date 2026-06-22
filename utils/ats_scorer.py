"""ATS scoring and analysis."""
import re
from typing import Dict, List, Optional

from config import ATS_SECTIONS, ATS_WEIGHTS


class ATSScorer:
    ATS_BLOCKERS = ["image", "graphic", "table", "custom format"]
    KEYWORDS_DATABASE = {
        "skills": [
            "python", "java", "sql", "javascript", "react", "aws",
            "kubernetes", "docker",
        ],
        "metrics": [
            "increased", "improved", "reduced", "optimized",
            "streamlined", "achieved",
        ],
        "technical": [
            "api", "database", "algorithm", "architecture",
            "deployment", "pipeline",
        ],
        "soft_skills": [
            "leadership", "collaboration", "communication",
            "teamwork", "problem-solving",
        ],
    }

    @staticmethod
    def score_resume(
        resume_text: str,
        job_description: Optional[str] = None,
    ) -> Dict:
        scores = {
            "format": ATSScorer._score_format(resume_text),
            "keywords": ATSScorer._score_keywords(resume_text, job_description),
            "structure": ATSScorer._score_structure(resume_text),
            "clarity": ATSScorer._score_clarity(resume_text),
            "blockers": ATSScorer._check_blockers(resume_text),
        }

        section_scores = ATSScorer._section_breakdown(resume_text)

        overall = int(
            scores["format"] * 0.2
            + scores["keywords"] * 0.35
            + scores["structure"] * 0.2
            + scores["clarity"] * 0.15
            + (100 - scores["blockers"]) * 0.1
        )

        return {
            "overall": overall,
            "breakdown": scores,
            "section_scores": section_scores,
            "recommendations": ATSScorer._get_recommendations(scores),
        }

    @staticmethod
    def _section_breakdown(text: str) -> Dict[str, int]:
        lower = text.lower()
        mapping = {
            "header": any(x in lower for x in ["@", "phone", "linkedin"]),
            "summary": "summary" in lower or "objective" in lower,
            "experience": "experience" in lower,
            "skills": "skill" in lower,
            "education": "education" in lower,
            "projects": "project" in lower,
        }
        result = {}
        for section in ATS_SECTIONS:
            weight = ATS_WEIGHTS.get(section, 10)
            present = mapping.get(section, False)
            result[section] = weight * 10 if present else max(20, weight * 4)
        return result

    @staticmethod
    def _score_format(text: str) -> int:
        score = 100
        if len(text) > 5000:
            score -= 10
        if text.count("\n") < 5:
            score -= 15
        return max(0, score)

    @staticmethod
    def _score_keywords(text: str, job_description: Optional[str]) -> int:
        text_lower = text.lower()
        count = 0
        for keywords in ATSScorer.KEYWORDS_DATABASE.values():
            for keyword in keywords:
                if keyword in text_lower:
                    count += 1

        if job_description:
            job_words = set(re.findall(r"[a-zA-Z]{4,}", job_description.lower()))
            matches = sum(1 for word in job_words if word in text_lower)
            jd_bonus = min(30, int((matches / max(len(job_words), 1)) * 30))
            base = min(70, int((count / 15) * 70))
            return min(100, base + jd_bonus)

        return min(100, int((count / 15) * 100))

    @staticmethod
    def _score_structure(text: str) -> int:
        score = 60
        for section in ["experience", "skills", "education", "project"]:
            if section in text.lower():
                score += 10
        return min(100, score)

    @staticmethod
    def _score_clarity(text: str) -> int:
        lines = [line for line in text.split("\n") if line.strip()]
        if not lines:
            return 40
        avg_len = sum(len(line) for line in lines) / len(lines)
        score = 70
        if 40 < avg_len < 110:
            score += 15
        if any(char.isdigit() for char in text):
            score += 15
        return min(100, score)

    @staticmethod
    def _check_blockers(text: str) -> int:
        score = 0
        lower = text.lower()
        for blocker in ATSScorer.ATS_BLOCKERS:
            if blocker in lower:
                score += 25
        return min(100, score)

    @staticmethod
    def _get_recommendations(scores: Dict) -> List[str]:
        recs = []
        if scores["format"] < 80:
            recs.append("Ensure consistent formatting and clean structure")
        if scores["keywords"] < 70:
            recs.append("Add more technical keywords matching the job description")
        if scores["structure"] < 80:
            recs.append("Include Experience, Skills, Education, and Projects sections")
        if scores["clarity"] < 75:
            recs.append("Add quantifiable metrics (numbers, percentages, results)")
        if scores["blockers"] > 20:
            recs.append("Remove complex formatting, images, or tables")
        return recs
