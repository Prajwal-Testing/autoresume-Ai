"""Optional CrewAI orchestrator wrapper."""
from typing import Any, Dict, Optional

from orchestrator.agent_orchestrator import AgentOrchestrator


class CrewAIOrchestrator:
    """CrewAI-compatible facade that delegates to LangChain orchestrator."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        demo_mode: bool = False,
    ):
        self._delegate = AgentOrchestrator(api_key=api_key, demo_mode=demo_mode)
        self.crew_available = self._check_crewai()

    def _check_crewai(self) -> bool:
        try:
            import crewai  # noqa: F401
            return True
        except ImportError:
            return False

    def process_resume(
        self,
        resume_text: str,
        job_description: Optional[str] = None,
        target_role: str = "AI Engineer",
    ) -> Dict[str, Any]:
        result = self._delegate.process_resume(
            resume_text=resume_text,
            job_description=job_description,
            target_role=target_role,
        )
        result["framework"] = "crewai" if self.crew_available else "crewai-fallback-langchain"
        return result

    def get_logs(self):
        return self._delegate.get_logs()

    def get_summary(self):
        return self._delegate.get_summary()


def create_orchestrator(
    api_key: Optional[str] = None,
    demo_mode: bool = False,
    use_crewai: bool = False,
):
    if use_crewai:
        return CrewAIOrchestrator(api_key=api_key, demo_mode=demo_mode)
    return AgentOrchestrator(api_key=api_key, demo_mode=demo_mode)
