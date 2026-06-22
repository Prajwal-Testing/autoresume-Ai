"""Base agent class for all specialized agents."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from utils.api_client import GeminiClient
from utils.logger import AgentLogger, get_logger


class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        api_key: Optional[str] = None,
        logger: Optional[AgentLogger] = None,
        demo_mode: bool = False,
    ):
        self.name = name
        self.logger = logger or get_logger()
        self.client = GeminiClient(api_key=api_key, demo_mode=demo_mode)
        self.result: Optional[Dict[str, Any]] = None

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def _log_start(self) -> None:
        self.logger.agent_running(self.name)

    def _log_complete(self, message: str = "") -> None:
        self.logger.agent_complete(self.name, message)

    def _log_error(self, error: str) -> None:
        self.logger.agent_error(self.name, error)

    def _generate(self, prompt: str) -> str:
        return self.client.generate(prompt)
