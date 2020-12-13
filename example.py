from discord.ext import commands

from model import InteractionContext
from slash import Slash

bot = commands.Bot(command_prefix="/")
slash = Slash(
    bot,
    client_id=CLIENT_ID,
    token=TOKEN,
    guild_id=GUILD_ID,
)


## Example
@slash.slash(name="wow", description="This is w0w command.")
async def wow(interact: InteractionContext):
    await interact.send(content="asdf", private=True)


bot.run(BOT_TOKEN)
