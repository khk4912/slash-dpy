from exceptions import InvaildArgument
import inspect
from dataclasses import dataclass
from typing import Callable, Optional, OrderedDict

import discord
from discord.member import Member
from discord.role import Role
from discord.user import User

import aiohttp

SUB_COMMAND = 1
SUB_COMMAND_GROUP = 2
STRING = 3
INTEGER = 4
BOOLEAN = 5
USER = 6
CHANNEL = 7
ROLE = 8


@dataclass
class SlashCommand:
    name: str
    description: Optional[str]
    options: OrderedDict[str, inspect.Parameter]
    func: Callable

    def to_dict(self) -> dict:
        self.options.popitem(last=False)
        data = {}
        options = []

        data["name"] = self.name
        data["description"] = self.description or f"Command {self.name}"

        option_type = None
        required = True

        for name, param in self.options.items():
            annot = param.annotation
            if annot == User or annot == Member:
                option_type = USER
            elif annot == int:
                option_type = INTEGER
            elif annot == str:
                option_type = STRING
            elif annot == Role:
                option_type = ROLE
            elif annot == Optional[User] or annot == Optional[Member]:
                option_type = USER
                required = False
            elif annot == Optional[int]:
                option_type = INTEGER
                required = False
            elif annot == Optional[str]:
                option_type = STRING
                required = False
            elif annot == Optional[Role]:
                option_type = ROLE
                required = False
            options.append(
                {
                    "name": name,
                    "description": f"Param {name}",
                    "type": option_type,
                    "required": required,
                }
            )

        data["options"] = options
        print(data)
        return data


@dataclass
class InteractionContext:
    author: User
    options: Optional[dict]
    id: int
    token: str

    async def send(
        self,
        content: Optional[str] = None,
        embed: Optional[discord.Embed] = None,
        private: bool = False,
        tts: bool = False,
    ):
        embeds = []
        if content is None and embed is None:
            raise InvaildArgument("Both content and embeds are None.")

        if embed is not None:
            embeds.append(embed.to_dict())

        data = {
            "type": 4,
            "data": {
                "tts": tts,
                "content": content,
                "embeds": embeds,
            },
        }

        if private:
            data["data"]["flags"] = 64

        url = f"https://discord.com/api/v8/interactions/{self.id}/{self.token}/callback"
        headers = {"Authorization": f"Bot {self.token}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as r:
                c = await r.text()
                print(c)
