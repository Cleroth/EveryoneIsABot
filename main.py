import os
import discord
from dotenv import load_dotenv # for env variables
import aiohttp # for webhook

# ENV
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK = os.getenv('WEBHOOK')

# BOT
class Client(discord.Client):
    async def on_message(self, message: discord.Message):
        author : discord.Member = message.author
        if author.bot or message.content == '':
            return
        if message.channel.name != 'lounge':
            return

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(WEBHOOK,
                                       adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(message.content, username=author.display_name,
                               avatar_url=author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False))
        await message.delete()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

client = Client()
client.run(TOKEN)