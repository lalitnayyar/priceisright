from abc import ABC, abstractmethod
from app.core.models import AgentStatus
import logging

class Agent(ABC):
    def __init__(self, name: str, role: str, color: str, model: str):
        self.name = name
        self.role = role
        self.color = color
        self.model = model
        self.logger = logging.getLogger(f"agent.{name}")
        self.status = "READY"

    def set_status(self, status: str):
        self.status = status

    def get_status(self) -> AgentStatus:
        return AgentStatus(
            name=self.name,
            role=self.role,
            model=self.model,
            status=self.status
        )

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
