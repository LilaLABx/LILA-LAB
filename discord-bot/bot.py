"""LILA Lab Discord Bot - Main Entry Point.

Language Intelligence for Low-resource Applications
A research collective building NLP infrastructure for underserved languages.
"""

import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands

import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("lila-bot")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    description="LILA Lab Discord Bot",
)


@bot.event
async def on_ready():
    """Bot startup event."""
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guild(s)")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="for researchers | /help",
    )
    await bot.change_presence(activity=activity)


@bot.event
async def on_member_join(member):
    """Handle new member joining."""
    # This is handled by the welcome cog
    pass


@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    """Show help message."""
    await interaction.response.send_message(config.HELP_TEXT, ephemeral=True)


@bot.tree.command(name="about", description="About LILA Lab")
async def about_command(interaction: discord.Interaction):
    """Show about message."""
    text = config.ABOUT_TEXT.format(**config.RESOURCES)
    await interaction.response.send_message(text, ephemeral=True)


@bot.tree.command(name="resources", description="Get contribution resources")
async def resources_command(interaction: discord.Interaction):
    """Show resource links."""
    text = f"""
**LILA Lab Resources**

:page_facing_up: **Collaboration Framework**
{config.RESOURCES['collaboration']}

:page_facing_up: **Contributing Guide**
{config.RESOURCES['contribution_guide']}

:page_facing_up: **Linguistic Contribution Guide**
{config.RESOURCES['linguistic_guide']}

:page_facing_up: **Extension Template**
{config.RESOURCES['extension_template']}

:desktop: **GitHub Repository**
{config.RESOURCES['github']}

:globe_with_meridians: **Website**
{config.RESOURCES['website']}

:books: **OSF Project**
{config.RESOURCES['osf']}

:robot: **Hugging Face**
{config.RESOURCES['huggingface']}
"""
    await interaction.response.send_message(text, ephemeral=True)


async def main():
    """Load cogs and start bot."""
    async with bot:
        # Load cogs
        cogs_dir = Path(__file__).parent / "cogs"
        for cog_file in cogs_dir.glob("*.py"):
            if cog_file.stem.startswith("_"):
                continue
            try:
                await bot.load_extension(f"cogs.{cog_file.stem}")
                logger.info(f"Loaded cog: {cog_file.stem}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_file.stem}: {e}")

        # Start bot
        await bot.start(config.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
