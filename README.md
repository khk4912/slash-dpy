## Example

```py
from slash import Slash
from model import InteractionContext
from discord.ext import commands


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
```
![6uFpCde6V9](https://user-images.githubusercontent.com/30457148/102010648-c4b26300-3d82-11eb-8a55-66b8a107677c.gif)
