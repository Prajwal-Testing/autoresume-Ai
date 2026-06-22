"""Live logging system for agent operations."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum

from config import LOG_MAX_ITEMS


class LogLevel(Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class AgentLogger:
    def __init__(self, max_logs: int = LOG_MAX_ITEMS):
        self.logs: List[Dict[str, Any]] = []
        self.max_logs = max_logs
        self.active_agents: Dict[str, str] = {}

    def log(
        self,
        agent_name: str,
        message: str,
        level: LogLevel = LogLevel.INFO,
    ) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(
            {
                "timestamp": timestamp,
                "agent": agent_name,
                "message": message,
                "level": level.value,
            }
        )
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

    def agent_running(self, agent_name: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.active_agents[agent_name] = timestamp
        self.log(agent_name, f"{agent_name} Running...", LogLevel.INFO)

    def agent_start(self, agent_name: str) -> None:
        self.agent_running(agent_name)

    def agent_complete(self, agent_name: str, result: str = "") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        if agent_name in self.active_agents:
            del self.active_agents[agent_name]
        suffix = f" {result}" if result else ""
        self.log(agent_name, f"{agent_name} Complete{suffix}", LogLevel.SUCCESS)

    def agent_error(self, agent_name: str, error: str) -> None:
        if agent_name in self.active_agents:
            del self.active_agents[agent_name]
        self.log(agent_name, f"[ERROR] {error}", LogLevel.ERROR)

    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logs

    def get_formatted_logs(self) -> str:
        return "\n".join(
            f"[{log['timestamp']}] {log['agent']}: {log['message']}" for log in self.logs
        )

    def clear(self) -> None:
        self.logs = []
        self.active_agents = {}


_logger: Optional[AgentLogger] = None


def get_logger() -> AgentLogger:
    global _logger
    if _logger is None:
        _logger = AgentLogger()
    return _logger


def set_logger(logger: AgentLogger) -> None:
    global _logger
    _logger = logger
