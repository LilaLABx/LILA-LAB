"""Issue Tracking Cog.

Syncs GitHub issues to a Discord channel, supports reaction-based claiming,
and provides daily digests of open issues.
"""

import json
import os
from datetime import datetime, time
from pathlib import Path

import aiohttp
import config
import discord
from discord import app_commands
from discord.ext import commands, tasks


class IssueTracking(commands.Cog):
    """Sync GitHub issues to Discord, support claiming, track assignments."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO", "LilaLABx/LILA-LAB")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.github_token}" if self.github_token else None,
        }
        # Track posted issues to avoid duplicates
        self.posted_issues_file = Path(__file__).parent.parent / "data" / "posted_issues.json"
        self.posted_issues = self._load_posted()
        # Track claim intents: message_id -> {issue_number, claimer_id, claimer_name}
        self.claim_intents = {}
        # Ensure startup sync fires once
        self._startup_synced = False

        if self.github_token:
            self.sync_issues_to_channel.start()
            self.daily_digest.start()

    @commands.Cog.listener()
    async def on_ready(self):
        """Trigger an immediate sync when the bot comes online."""
        if self.github_token and not self._startup_synced:
            self._startup_synced = True
            await self.sync_issues_to_channel()

    def _load_posted(self):
        if self.posted_issues_file.exists():
            try:
                return json.loads(self.posted_issues_file.read_text())
            except Exception:
                return []
        return []

    def _save_posted(self):
        self.posted_issues_file.parent.mkdir(parents=True, exist_ok=True)
        self.posted_issues_file.write_text(json.dumps(self.posted_issues, indent=2))

    def cog_unload(self):
        if self.sync_issues_to_channel.is_running():
            self.sync_issues_to_channel.cancel()
        if self.daily_digest.is_running():
            self.daily_digest.cancel()

    @tasks.loop(minutes=30)
    async def sync_issues_to_channel(self):
        """Fetch open issues and post new ones to the issue tracking channel."""
        await self.bot.wait_until_ready()
        if not self.github_token:
            return

        channel = self.bot.get_channel(config.ISSUE_TRACKING_CHANNEL_ID)
        if not channel:
            return

        url = f"https://api.github.com/repos/{self.github_repo}/issues?state=open&per_page=100"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    return
                issues = await resp.json()

        new_count = 0
        for issue in issues:
            if "pull_request" in issue:
                continue
            issue_id = issue["number"]
            if issue_id in self.posted_issues:
                continue

            embed = self._build_issue_embed(issue)
            msg = await channel.send(embed=embed)
            await msg.add_reaction("✋")
            self.posted_issues.append(issue_id)
            self.claim_intents[msg.id] = {
                "issue_number": issue_id,
                "claimer_id": None,
            }
            new_count += 1

        if new_count > 0:
            self._save_posted()
            await channel.send(
                f"📬 **{new_count}** new issue{'s' if new_count > 1 else ''} posted. "
                f"React with ✋ to claim one!"
            )

    @tasks.loop(time=time(hour=9, minute=0))
    async def daily_digest(self):
        """Post a daily summary of open issues to the tracking channel."""
        await self.bot.wait_until_ready()
        if not self.github_token:
            return

        channel = self.bot.get_channel(config.ISSUE_TRACKING_CHANNEL_ID)
        if not channel:
            return

        url = f"https://api.github.com/repos/{self.github_repo}/issues?state=open&per_page=100"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    return
                issues = await resp.json()

        real_issues = [i for i in issues if "pull_request" not in i]
        label_counts = {}
        for i in real_issues:
            for label in i.get("labels", []):
                name = label["name"]
                label_counts[name] = label_counts.get(name, 0) + 1

        unassigned = sum(1 for i in real_issues if not i.get("assignee"))
        label_summary = "\n".join(
            f"• **{name}:** {count}" for name, count in sorted(label_counts.items(), key=lambda x: -x[1])[:8]
        ) or "None"

        embed = discord.Embed(
            title=f"📋 Daily Issue Digest — {len(real_issues)} Open",
            description=(
                f"**Unassigned:** {unassigned}\n"
                f"**Assigned:** {len(real_issues) - unassigned}\n\n"
                f"**Labels:**\n{label_summary}"
            ),
            color=discord.Color.from_str("#006D77"),
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(text="React with ✋ to claim an issue")
        await channel.send(embed=embed)

    @daily_digest.before_loop
    @sync_issues_to_channel.before_loop
    async def before_sync(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Handle ✋ reaction for claiming issues."""
        if payload.guild_id is None:
            return
        if payload.emoji.name != "✋":
            return

        message_id = payload.message_id
        if message_id not in self.claim_intents:
            return

        entry = self.claim_intents[message_id]
        if entry["claimer_id"] is not None:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        issue_number = entry["issue_number"]
        entry["claimer_id"] = payload.user_id

        channel = guild.get_channel(payload.channel_id)
        if not channel:
            return

        try:
            msg = await channel.fetch_message(message_id)
            await msg.remove_reaction("✋", member)
        except Exception:
            pass

        embed = discord.Embed(
            title=f"✋ Issue #{issue_number} Claimed",
            description=(
                f"**{member.display_name}** wants to work on issue **#{issue_number}**.\n"
                f"[View on GitHub](https://github.com/{self.github_repo}/issues/{issue_number})\n\n"
                f"An admin can assign via `/claim {issue_number}` to confirm."
            ),
            color=discord.Color.from_str("#E29578"),
        )
        await channel.send(embed=embed)

    def _build_issue_embed(self, issue):
        labels = issue.get("labels", [])
        label_text = " ".join(
            f"[{l['name']}]" for l in labels[:5]
        ) or "No labels"

        assignee = issue.get("assignee")
        assignee_text = assignee["login"] if assignee else "Unassigned"

        body = (issue.get("body") or "")[:300]
        if body:
            body += "…"

        embed = discord.Embed(
            title=f"#{issue['number']}: {issue['title']}",
            description=body,
            url=issue["html_url"],
            color=discord.Color.from_str("#006D77"),
        )
        embed.add_field(name="Labels", value=label_text, inline=True)
        embed.add_field(name="Assignee", value=assignee_text, inline=True)
        embed.set_footer(text=f"Created {issue['created_at'][:10]} • React ✋ to claim")
        return embed

    @app_commands.command(name="claim", description="Claim a GitHub issue (assigns via API)")
    @app_commands.describe(issue_number="The GitHub issue number to claim")
    async def claim_command(self, interaction: discord.Interaction, issue_number: int):
        """Claim a GitHub issue by assigning it to the caller."""
        if not self.github_token:
            await interaction.response.send_message(
                "GitHub token not configured.", ephemeral=True
            )
            return

        url = f"https://api.github.com/repos/{self.github_repo}/issues/{issue_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    await interaction.response.send_message(
                        f"Issue #{issue_number} not found.", ephemeral=True
                    )
                    return
                issue = await resp.json()

            if issue.get("assignee"):
                await interaction.response.send_message(
                    f"Issue #{issue_number} is already assigned to {issue['assignee']['login']}.",
                    ephemeral=True,
                )
                return

            gh_username = os.getenv("GITHUB_USERNAME") or interaction.user.name
            assign_url = f"https://api.github.com/repos/{self.github_repo}/issues/{issue_number}/assignees"
            async with session.post(
                assign_url,
                headers=self.headers,
                json={"assignees": [gh_username]},
            ) as assign_resp:
                if assign_resp.status in (200, 201):
                    embed = discord.Embed(
                        title=f"✅ Assigned: #{issue_number}",
                        description=(
                            f"**{interaction.user.display_name}** assigned to:\n"
                            f"**{issue['title']}**\n"
                            f"[View Issue]({issue['html_url']})"
                        ),
                        color=discord.Color.from_str("#28a745"),
                    )
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(
                        "Could not auto-assign. An admin may need to grant the bot repo permissions.",
                        ephemeral=True,
                    )

    @app_commands.command(name="sync-issues", description="Force sync all pending GitHub issues to this channel (Admin)")
    @app_commands.default_permissions(administrator=True)
    async def sync_issues_command(self, interaction: discord.Interaction):
        """Manually trigger a full issue sync to the tracking channel."""
        await interaction.response.defer(ephemeral=True)
        if not self.github_token:
            await interaction.followup.send("GitHub token not configured.", ephemeral=True)
            return

        # Clear posted_issues to force re-posting everything
        self.posted_issues.clear()
        self._save_posted()
        await self.sync_issues_to_channel()
        await interaction.followup.send(
            f"✅ Sync complete. Check <#{config.ISSUE_TRACKING_CHANNEL_ID}> for new issues.",
            ephemeral=True,
        )

    @app_commands.command(name="issue-status", description="Get status of a GitHub issue")
    @app_commands.describe(issue_number="The GitHub issue number")
    async def issue_status_command(self, interaction: discord.Interaction, issue_number: int):
        """Show the current status of a specific issue."""
        if not self.github_token:
            await interaction.response.send_message("GitHub token not configured.", ephemeral=True)
            return

        url = f"https://api.github.com/repos/{self.github_repo}/issues/{issue_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    await interaction.response.send_message(
                        f"Issue #{issue_number} not found.", ephemeral=True
                    )
                    return
                issue = await resp.json()

        embed = self._build_issue_embed(issue)
        embed.color = discord.Color.from_str("#E29578")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(IssueTracking(bot))
