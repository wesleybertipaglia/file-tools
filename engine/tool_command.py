from abc import ABC, abstractmethod
from engine import tool_type

class ToolCommand(ABC):
    @abstractmethod
    def name(self) -> str:
        """Name of the action (to display in the menu)"""
        pass

    @abstractmethod
    def type(self) -> tool_type.ToolType:
        """Type of the tool (e.g., RENAMER, IMAGE...)"""
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """Executes the tool's logic"""
        pass
