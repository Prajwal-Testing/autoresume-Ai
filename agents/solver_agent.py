"""Solver Agent: Generates improved resume and LaTeX output."""
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from utils.latex_generator import LaTeXGenerator


class SolverAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Solver Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_data = input_data.get("resume_data", {})
        improvements = input_data.get("improvements", "")
        resume_text = input_data.get("resume_text", "")
        job_description = input_data.get("job_description", "")

        try:
            prompt = f"""Solver agent / LaTeX generator: Improve this resume.

Original data:
{resume_data}

Original text:
{resume_text}

Improvements:
{improvements}

Job description:
{job_description or 'N/A'}

Return a polished ATS-friendly resume with stronger bullets and keywords."""
            improved_content = self._generate(prompt)

            latex_source = resume_data if resume_data else {}
            if not latex_source and resume_text:
                latex_code = LaTeXGenerator.generate_latex_from_text(
                    improved_content or resume_text
                )
            else:
                merged = dict(resume_data)
                merged["summary"] = improved_content[:500] if improved_content else merged.get("summary", "")
                latex_code = LaTeXGenerator.generate_latex(merged)

            success, output_path = LaTeXGenerator.compile_pdf(latex_code, "resume_final")
            self._log_complete(f"LaTeX generated (PDF: {success})")
            return {
                "status": "success",
                "improved_content": improved_content,
                "latex_code": latex_code,
                "pdf_available": success,
                "output_path": output_path,
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}
