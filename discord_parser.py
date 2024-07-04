import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def fetch_channel_safe(channel_id):
    try:
        return await bot.fetch_channel(channel_id)
    except discord.errors.NotFound:
        print(f"Channel with ID {channel_id} not found.")
    except discord.errors.Forbidden:
        print(f"Bot doesn't have permission to access channel with ID {channel_id}.")
    except discord.errors.HTTPException:
        print(f"An HTTP error occurred while fetching channel with ID {channel_id}.")
    return None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
    print("Servers the bot is in:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
    
    source_channel_id = 123456789  # Replace with your actual source channel ID
    village_channel_id = 987654321  # Replace with your actual village channel ID
    alliance_channel_id = 456789123  # Replace with your actual alliance channel ID
    
    print(f"\nChannel Diagnostics:")
    source_channel = await fetch_channel_safe(source_channel_id)
    village_channel = await fetch_channel_safe(village_channel_id)
    alliance_channel = await fetch_channel_safe(alliance_channel_id)
    
    print(f"Source channel (ID: {source_channel_id}) found: {source_channel is not None}")
    print(f"Village channel (ID: {village_channel_id}) found: {village_channel is not None}")
    print(f"Alliance channel (ID: {alliance_channel_id}) found: {alliance_channel is not None}")
    
    if not (source_channel and village_channel and alliance_channel):
        print("\nNot all channels were found. Please check the following:")
        print("1. Ensure the channel IDs are correct.")
        print("2. Make sure the bot is in the server containing these channels.")
        print("3. Verify that the bot has permissions to view these channels.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    source_channel_id = 123456789  # Replace with your actual source channel ID
    village_channel_id = 987654321  # Replace with your actual village channel ID
    alliance_channel_id = 456789123  # Replace with your actual alliance channel ID

    if message.channel.id == source_channel_id:
        if "<Village>" in message.content:
            village_channel = await fetch_channel_safe(village_channel_id)
            if village_channel:
                await village_channel.send(message.content)
                print(f"Sent message to Village channel: {message.content}")
            else:
                print(f"Failed to send message to Village channel. Channel not found or inaccessible.")
        elif "<Alliance>" in message.content:
            alliance_channel = await fetch_channel_safe(alliance_channel_id)
            if alliance_channel:
                await alliance_channel.send(message.content)
                print(f"Sent message to Alliance channel: {message.content}")
            else:
                print(f"Failed to send message to Alliance channel. Channel not found or inaccessible.")

bot.run('YOUR_BOT_TOKEN')
