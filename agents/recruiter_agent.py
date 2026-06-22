"""Recruiter Agent: Provides recruiter feedback perspective."""
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent


class RecruiterAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Recruiter Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")
        target_role = input_data.get("target_role", "Software Engineer")
        job_description = input_data.get("job_description", "")

        try:
            prompt = f"""Recruiter agent: Review this resume for {target_role}.

Resume:
{resume_text}

Job Description:
{job_description or 'N/A'}

Give first impression, strengths, red flags, callback score, and suggestions."""
            feedback = self._generate(prompt)
            callback_score = self._estimate_callback_likelihood(resume_text)
            self._log_complete(f"Callback likelihood {callback_score}%")
            return {
                "status": "success",
                "feedback": feedback,
                "callback_likelihood": callback_score,
                "target_role": target_role,
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}

    def _estimate_callback_likelihood(self, resume: str) -> int:
        score = 50
        lower = resume.lower()
        if "experience" in lower:
            score += 10
        if any(char.isdigit() for char in resume):
            score += 15
        if "project" in lower:
            score += 10
        if len(resume) > 500:
            score += 5
        return min(95, score)
