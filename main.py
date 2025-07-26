import os
import discord
from discord.ext import tasks, commands
import requests

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
CHANNEL_NAMES = ["electronics", "sneakers", "gaming", "furniture", "free-stuff", "misc"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if guild:
        for name in CHANNEL_NAMES:
            if not discord.utils.get(guild.text_channels, name=name):
                await guild.create_text_channel(name)
    post_deals.start()

@tasks.loop(minutes=10)
async def post_deals():
    fake_deals = [
        {
            "title": "Xbox Series X - $200",
            "url": "https://example.com/xbox",
            "price": 200,
            "market_price": 350,
            "category": "gaming",
            "profit": 150,
            "image": "https://via.placeholder.com/200"
        }
    ]
    
    for deal in fake_deals:
        channel = discord.utils.get(bot.get_all_channels(), name=deal["category"])
        if channel:
            embed = discord.Embed(
                title=deal["title"],
                url=deal["url"],
                description=f"💰 **Profit:** ${deal['profit']}\n🛒 Price: ${deal['price']} | Market: ${deal['market_price']}",
                color=discord.Color.green()
            )
            embed.set_image(url=deal["image"])
            await channel.send(embed=embed)

bot.run(TOKEN)


