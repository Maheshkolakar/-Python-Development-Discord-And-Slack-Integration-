import discord
from discord.ext import commands
import mysql.connector

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@1234",
    database="discord_bot_db"
)

# Create a cursor object to interact with the database
db_cursor = db_connection.cursor()

intents = discord.Intents.default()
intents.messages = True  # Enable the message event

# Set up the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def authenticate(ctx):
    # Check if the server is already authenticated
    db_cursor.execute("SELECT * FROM discord_tokens WHERE server_id = %s", (str(ctx.guild.id),))
    result = db_cursor.fetchone()

    if result:
        await ctx.send("Bot is already authenticated for this server.")
    else:
        # Save the token for the current server in the database
        db_cursor.execute("INSERT INTO discord_tokens (server_id, token) VALUES (%s, %s)",
                          (str(ctx.guild.id), "your_discord_bot_token_here"))
        db_connection.commit()
        await ctx.send("Bot authenticated successfully!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        # Replace YOUR_GUILD_ID with the actual ID of your Discord server
        guild = bot.get_guild(1185134192682610760)
        if guild:
            await message.channel.send(f"Hello World {guild.name}")
        else:
            print("Guild not found.")


# Run the bot with your Discord bot token


bot.run('copy your token here')


