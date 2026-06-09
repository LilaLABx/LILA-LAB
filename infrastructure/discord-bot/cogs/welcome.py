"""Welcome and Onboarding Cog.

Handles new member welcome, role assignment, and onboarding flow.
"""

import discord
from discord.ext import commands
from discord import app_commands

import config


class WelcomeCog(commands.Cog):
    """Welcome and onboarding functionality."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.welcome_channel_id = config.WELCOME_CHANNEL_ID

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle new member joining the server."""
        # Get welcome channel
        channel = member.guild.get_channel(self.welcome_channel_id)
        if not channel:
            return

        # Assign Newcomer role
        newcomer_role = discord.utils.get(member.guild.roles, name=config.ROLES["newcomer"])
        if newcomer_role:
            try:
                await member.add_roles(newcomer_role)
            except discord.Forbidden:
                pass

        # Send welcome message
        welcome_text = config.WELCOME_MESSAGE.format(
            user=member,
            collaboration_channel="collaboration",
            general_channel="general",
            **config.RESOURCES,
        )

        # Create welcome embed
        embed = discord.Embed(
            title=f"Welcome to LILA Lab, {member.display_name}!",
            description=welcome_text,
            color=discord.Color.from_str("#006D77"),  # Deep Teal
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text="LILA Lab | Language Intelligence for Low-resource Applications",
            icon_url="https://avatars.githubusercontent.com/u/00000000",
        )

        await channel.send(embed=embed)

        # Send DM with detailed resources
        try:
            dm_embed = discord.Embed(
                title="Welcome to LILA Lab!",
                description=(
                    "Thank you for joining our research collective! "
                    "Here are some resources to get you started."
                ),
                color=discord.Color.from_str("#E29578"),  # Warm Gold
            )
            dm_embed.add_field(
                name="Getting Started",
                value=(
                    f"1. Read the [Collaboration Framework]({config.RESOURCES['collaboration']})\n"
                    f"2. Check the [Contributing Guide]({config.RESOURCES['contribution_guide']})\n"
                    f"3. If you're a linguist, see the [Linguistic Contribution Guide]({config.RESOURCES['linguistic_guide']})\n"
                    "4. Use `/roles` to assign yourself language and expertise roles"
                ),
                inline=False,
            )
            dm_embed.add_field(
                name="Quick Commands",
                value=(
                    "`/help` - Show all commands\n"
                    "`/roles` - Self-assign roles\n"
                    "`/about` - About LILA Lab\n"
                    "`/resources` - Get resource links"
                ),
                inline=False,
            )
            dm_embed.add_field(
                name="Need Help?",
                value=(
                    "Ask in #general or open a ticket in #support\n"
                    "Email: lila.lab0x@gmail.com"
                ),
                inline=False,
            )

            await member.send(embed=dm_embed)
        except discord.Forbidden:
            # User has DMs disabled
            pass

    @app_commands.command(name="roles", description="Self-assign language and contribution roles")
    async def roles_command(self, interaction: discord.Interaction):
        """Show role selection menu."""
        embed = discord.Embed(
            title="Choose Your Roles",
            description=(
                "Select roles that match your expertise and language skills.\n"
                "Use the dropdowns below to assign roles to yourself."
            ),
            color=discord.Color.from_str("#006D77"),
        )

        # Language roles view
        view = RoleSelectView(
            placeholder="Select your languages",
            roles=config.LANGUAGE_ROLES,
            role_type="language",
        )

        # Contribution roles view
        view2 = RoleSelectView(
            placeholder="Select your expertise",
            roles=config.CONTRIBUTION_ROLES,
            role_type="contribution",
        )

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        # Send second view as followup
        await interaction.followup.send(
            embed=discord.Embed(
                title="Your Expertise",
                description="Select your research/academic background:",
                color=discord.Color.from_str("#E29578"),
            ),
            view=view2,
            ephemeral=True,
        )

    @app_commands.command(name="remove-role", description="Remove a role from yourself")
    @app_commands.describe(role="The role to remove")
    async def remove_role_command(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        """Remove a role from yourself."""
        # Check if role is in the allowed list
        allowed_roles = config.LANGUAGE_ROLES + config.CONTRIBUTION_ROLES
        if role.name not in allowed_roles:
            await interaction.response.send_message(
                "You can only remove language or contribution roles.",
                ephemeral=True,
            )
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"Removed role: {role.name}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"You don't have the role: {role.name}",
                ephemeral=True,
            )


class RoleSelectView(discord.ui.View):
    """Dropdown view for role selection."""

    def __init__(self, placeholder: str, roles: list, role_type: str):
        super().__init__(timeout=180)
        self.role_type = role_type

        # Add select menu
        select = discord.ui.Select(
            placeholder=placeholder,
            min_values=1,
            max_values=len(roles),
            options=[
                discord.SelectOption(label=role, value=role)
                for role in roles
            ],
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        """Handle role selection."""
        selected_roles = interaction.data["values"]
        added = []
        already_has = []

        for role_name in selected_roles:
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role:
                if role in interaction.user.roles:
                    already_has.append(role_name)
                else:
                    try:
                        await interaction.user.add_roles(role)
                        added.append(role_name)
                    except discord.Forbidden:
                        pass

        # Build response
        response_parts = []
        if added:
            response_parts.append(f"**Added:** {', '.join(added)}")
        if already_has:
            response_parts.append(f"**Already have:** {', '.join(already_has)}")

        await interaction.response.send_message(
            "\n".join(response_parts) if response_parts else "No roles changed.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    """Add cog to bot."""
    await bot.add_cog(WelcomeCog(bot))
