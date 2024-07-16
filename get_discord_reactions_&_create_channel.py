# Get ✅ reactions from discord message using /reactions <message_link> and bot responds mentioning everyone that reacted (Should be used in private chat)
# Then use /create_channel <category_id> <Channel_name> <message_link> where the message_link is the link for the message the bot responded with the mentiones users
# Bot will then create the channel and give access to everyone that reacted to the first message
# Set target_channel_id to the private channel id

from discord import app_commands
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role, check

intents = discord.Intents.default()  # Create a default intents object
intents.message_content = True
intents.typing = False
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

target_channel_id = 1179625944756015145

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)\nBot ready!")
    except Exception as e:
        print(e)

@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        return

@bot.tree.command(name="reactions", description='Get reactions')
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator)
async def reactions(ctx, message_link: str):
    await ctx.response.defer()
    # Extracting channel and message IDs from the link
    link_parts = message_link.split('/')
    #print(link_parts)
    if len(link_parts) < 7 or link_parts[3] != 'channels':
        print("Invalid message link format")
        return

    guild_id, channel_id, message_id = link_parts[4], link_parts[5], link_parts[-1]

    #print(f"Guild ID: {guild_id}, Channel ID: {channel_id}, Message ID: {message_id}")

    channel = bot.get_channel(int(channel_id))
    if not channel:
        print("Channel not found")
        await ctx.followup.send("Channel not found")
        return

    try:
        message = await channel.fetch_message(int(message_id))

        target_emoji = '✅'

        # Get the reaction with the specified emoji
        target_reaction = discord.utils.get(message.reactions, emoji=target_emoji)

        if target_reaction:

            reaction_users = set()
            async for user in target_reaction.users():
                reaction_users.add(user)

            target_channel = bot.get_channel(target_channel_id)

            mention_string = ' '.join([user.mention for user in reaction_users])
            await target_channel.send(f'{mention_string}')
            embed = discord.Embed(
                    title=f"Reactions",
                    description=f"Done",
                    color=0x31E75F,  # Red color for cooldown message
                )
            await ctx.followup.send("Done")
        else:
            await ctx.followup.send(f"No reactions found with {target_emoji}")    
    except discord.NotFound:
        print("Message not found")
        return
    except Exception as e:
        print(f"Error in 'reactions' command: {e}")

@bot.tree.command(name="create_channel",description='Create channel with message history')
@commands.check(lambda ctx: ctx.author.guild_permissions.administrator)
async def create_channel(ctx, category_id: str, channel_name: str, message_id: str):
    await ctx.response.defer()

    # Get the category for channel creation
    category = discord.utils.get(ctx.guild.categories, id=int(category_id))
    if not category:
        print(f"Category with ID {category_id} not found")
        await ctx.followup.send(f"Category with ID {category_id} not found")
        return

    # Get the message with allowed users
    try:
        message = await ctx.channel.fetch_message(int(message_id))
    except discord.NotFound:
        print(f"Message with ID {message_id} not found")
        await ctx.followup.send(f"Message with ID {message_id} not found")
        return

    # Create the channel
    try:
        new_channel = await ctx.guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites={
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            },
        )

        # Allow users from the specified message to read the channel
        for user in message.mentions:
            await new_channel.set_permissions(user, read_messages=True, read_message_history=True, send_messages=True)

        await ctx.followup.send(f"Channel '{channel_name}' created successfully")
    except Exception as e:
        print(f"Error creating channel: {e}")
        await ctx.followup.send(f"Error creating channel: {e}")

bot.run('AUTH_TOKEN')
