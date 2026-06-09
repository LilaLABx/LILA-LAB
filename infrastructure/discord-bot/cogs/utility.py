"""Utility Cog.

Commands for contribution guides, resources, and community information.
"""

import discord
from discord.ext import commands
from discord import app_commands

import config


class UtilityCog(commands.Cog):
    """Utility commands for community members."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="contribute", description="Learn how to contribute to LILA Lab")
    async def contribute_command(self, interaction: discord.Interaction):
        """Show contribution options."""
        embed = discord.Embed(
            title="How to Contribute to LILA Lab",
            description=(
                "LILA Lab is a research collective. There are 8 ways to contribute:"
            ),
            color=discord.Color.from_str("#006D77"),
        )

        contributions = [
            (
                "1. Language Extension Paper",
                "Apply BENI to your language, publish a comparative paper.",
                "First-author publication",
            ),
            (
                "2. Cross-Domain Extension",
                "Apply the framework to health, climate, education, or politics.",
                "First-author publication",
            ),
            (
                "3. Methodological Contribution",
                "Improve the classifier, reduce annotation cost, add validation.",
                "Co-authorship",
            ),
            (
                "4. Replication + Validation",
                "Independently reproduce our results.",
                "Replication report",
            ),
            (
                "5. Citizen Science Annotation",
                "Label articles in your native language. No code required.",
                "Acknowledgement",
            ),
            (
                "6. Policy & Application Brief",
                "Use the index for policy analysis in your country.",
                "Co-authorship",
            ),
            (
                "7. Infrastructure & Tooling",
                "Build dashboards, APIs, or mobile apps.",
                "Co-authorship",
            ),
            (
                "8. Teaching Materials",
                "Create tutorials and course modules.",
                "Co-authorship",
            ),
        ]

        for title, desc, credit in contributions:
            embed.add_field(
                name=title,
                value=f"{desc}\n*Credit: {credit}*",
                inline=False,
            )

        embed.add_field(
            name="Getting Started",
            value=(
                f"1. Read the [Collaboration Framework]({config.RESOURCES['collaboration']})\n"
                f"2. Choose a contribution model\n"
                f"3. Record your intent in OWNERS.csv\n"
                f"4. Start contributing!"
            ),
            inline=False,
        )

        embed.set_footer(text="Questions? Ask in #general or email lila.lab0x@gmail.com")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="languages", description="See which languages need speakers")
    async def languages_command(self, interaction: discord.Interaction):
        """Show language priorities."""
        embed = discord.Embed(
            title="Languages We're Working On",
            description="Here are the languages that need native speakers for annotation:",
            color=discord.Color.from_str("#E29578"),
        )

        languages = [
            ("Bangla", "Active", "265M speakers", "BENI pipeline running"),
            ("Assamese", "High Priority", "15M speakers", "No data yet"),
            ("Nepali", "High Priority", "25M speakers", "No data yet"),
            ("Sylheti", "High Priority", "11M speakers", "No data yet"),
            ("Chittagonian", "High Priority", "13M speakers", "No data yet"),
            ("Hindi", "Medium Priority", "600M speakers", "No data yet"),
            ("Maithili", "Medium Priority", "34M speakers", "No data yet"),
            ("Odia", "Medium Priority", "35M speakers", "No data yet"),
        ]

        for lang, priority, speakers, status in languages:
            embed.add_field(
                name=f"{lang} ({speakers})",
                value=f"**Priority:** {priority}\n**Status:** {status}",
                inline=True,
            )

        embed.add_field(
            name="How to Help",
            value=(
                "1. If you speak one of these languages, use `/roles` to add the language role\n"
                "2. Read the [Linguistic Contribution Guide]({config.RESOURCES['linguistic_guide']})\n"
                "3. Submit 1,000+ news articles in your language\n"
                "4. Annotate articles as Economic/Not Economic"
            ),
            inline=False,
        )

        embed.set_footer(text="Your language is underserved by current AI. Let's change that.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="extensions", description="View extension proposals")
    async def extensions_command(self, interaction: discord.Interaction):
        """Show extension proposals and status."""
        embed = discord.Embed(
            title="LILA Lab Extensions",
            description="Current and planned language/domain extensions:",
            color=discord.Color.from_str("#E76F51"),
        )

        # Active extensions
        embed.add_field(
            name="Active Pipelines",
            value=(
                "**BENI** - Bangla Exploration & Native-language Intelligence\n"
                "Status: Active, validated, index published\n"
                "Accuracy: 88.2% on gold-standard annotations"
            ),
            inline=False,
        )

        # Planned extensions
        embed.add_field(
            name="Planned Extensions",
            value=(
                "**AENI** - Assamese Exploration & Native-language Intelligence\n"
                "Status: Seeking contributors\n\n"
                "**NENI** - Nepali Exploration & Native-language Intelligence\n"
                "Status: Seeking contributors\n\n"
                "**SENI** - Sylheti Exploration & Native-language Intelligence\n"
                "Status: Seeking contributors"
            ),
            inline=False,
        )

        # How to propose
        embed.add_field(
            name="Propose a New Extension",
            value=(
                f"1. Read the [Extension Template]({config.RESOURCES['extension_template']})\n"
                "2. Open a GitHub Issue with your proposal\n"
                "3. Join #extensions in Discord to discuss\n"
                "4. Get your language's first economic narrative index!"
            ),
            inline=False,
        )

        embed.set_footer(text="Every new language reveals something about how economic narratives work differently.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="stats", description="Show LILA Lab statistics")
    async def stats_command(self, interaction: discord.Interaction):
        """Show community statistics."""
        guild = interaction.guild

        embed = discord.Embed(
            title="LILA Lab Statistics",
            color=discord.Color.from_str("#006D77"),
        )

        # Member count
        embed.add_field(
            name="Members",
            value=str(guild.member_count),
            inline=True,
        )

        # Channel count
        embed.add_field(
            name="Channels",
            value=str(len(guild.channels)),
            inline=True,
        )

        # Role counts
        role_counts = {}
        for member in guild.members:
            for role in member.roles:
                if role.name != "@everyone":
                    role_counts[role.name] = role_counts.get(role.name, 0) + 1

        # Top roles
        top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_roles:
            role_text = "\n".join([f"**{name}:** {count}" for name, count in top_roles])
            embed.add_field(
                name="Top Roles",
                value=role_text,
                inline=False,
            )

        embed.set_footer(text="LILA Lab | Language Intelligence for Low-resource Applications")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    """Add cog to bot."""
    await bot.add_cog(UtilityCog(bot))
