from typing import Dict, List, Optional
import discord
from discord.ext import commands
from functools import wraps


class Slash:
    def __init__(self, ignore_names: Optional[List[str]]) -> None:
        self.ignore_names = ignore_names

    def _parse_command_info(self, command: commands.Command) -> None:
        pass

    def _post(self, url, info:Dict[str, str) -> None:
        pass

