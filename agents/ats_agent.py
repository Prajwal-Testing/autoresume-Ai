"""ATS Agent: Scores resume against ATS requirements."""
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from utils.ats_scorer import ATSScorer


class ATSAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("ATS Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")
        job_description = input_data.get("job_description", "")

        try:
            ats_result = ATSScorer.score_resume(resume_text, job_description or None)
            prompt = f"""ATS agent: Provide detailed ATS analysis.

Resume:
{resume_text}

Job Description:
{job_description or 'N/A'}"""
            detailed_analysis = self._generate(prompt)
            self._log_complete(f"Score {ats_result['overall']}/100")
            return {
                "status": "success",
                "ats_score": ats_result["overall"],
                "breakdown": ats_result["breakdown"],
                "section_scores": ats_result["section_scores"],
                "recommendations": ats_result["recommendations"],
                "detailed_analysis": detailed_analysis,
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}
