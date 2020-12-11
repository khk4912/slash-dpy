from typing import Dict, List, Optional, Union

import requests
from discord.ext import commands
from discord.ext.commands.core import Command

from model import SlashCommand


class Slash:
    def __init__(
        self,
        bot: Union[commands.Bot, commands.AutoShardedBot],
        client_id: int,
        token: str,
        ignore_commands: List[str] = [],
        guild_id: Optional[int] = None,
    ) -> None:
        self.bot = bot
        self.client_id = client_id
        self.__token = token
        self.guild_id = guild_id

        self.ignore_commands = ignore_commands
        self._commands: Dict[str, SlashCommand] = {}

        for i in self.bot.walk_commands():
            if not isinstance(i, Command):
                continue

            if i.qualified_name not in ignore_commands:
                self._commands[i.name] = self._parse_command_info(i)

        self._post()
        self.bot.add_listener(self.on_socket_response, "on_socket_response")

    def _parse_command_info(self, command: Command) -> SlashCommand:
        return SlashCommand(
            name=command.name,
            description=command.brief,
            options=command.clean_params,
            command=command,
        )

    def _post(self) -> None:
        client_id = self.client_id
        url = (
            f"https://discord.com/api/v8/applications/{client_id}/commands"
            if self.guild_id is None
            else f"https://discord.com/api/v8/applications/{client_id}/guilds/{self.guild_id}/commands"
        )

        for i in self._commands.values():
            r = requests.post(
                url=url,
                headers={"Authorization": f"Bot {self.__token}"},
                json=i.to_dict(),
            )

    async def on_socket_response(self, msg: dict) -> None:
        if msg["t"] == "INTERACTION_CREATE":
            name = msg["d"]["data"]["name"]
            pass
