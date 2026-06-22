"""Finalizer Agent: Quality assurance and final resume assembly."""
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent


class FinalizerAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Finalizer Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")
        improved_content = input_data.get("improved_content", "")
        job_description = input_data.get("job_description", "")
        target_role = input_data.get("target_role", "AI Engineer")
        bullet_improvements = input_data.get("bullet_improvements", [])

        try:
            prompt = f"""Finalizer agent: Produce the final ATS-ready resume.

Original:
{resume_text}

Draft improvements:
{improved_content}

Role: {target_role}
Job description: {job_description or 'N/A'}

Polish formatting, ensure keyword alignment, and return the complete final resume text."""
            final_resume = self._generate(prompt)
            if not final_resume or final_resume.startswith("Error:"):
                final_resume = self._build_fallback(resume_text, improved_content, bullet_improvements)

            quality_score = self._quality_score(final_resume, job_description)
            self._log_complete(f"Quality score {quality_score}/100")
            return {
                "status": "success",
                "final_resume": final_resume.strip(),
                "quality_score": quality_score,
                "ready_for_download": True,
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}

    def _build_fallback(
        self,
        original: str,
        improved: str,
        bullet_improvements: list,
    ) -> str:
        sections = [improved.strip()] if improved.strip() else []
        if bullet_improvements:
            sections.append("\nKEY IMPROVEMENTS:")
            for item in bullet_improvements[:5]:
                sections.append(f"- {item.get('after', '')}")
        if not sections:
            return original
        header = original.split("\n")[0] if original else "PROFESSIONAL RESUME"
        return f"{header}\n\n" + "\n".join(sections)

    def _quality_score(self, resume: str, job_description: str) -> int:
        score = 60
        if any(char.isdigit() for char in resume):
            score += 10
        if len(resume) > 400:
            score += 10
        if "experience" in resume.lower():
            score += 10
        if job_description:
            job_words = [w for w in job_description.lower().split() if len(w) > 4]
            matches = sum(1 for w in job_words if w in resume.lower())
            score += min(10, matches // 5)
        return min(100, score)
