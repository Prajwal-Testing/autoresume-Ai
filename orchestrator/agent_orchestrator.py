"""LangChain-based multi-agent workflow orchestrator."""
import time
from typing import Any, Dict, List, Optional

from agents import (
    AnalyzerAgent,
    ATSAgent,
    CareerCoachAgent,
    CriticAgent,
    FinalizerAgent,
    ImproverAgent,
    ParserAgent,
    RecruiterAgent,
    SolverAgent,
)
from utils.logger import AgentLogger, get_logger, set_logger


class AgentOrchestrator:
    def __init__(
        self,
        api_key: Optional[str] = None,
        demo_mode: bool = False,
    ):
        self.api_key = api_key
        self.demo_mode = demo_mode or not bool(api_key)
        self.logger = AgentLogger()
        set_logger(self.logger)
        self.agents = self._initialize_agents()
        self.results: Dict[str, Any] = {}
        self.execution_times: Dict[str, float] = {}
        self.original_resume_text = ""

    def _initialize_agents(self) -> Dict[str, Any]:
        common = {
            "api_key": self.api_key,
            "logger": self.logger,
            "demo_mode": self.demo_mode,
        }
        return {
            "parser": ParserAgent(**common),
            "analyzer": AnalyzerAgent(**common),
            "ats": ATSAgent(**common),
            "recruiter": RecruiterAgent(**common),
            "critic": CriticAgent(**common),
            "improver": ImproverAgent(**common),
            "solver": SolverAgent(**common),
            "career_coach": CareerCoachAgent(**common),
            "finalizer": FinalizerAgent(**common),
        }

    def process_resume(
        self,
        resume_text: str,
        job_description: Optional[str] = None,
        target_role: str = "AI Engineer",
    ) -> Dict[str, Any]:
        self.logger.clear()
        self.results = {}
        self.execution_times = {}
        self.original_resume_text = resume_text
        job_description = job_description or ""

        self._execute_agent("parser", {"resume_text": resume_text})
        if self.results.get("parser", {}).get("status") != "success":
            return {
                "status": "error",
                "message": "Failed to parse resume",
                "results": self.results,
                "logs": self.logger.get_logs(),
                "execution_times": self.execution_times,
            }

        resume_data = self.results["parser"]["data"]
        shared = {
            "resume_text": resume_text,
            "job_description": job_description,
            "target_role": target_role,
        }

        for agent_name in ["analyzer", "ats", "recruiter", "critic", "improver"]:
            self._execute_agent(agent_name, shared)

        self._execute_agent(
            "solver",
            {
                "resume_data": resume_data,
                "resume_text": resume_text,
                "job_description": job_description,
                "improvements": self.results.get("improver", {}).get("improvements", ""),
            },
        )

        self._execute_agent("career_coach", shared)

        improved_content = self.results.get("solver", {}).get("improved_content", "")
        self._execute_agent(
            "finalizer",
            {
                **shared,
                "improved_content": improved_content,
                "bullet_improvements": self.results.get("improver", {}).get(
                    "bullet_improvements", []
                ),
            },
        )

        return {
            "status": "success",
            "results": self.results,
            "logs": self.logger.get_logs(),
            "execution_times": self.execution_times,
            "original_resume": resume_text,
            "final_resume": self.results.get("finalizer", {}).get("final_resume", resume_text),
        }

    def _execute_agent(self, agent_name: str, input_data: Dict[str, Any]) -> None:
        agent = self.agents.get(agent_name)
        if not agent:
            self.logger.agent_error(agent_name, "Agent not found")
            self.results[agent_name] = {"status": "error", "message": "Agent not found"}
            return

        start = time.time()
        try:
            self.results[agent_name] = agent.execute(input_data)
        except Exception as exc:
            self.logger.agent_error(agent_name, str(exc))
            self.results[agent_name] = {"status": "error", "message": str(exc)}
        self.execution_times[agent_name] = round(time.time() - start, 2)

    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logger.get_logs()

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_agents": len(self.agents),
            "successful": sum(
                1 for result in self.results.values() if result.get("status") == "success"
            ),
            "failed": sum(
                1 for result in self.results.values() if result.get("status") == "error"
            ),
            "total_execution_time": round(sum(self.execution_times.values()), 2),
            "execution_times": self.execution_times,
        }
