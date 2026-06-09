"""Contributor Tracking Cog.

Manages contributor records, integrates with OWNERS.csv, and tracks contributions.
"""

import csv
import io
from datetime import datetime
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

import config


class ContributorTracking(commands.Cog):
    """Track contributors and integrate with OWNERS.csv."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.owners_csv_path = Path(__file__).parent.parent.parent / "papers" / "contributions" / "OWNERS.csv"
        self.contributors_db = Path(__file__).parent.parent / "data" / "contributors.json"
        self._load_contributors()

    def _load_contributors(self):
        """Load contributors from OWNERS.csv and local database."""
        self.contributors = {}

        # Load from OWNERS.csv
        if self.owners_csv_path.exists():
            try:
                with open(self.owners_csv_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row.get("name", "").strip()
                        if name:
                            if name not in self.contributors:
                                self.contributors[name] = {
                                    "name": name,
                                    "orcid": row.get("orcid", ""),
                                    "roles": [],
                                    "contributions": [],
                                    "discord_id": None,
                                    "email": None,
                                }
                            self.contributors[name]["roles"].append(row.get("role", ""))
                            self.contributors[name]["contributions"].append({
                                "paper": row.get("paper", ""),
                                "task": row.get("task", ""),
                                "status": row.get("status", ""),
                                "date_started": row.get("date_started", ""),
                                "date_completed": row.get("date_completed", ""),
                            })
            except Exception as e:
                print(f"Error loading OWNERS.csv: {e}")

    def _save_contributors(self):
        """Save contributors to local database."""
        self.contributors_db.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(self.contributors_db, "w") as f:
            json.dump(self.contributors, f, indent=2)

    @app_commands.command(name="register", description="Register as a contributor")
    @app_commands.describe(
        email="Your email address (for notifications)",
        orcid="Your ORCID ID (optional)",
    )
    async def register_command(
        self,
        interaction: discord.Interaction,
        email: str,
        orcid: Optional[str] = None,
    ):
        """Register yourself as a LILA Lab contributor."""
        user = interaction.user
        name = user.display_name

        # Check if already registered
        if name in self.contributors:
            await interaction.response.send_message(
                f"You're already registered! Use `/profile` to view your profile.",
                ephemeral=True,
            )
            return

        # Create contributor record
        self.contributors[name] = {
            "name": name,
            "orcid": orcid or "",
            "discord_id": user.id,
            "email": email,
            "discord_name": user.display_name,
            "registered_at": datetime.utcnow().isoformat(),
            "roles": ["Newcomer"],
            "contributions": [],
        }
        self._save_contributors()

        # Add to OWNERS.csv
        self._add_to_owners_csv(name, orcid, "Contributor", "registration", "registered")

        # Assign Newcomer role
        newcomer_role = discord.utils.get(interaction.guild.roles, name="Newcomer")
        if newcomer_role:
            try:
                await user.add_roles(newcomer_role)
            except discord.Forbidden:
                pass

        # Create welcome embed
        embed = discord.Embed(
            title="Welcome to LILA Lab!",
            description=(
                f"**{name}** has been registered as a contributor.\n\n"
                f"**What's Next:**\n"
                f"1. Read the [Collaboration Framework]({config.RESOURCES['collaboration']})\n"
                f"2. Choose how you want to contribute\n"
                f"3. Use `/tasks` to see available contribution opportunities\n"
                f"4. Start contributing!"
            ),
            color=discord.Color.from_str("#006D77"),
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="Use /profile to view your contributor profile.")

        await interaction.response.send_message(embed=embed)

        # Notify in general channel
        general_channel = interaction.guild.get_channel(config.GENERAL_CHANNEL_ID)
        if general_channel:
            await general_channel.send(
                f"👋 Welcome new contributor: {user.mention}!\n"
                f"Use `/help` to see how to get involved."
            )

    @app_commands.command(name="profile", description="View your contributor profile")
    async def profile_command(self, interaction: discord.Interaction):
        """View your contributor profile."""
        name = interaction.user.display_name

        if name not in self.contributors:
            await interaction.response.send_message(
                "You're not registered yet. Use `/register` to get started.",
                ephemeral=True,
            )
            return

        contributor = self.contributors[name]

        embed = discord.Embed(
            title=f"Contributor Profile: {name}",
            color=discord.Color.from_str("#006D77"),
        )

        # Basic info
        embed.add_field(
            name="Information",
            value=(
                f"**Name:** {contributor['name']}\n"
                f"**ORCID:** {contributor.get('orcid', 'Not set')}\n"
                f"**Email:** {contributor.get('email', 'Not set')}\n"
                f"**Registered:** {contributor.get('registered_at', 'Unknown')[:10]}"
            ),
            inline=False,
        )

        # Roles
        roles = contributor.get("roles", [])
        if roles:
            embed.add_field(
                name="Roles",
                value=", ".join(roles),
                inline=False,
            )

        # Contributions
        contributions = contributor.get("contributions", [])
        if contributions:
            contrib_text = ""
            for c in contributions[:5]:
                status_emoji = "✅" if c["status"] == "completed" else "🔄"
                contrib_text += f"{status_emoji} **{c['paper']}**: {c['task'][:50]}\n"
            embed.add_field(
                name="Contributions",
                value=contrib_text,
                inline=False,
            )

        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="tasks", description="View available contribution tasks")
    async def tasks_command(self, interaction: discord.Interaction):
        """Show available contribution tasks."""
        embed = discord.Embed(
            title="Available Contribution Tasks",
            description="Choose a task that matches your skills and interests.",
            color=discord.Color.from_str("#E29578"),
        )

        tasks = [
            {
                "title": "Assamese Annotation",
                "description": "Label 500 Bangla news articles as Economic/Not Economic",
                "skills": ["Assamese speaker"],
                "effort": "2-3 hours",
                "credit": "Acknowledgement + co-authorship",
            },
            {
                "title": "Nepali Annotation",
                "description": "Label 500 Nepali news articles",
                "skills": ["Nepali speaker"],
                "effort": "2-3 hours",
                "credit": "Acknowledgement + co-authorship",
            },
            {
                "title": "Extension Proposal",
                "description": "Write a proposal for a new language pipeline",
                "skills": ["Research experience", "Language expertise"],
                "effort": "1-2 weeks",
                "credit": "First-author paper",
            },
            {
                "title": "Pipeline Testing",
                "description": "Test BENI pipeline and report bugs",
                "skills": ["Python", "NLP basics"],
                "effort": "1-2 hours",
                "credit": "Acknowledgement",
            },
            {
                "title": "Documentation",
                "description": "Improve documentation or translate guides",
                "skills": ["Writing", "Language skills"],
                "effort": "2-4 hours",
                "credit": "Acknowledgement",
            },
        ]

        for task in tasks:
            embed.add_field(
                name=task["title"],
                value=(
                    f"**Description:** {task['description']}\n"
                    f"**Skills:** {', '.join(task['skills'])}\n"
                    f"**Effort:** {task['effort']}\n"
                    f"**Credit:** {task['credit']}"
                ),
                inline=False,
            )

        embed.set_footer(text="Use /claim-task to claim a task. Use /contribute for more options.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="claim-task", description="Claim a contribution task")
    @app_commands.describe(task="The task you want to claim")
    @app_commands.choices(
        task=[
            app_commands.Choice(name="Assamese Annotation", value="assamese_annotation"),
            app_commands.Choice(name="Nepali Annotation", value="nepali_annotation"),
            app_commands.Choice(name="Extension Proposal", value="extension_proposal"),
            app_commands.Choice(name="Pipeline Testing", value="pipeline_testing"),
            app_commands.Choice(name="Documentation", value="documentation"),
        ]
    )
    async def claim_task_command(
        self,
        interaction: discord.Interaction,
        task: app_commands.Choice[str],
    ):
        """Claim a contribution task."""
        user = interaction.user
        name = user.display_name

        # Ensure user is registered
        if name not in self.contributors:
            await interaction.response.send_message(
                "Please register first using `/register`.",
                ephemeral=True,
            )
            return

        # Create task record
        task_id = f"TASK-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Add to contributor's record
        self.contributors[name]["contributions"].append({
            "paper": task.value,
            "task": task.name,
            "status": "in_progress",
            "date_started": datetime.utcnow().isoformat()[:10],
            "date_completed": "",
            "task_id": task_id,
        })
        self._save_contributors()

        # Create embed
        embed = discord.Embed(
            title="Task Claimed!",
            description=(
                f"**Task:** {task.name}\n"
                f"**Task ID:** {task_id}\n"
                f"**Assigned to:** {user.mention}\n\n"
                f"**Next Steps:**\n"
                f"1. Read the relevant contribution guide\n"
                f"2. Complete the task\n"
                f"3. Submit your work via Pull Request or email\n"
                f"4. Use `/update-task` to mark as complete"
            ),
            color=discord.Color.from_str("#28a745"),
        )

        await interaction.response.send_message(embed=embed)

        # Notify in linguistic-data channel if annotation task
        if "annotation" in task.value:
            linguistic_channel = interaction.guild.get_channel(config.GENERAL_CHANNEL_ID)
            if linguistic_channel:
                await linguistic_channel.send(
                    f"📝 **{user.display_name}** claimed annotation task: {task.name}\n"
                    f"Use `/update-task` when complete."
                )

    @app_commands.command(name="update-task", description="Update task status")
    @app_commands.describe(
        task_id="Your task ID",
        status="New status",
    )
    @app_commands.choices(
        status=[
            app_commands.Choice(name="In Progress", value="in_progress"),
            app_commands.Choice(name="Completed", value="completed"),
            app_commands.Choice(name="Blocked", value="blocked"),
        ]
    )
    async def update_task_command(
        self,
        interaction: discord.Interaction,
        task_id: str,
        status: app_commands.Choice[str],
    ):
        """Update the status of your claimed task."""
        name = interaction.user.display_name

        if name not in self.contributors:
            await interaction.response.send_message(
                "You're not registered.",
                ephemeral=True,
            )
            return

        # Find and update task
        found = False
        for contrib in self.contributors[name]["contributions"]:
            if contrib.get("task_id") == task_id:
                contrib["status"] = status.value
                if status.value == "completed":
                    contrib["date_completed"] = datetime.utcnow().isoformat()[:10]
                found = True
                break

        if not found:
            await interaction.response.send_message(
                f"Task {task_id} not found.",
                ephemeral=True,
            )
            return

        self._save_contributors()

        # Create embed
        status_emoji = "✅" if status.value == "completed" else "🔄" if status.value == "in_progress" else "🚫"
        
        embed = discord.Embed(
            title=f"Task Updated {status_emoji}",
            description=(
                f"**Task ID:** {task_id}\n"
                f"**New Status:** {status.name}\n"
                f"**Updated by:** {interaction.user.mention}"
            ),
            color=discord.Color.from_str("#28a745") if status.value == "completed" else discord.Color.from_str("#006D77"),
        )

        if status.value == "completed":
            embed.add_field(
                name="Thank You!",
                value=(
                    "Your contribution has been recorded.\n"
                    "You'll receive credit in the relevant paper.\n"
                    "Use `/profile` to see your updated record."
                ),
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

        # Notify completion
        if status.value == "completed":
            general_channel = interaction.guild.get_channel(config.GENERAL_CHANNEL_ID)
            if general_channel:
                await general_channel.send(
                    f"🎉 **{interaction.user.display_name}** completed task {task_id}!"
                )

    def _add_to_owners_csv(
        self,
        name: str,
        orcid: str,
        role: str,
        paper: str,
        task: str,
    ):
        """Add a record to OWNERS.csv."""
        try:
            # Read existing content
            existing_rows = []
            if self.owners_csv_path.exists():
                with open(self.owners_csv_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    existing_rows = list(reader)

            # Add new row
            new_row = {
                "name": name,
                "orcid": orcid,
                "role": role,
                "paper": paper,
                "task": task,
                "status": "in_progress",
                "date_started": datetime.utcnow().isoformat()[:10],
                "date_completed": "",
                "notes": "",
            }
            existing_rows.append(new_row)

            # Write back
            with open(self.owners_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "name", "orcid", "role", "paper", "task",
                    "status", "date_started", "date_completed", "notes"
                ])
                writer.writeheader()
                writer.writerows(existing_rows)

        except Exception as e:
            print(f"Error updating OWNERS.csv: {e}")

    @app_commands.command(name="leaderboard", description="View contributor leaderboard")
    async def leaderboard_command(self, interaction: discord.Interaction):
        """Show top contributors."""
        # Sort by number of contributions
        sorted_contributors = sorted(
            self.contributors.values(),
            key=lambda x: len(x.get("contributions", [])),
            reverse=True,
        )

        embed = discord.Embed(
            title="Contributor Leaderboard",
            color=discord.Color.from_str("#E29578"),
        )

        # Top 10 contributors
        for i, contrib in enumerate(sorted_contributors[:10], 1):
            num_contributions = len(contrib.get("contributions", []))
            completed = sum(
                1 for c in contrib.get("contributions", [])
                if c.get("status") == "completed"
            )
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            
            embed.add_field(
                name=f"{medal} {contrib['name']}",
                value=(
                    f"**Contributions:** {num_contributions}\n"
                    f"**Completed:** {completed}"
                ),
                inline=True,
            )

        if not sorted_contributors:
            embed.description = "No contributors yet. Be the first to register!"

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    """Add cog to bot."""
    await bot.add_cog(ContributorTracking(bot))
