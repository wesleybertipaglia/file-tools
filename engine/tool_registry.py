from typing import Dict, List
from engine import tool_command
from engine import tool_type

_COMMANDS: Dict[tool_type.ToolType, Dict[str, tool_command.ToolCommand]] = {}

def register_command(key: str, command: tool_command.ToolCommand):
    tool_type = command.type()

    if tool_type not in _COMMANDS:
        _COMMANDS[tool_type] = {}
    _COMMANDS[tool_type][key] = command

def get_commands_by_type(tool_type: tool_type.ToolType) -> Dict[str, tool_command.ToolCommand]:
    return _COMMANDS.get(tool_type, {})

def get_all_commands() -> List[tool_command.ToolCommand]:
    all_commands = []
    for cmds in _COMMANDS.values():
        all_commands.extend(cmds.values())
    return all_commands
