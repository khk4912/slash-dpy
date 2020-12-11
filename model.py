import inspect
from dataclasses import dataclass
from typing import Optional, OrderedDict

from discord.ext.commands.core import Command
from discord.member import Member
from discord.role import Role
from discord.user import User

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
    command: Command

    def to_dict(self) -> dict:
        data = {}
        options = []

        data["name"] = self.name
        data["description"] = self.description or f"Command {self.name}"

        option_type = None
        required = True

        for name, param in self.options.items():
            annot = param.annotation

            if isinstance(annot, User) or isinstance(annot, Member):
                option_type = USER
            elif isinstance(annot, int):
                option_type = INTEGER
            elif isinstance(annot, str):
                option_type = STRING
            elif isinstance(annot, Role):
                option_type = ROLE
            elif annot == Optional[User] or isinstance == Optional[Member]:
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
