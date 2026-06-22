"""Improver Agent: Suggests specific improvements."""
from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent


class ImproverAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Improver Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")
        job_description = input_data.get("job_description", "")
        target_role = input_data.get("target_role", "")

        try:
            prompt = f"""Improver agent: Provide before/after improvements.

Resume:
{resume_text}

Target role: {target_role}
Job description: {job_description or 'N/A'}

Focus on metrics, action verbs, keyword alignment, and clarity."""
            improvements = self._generate(prompt)
            bullet_improvements = self._generate_bullet_improvements(resume_text)
            self._log_complete(f"{len(bullet_improvements)} bullet improvements")
            return {
                "status": "success",
                "improvements": improvements,
                "bullet_improvements": bullet_improvements,
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}

    def _generate_bullet_improvements(self, resume: str) -> List[Dict[str, str]]:
        lower = resume.lower()
        suggestions = []
        if "managed" in lower:
            suggestions.append(
                {
                    "before": "Managed team",
                    "after": "Led cross-functional team of 8+ engineers",
                    "impact": "More specific and achievement-focused",
                }
            )
        if "worked on" in lower:
            suggestions.append(
                {
                    "before": "Worked on project",
                    "after": "Architected and deployed scalable microservices",
                    "impact": "Shows ownership and technical depth",
                }
            )
        if "responsible for" in lower:
            suggestions.append(
                {
                    "before": "Responsible for feature X",
                    "after": "Designed feature X, improving performance by 40%",
                    "impact": "Active voice with quantifiable results",
                }
            )
        if not suggestions:
            suggestions.append(
                {
                    "before": "Built ML model",
                    "after": "Built ML model improving accuracy by 18% on 2M records",
                    "impact": "Adds measurable business impact",
                }
            )
        return suggestions
