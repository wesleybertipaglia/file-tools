from abc import ABC, abstractmethod
from engine import tool_type

class ToolCommand(ABC):
    @abstractmethod
    def name(self) -> str:
        """Nome da ação (para exibir no menu)"""
        pass

    @abstractmethod
    def type(self) -> tool_type.ToolType:
        """Tipo da ferramenta (ex: RENAMER, IMAGE...)"""
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """Executa a lógica da ferramenta"""
        pass
