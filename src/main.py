import logging

import nextcord
import uvloop
from nextcord.ext import commands

from cogs import GameCog, MiscCog
from util import GameDatabase, loaded_settings


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    uvloop.install()

    database = GameDatabase()

    intents = nextcord.Intents.default()
    # noinspection PyDunderSlots,PyUnresolvedReferences
    intents.message_content = True

    bot: commands.Bot = commands.Bot(intents=intents)  # type: ignore

    bot.add_cog(MiscCog(bot))
    bot.add_cog(GameCog(bot, database))

    bot.run(loaded_settings.bot_token)


if __name__ == "__main__":
    main()
