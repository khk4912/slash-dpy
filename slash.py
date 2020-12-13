import inspect
from typing import Callable, Dict, List, Optional, OrderedDict, Union

import aiohttp
import requests
from discord.ext import commands
from discord.ext.commands.core import Command

from model import InteractionContext, SlashCommand


class Slash:
    def __init__(
        self,
        bot: Union[commands.Bot, commands.AutoShardedBot],
        client_id: int,
        token: str,
        guild_id: Optional[int] = None,
    ) -> None:
        self.bot = bot
        self.client_id = client_id
        self.__token = token
        self.guild_id = guild_id

        self.bot.add_listener(self.on_socket_response, "on_socket_response")
        self._commands: Dict[str, SlashCommand] = {}

    # decorator
    def slash(self, name: str, description: str):
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

            url = f"https://discord.com/api/v8/interactions/{data['id']}/{data['token']}/callback"

            await self._commands[name].func(
                InteractionContext(
                    author=self.bot.get_user(raw_user),
                    options=options,
                    id=int_id,
                    token=token,
                ),
            )
            # async with aiohttp.ClientSession() as session:
            #     async with session.post(
            #         url,
            #         json=response,
            #         headers={"Authorization": f"Bot {self.__token}"},
            #     ) as resp:
            #         print(resp.status)
            #         print(await resp.text())
