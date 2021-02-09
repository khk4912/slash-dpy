import inspect
from dataclasses import dataclass
from typing import Callable, Optional, OrderedDict

import aiohttp
import discord
from discord.member import Member
from discord.role import Role
from discord.user import User

from exceptions import InvaildArgument

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
    """
    Model of SlashCommand.

    Attributes
    ----------
    name : str
        Name of SlashCommand
    description : str
        Description of SlashCommand
    options: OrdeeredDict[str, inspect.Parameter]
        Options created based on parameter's annotations.
    func : Callable
        Function covered with slash decorator.
    """

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

        option_type = STRING  # Default
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
    """
    Model of InteractionContext

    Attributes
    ----------
    author : discord.User, optional
        Message's author.
    options : list, optional
        List of options.
    id : int
        ID of interaction.
    token : str
        Token of interaction.
    """

    author: Optional[User]
    options: Optional[list]
    id: int
    token: str

    async def send(
        self,
        content: Optional[str] = None,
        embed: Optional[discord.Embed] = None,
        private: bool = False,
        tts: bool = False,
    ):
        """
        Function that calllback to interaction.

        Parameters
        ----------
        content : str, optional
            Content of message.
        embed : discord.Embed, optional
            Embed.
        private : bool
            Whether to send a message that is visible only to the sender.
            Default is False.
        tts : bool
            Whether to send TTS message. Default is False.
        """
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
