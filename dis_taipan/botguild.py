"""

"""
import os

from dis_snek import Snake, Guild, PartialEmoji, Scale

class SelfGuild(Scale):
    def __init__(self, bot: Snake) -> None:
        self.bot = bot

    async def get_server(self) -> Guild:
        for guild in self.bot.guilds:
            if guild.name == self.bot.user.username:
                return guild
        return await self.bot.create_guild(self.bot.user.username)

    async def get_emoji(self, name: str) -> PartialEmoji:
        for emoji in self.bot.emojis:
            if emoji.name == name:
                return emoji
        path = os.path.join('emoji_images', name + '.png')
        if not os.path.exists(path):
            await self._fetch_emoji_image(name, path)
        if not os.path.exists(path):
            raise FileNotFoundError(f'Emoji image {path} not found')

        guild = await self.get_server()
        print(f'Uploading {name} to {guild.name}')
        with open(path, 'rb') as f:
            return await guild.create_custom_emoji(name=name, imagefile=f.read())

    async def _fetch_emoji_image(self, name: str, path: str) -> None:  # noqa
        """Virtual method that can be overridden to fetch an emoji from an external source."""
        ...

def setup(bot: Snake) -> None:
    if not os.path.exists('emoji_images'):
        os.mkdir('emoji_images')
    SelfGuild(bot)
