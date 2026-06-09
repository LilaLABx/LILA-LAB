"""Moderation Cog.

Basic moderation tools for server management.
"""

import discord
from discord.ext import commands
from discord import app_commands

import config


class ModerationCog(commands.Cog):
    """Moderation commands for server management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Send announcement to #announcements")
    @app_commands.describe(message="The announcement message")
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def announce_command(self, interaction: discord.Interaction, message: str):
        """Send announcement to announcements channel."""
        channel = interaction.guild.get_channel(config.ANNOUNCEMENTS_CHANNEL_ID)
        if not channel:
            await interaction.response.send_message(
                "Announcements channel not found.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="Announcement",
            description=message,
            color=discord.Color.from_str("#E29578"),  # Warm Gold
        )
        embed.set_footer(
            text=f"Announced by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url,
        )

        await channel.send(embed=embed)
        await interaction.response.send_message(
            f"Announcement sent to {channel.mention}",
            ephemeral=True,
        )

    @app_commands.command(name="pin", description="Pin a message")
    @app_commands.describe(message_id="The message ID to pin")
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def pin_command(self, interaction: discord.Interaction, message_id: str):
        """Pin a message by ID."""
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            await message.pin()
            await interaction.response.send_message(
                f"Message pinned: {message.jump_url}",
                ephemeral=True,
            )
        except discord.NotFound:
            await interaction.response.send_message(
                "Message not found.",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to pin messages.",
                ephemeral=True,
            )

    @app_commands.command(name="cleanup", description="Delete messages (1-100)")
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def cleanup_command(self, interaction: discord.Interaction, amount: int):
        """Delete multiple messages."""
        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "Amount must be between 1 and 100.",
                ephemeral=True,
            )
            return

        # Defer response since this might take a while
        await interaction.response.defer(ephemeral=True)

        # Delete messages
        deleted = 0
        async for message in interaction.channel.history(limit=amount + 1):
            try:
                await message.delete()
                deleted += 1
            except discord.Forbidden:
                pass
            except discord.NotFound:
                pass

        await interaction.followup.send(
            f"Deleted {deleted} messages.",
            ephemeral=True,
        )

    @app_commands.command(name="timeout", description="Timeout a member")
    @app_commands.describe(
        member="The member to timeout",
        duration="Duration in minutes",
        reason="Reason for timeout",
    )
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def timeout_command(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: int,
        reason: str = "No reason provided",
    ):
        """Timeout a member for specified duration."""
        if duration < 1 or duration > 40320:  # Max 28 days
            await interaction.response.send_message(
                "Duration must be between 1 minute and 28 days.",
                ephemeral=True,
            )
            return

        try:
            await member.timeout(
                discord.utils.utcnow() + discord.timedelta(minutes=duration),
                reason=reason,
            )
            await interaction.response.send_message(
                f"{member.mention} has been timed out for {duration} minutes.\nReason: {reason}",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to timeout this member.",
                ephemeral=True,
            )

    @app_commands.command(name="untimeout", description="Remove timeout from a member")
    @app_commands.describe(member="The member to remove timeout from")
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def untimeout_command(self, interaction: discord.Interaction, member: discord.Member):
        """Remove timeout from a member."""
        try:
            await member.timeout(None, reason="Timeout removed by admin")
            await interaction.response.send_message(
                f"Timeout removed from {member.mention}",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to remove timeout from this member.",
                ephemeral=True,
            )

    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.describe(
        member="The member to kick",
        reason="Reason for kick",
    )
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def kick_command(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ):
        """Kick a member from the server."""
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(
                f"{member.mention} has been kicked.\nReason: {reason}",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to kick this member.",
                ephemeral=True,
            )

    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.describe(
        member="The member to ban",
        reason="Reason for ban",
    )
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def ban_command(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ):
        """Ban a member from the server."""
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(
                f"{member.mention} has been banned.\nReason: {reason}",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to ban this member.",
                ephemeral=True,
            )

    @app_commands.command(name="slowmode", description="Set slowmode for current channel")
    @app_commands.describe(seconds="Slowmode delay in seconds (0 to disable)")
    @app_commands.checks.has_role(config.ROLES["admin"])
    async def slowmode_command(self, interaction: discord.Interaction, seconds: int):
        """Set slowmode for the current channel."""
        if seconds < 0 or seconds > 21600:  # Max 6 hours
            await interaction.response.send_message(
                "Slowmode must be between 0 and 21600 seconds (6 hours).",
                ephemeral=True,
            )
            return

        try:
            await interaction.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                await interaction.response.send_message(
                    "Slowmode disabled.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"Slowmode set to {seconds} seconds.",
                    ephemeral=True,
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to change slowmode.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    """Add cog to bot."""
    await bot.add_cog(ModerationCog(bot))
