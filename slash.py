import inspect
from typing import Callable, Dict, Optional, OrderedDict, Union
from discord.client import Client

import requests
from discord.ext import commands
from model import InteractionContext, SlashCommand


class Slash:
    def __init__(
        self,
        bot: Union[commands.Bot, commands.AutoShardedBot],
        client_id: int,
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

        guild_id : int, optional
            Guild's ID. If an ID is given, register the slash command only in the
            guild of that ID.

        """
        self.bot = bot
        self.client_id = client_id
        self.guild_id = guild_id

    # decorator
