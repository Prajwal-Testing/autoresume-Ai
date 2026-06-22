"""Critic Agent: Provides critical evaluation of resume."""
from typing import Any, Dict, List, Optional, Tuple

from agents.base_agent import BaseAgent


class CriticAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Critic Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")

        try:
            prompt = f"""Critic agent: Critically evaluate this resume.

{resume_text}

List weaknesses, vague statements, clichés, and the #1 fix."""
            criticism = self._generate(prompt)
            issues = self._identify_critical_issues(resume_text)
            self._log_complete(f"{len(issues)} issues identified")
            return {
                "status": "success",
                "criticism": criticism,
                "critical_issues": issues,
                "severity_count": self._count_severity(issues),
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}

    def _identify_critical_issues(self, text: str) -> List[Tuple[str, str]]:
        issues = []
        lower = text.lower()
        if text.count("managed") > 3:
            issues.append(("Overused: 'managed'", "Major"))
        if "responsible for" in lower:
            issues.append(("Passive language: 'responsible for'", "Major"))
        if not any(char.isdigit() for char in text):
            issues.append(("No quantifiable metrics", "Critical"))
        if len(text) > 5000:
            issues.append(("Resume too long", "Major"))
        return issues

    def _count_severity(self, issues: List[Tuple[str, str]]) -> Dict[str, int]:
        return {
            "critical": sum(1 for _, sev in issues if sev == "Critical"),
            "major": sum(1 for _, sev in issues if sev == "Major"),
            "minor": sum(1 for _, sev in issues if sev == "Minor"),
        }
