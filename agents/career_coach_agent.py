"""Career Coach Agent: Provides career development guidance."""
from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent
from config import ROLE_TEMPLATES


class CareerCoachAgent(BaseAgent):
    def __init__(
        self,
        api_key: Optional[str] = None,
        logger=None,
        demo_mode: bool = False,
    ):
        super().__init__("Career Coach Agent", api_key, logger, demo_mode)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._log_start()
        resume_text = input_data.get("resume_text", "")
        target_role = input_data.get("target_role", "AI Engineer")
        role_template = ROLE_TEMPLATES.get(target_role, ROLE_TEMPLATES["AI Engineer"])

        try:
            prompt = f"""Career coach agent: Guide candidate toward {target_role}.

Resume:
{resume_text}

Required keywords: {', '.join(role_template['keywords'])}
Desired skills: {', '.join(role_template['skills'])}

Provide missing skills, projects, certifications, and 30-60-90 day plan."""
            guidance = self._generate(prompt)
            skill_gaps = self._identify_skill_gaps(resume_text, role_template)
            project_suggestions = role_template.get("projects_suggested", [])
            self._log_complete(f"Plan for {target_role}")
            return {
                "status": "success",
                "guidance": guidance,
                "target_role": target_role,
                "skill_gaps": skill_gaps,
                "project_suggestions": project_suggestions,
                "role_keywords": role_template["keywords"],
            }
        except Exception as exc:
            self._log_error(str(exc))
            return {"status": "error", "message": str(exc)}

    def _identify_skill_gaps(self, resume: str, role_template: Dict) -> List[str]:
        lower = resume.lower()
        return [
            skill
            for skill in role_template.get("skills", [])
            if skill.lower() not in lower
        ]
