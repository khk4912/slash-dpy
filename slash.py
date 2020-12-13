import inspect
from typing import Callable, Dict, Optional, OrderedDict, Union

import requests
from discord.ext import commands

from model import InteractionContext, SlashCommand


class Slash:
    def __init__(
        self,
        bot: Union[commands.Bot, commands.AutoShardedBot],
        client_id: int,
        token: str,
        guild_id: Optional[int] = None,
    ) -> None:
        """
        Class for Slash commands.

        Attributes
        ----------
        bot : Union[commands.Bot, commands.AutoShardedBot]
            discord.py's Bot Class.
        client_id : int
            Client ID of application.
        toekn : str
            Token of bot.
        guild_id : int, optional
            Guild's ID. If an ID is given, register the slash command only in the
            guild of that ID.

        """
        self.bot = bot
        self.client_id = client_id
        self.__token = token
        self.guild_id = guild_id

        self.bot.add_listener(self.on_socket_response, "on_socket_response")
        self._commands: Dict[str, SlashCommand] = {}

    # decorator
    def slash(self, name: str, description: str):
        """
        Decorator for making slash command.

        Parameters
        ----------
        name : str
            Name of slash command.
        description : str
            Description of slash command.
        """

        def wrapper(func):
            slash_command = self._parse_command_info(
                name=name, description=description, func=func
            )
            print(slash_command)
            self._commands[name] = slash_command
            self._post(data=slash_command.to_dict())
            return func

        return wrapper

    def _parse_command_info(
        self, name: str, description: str, func: Callable
    ) -> SlashCommand:
        return SlashCommand(
            name=name,
            description=description,
            options=OrderedDict(inspect.signature(func).parameters),
            func=func,
        )

    def _post(self, data: dict) -> None:
        client_id = self.client_id
        url = (
            f"https://discord.com/api/v8/applications/{client_id}/commands"
            if self.guild_id is None
            else f"https://discord.com/api/v8/applications/{client_id}/guilds/{self.guild_id}/commands"
        )

        _ = requests.post(
            url=url,
            headers={"Authorization": f"Bot {self.__token}"},
            json=data,
        )
        print(_.text)

    async def on_socket_response(self, msg: dict) -> None:
        if msg["t"] == "INTERACTION_CREATE":
            print(msg)
            data = msg["d"]
            raw_user = data["member"]["user"]["id"]

            options = None
            if "options" in data.keys():
                options = data["options"] or []
            name = data["data"]["name"]
            token = data["token"]
            int_id = data["id"]

            await self._commands[name].func(
                InteractionContext(
                    author=self.bot.get_user(raw_user),
                    options=options,
                    id=int_id,
                    token=token,
                ),
            )
