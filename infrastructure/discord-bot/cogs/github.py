"""GitHub Integration Cog.

Tracks issues, PRs, contributors, and syncs with GitHub repository.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import aiohttp

logger = logging.getLogger("lila-bot.github")
import config
import discord
from discord import app_commands
from discord.ext import commands, tasks


class GitHubIntegration(commands.Cog):
    """GitHub integration for tracking contributions and repository activity."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO", "LilaLABx/LILA-LAB")
        self.owners_csv_path = Path(__file__).parent.parent.parent / "papers" / "contributions" / "OWNERS.csv"
        self.contributors_cache = {}
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.github_token}" if self.github_token else None,
        }
        # Start background task to sync GitHub data
        if self.github_token:
            self.sync_github.start()

        self.pr_store_file = Path(__file__).parent.parent / "data" / "posted_prs.json"
        self.pr_store: dict[str, str] = {}
        self.pr_messages: dict[int, int] = {}
        self._load_pr_store()
        # PR role name for pings
        self.pr_role_name = os.getenv("PR_NOTIFICATION_ROLE", "PR Notification")

        if self.github_token:
            self.sync_prs_to_channel.start()

    def _load_pr_store(self):
        """Load PR store with auto-migration from v1 flat list."""
        path = self.pr_store_file
        if not path.exists():
            return
        try:
            raw = json.loads(path.read_text())
        except Exception:
            logger.warning("PR store corrupt — starting fresh")
            return

        if isinstance(raw, list):
            logger.info("Migrating PR store from v1 (flat list) to v2")
            self.pr_store = {str(i): "UNVERIFIED" for i in raw}
            self._save_pr_store()
            return

        if isinstance(raw, dict) and "prs" in raw:
            self.pr_store = raw["prs"]
            return

    def _save_pr_store(self):
        self.pr_store_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.pr_store_file.with_suffix(".tmp")
        tmp.write_text(json.dumps({"version": 2, "prs": self.pr_store}, indent=2))
        tmp.rename(self.pr_store_file)

    def cog_unload(self):
        """Cleanup when cog is unloaded."""
        self._save_pr_store()
        if self.sync_github.is_running():
            self.sync_github.cancel()
        if hasattr(self, "sync_prs_to_channel") and self.sync_prs_to_channel.is_running():
            self.sync_prs_to_channel.cancel()

    @tasks.loop(hours=1)
    async def sync_github(self):
        """Sync GitHub issues and PRs every hour."""
        await self._sync_issues()
        await self._sync_prs()
        await self._sync_contributors()

    async def _sync_issues(self):
        """Fetch and cache open issues."""
        if not self.github_token:
            return

        url = f"https://api.github.com/repos/{self.github_repo}/issues?state=open"
        async with aiohttp.ClientSession() as session, session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    issues = await response.json()
                    self.issues_cache = [
                        {
                            "number": i["number"],
                            "title": i["title"],
                            "labels": [l["name"] for l in i["labels"]],
                            "assignee": i["assignee"]["login"] if i["assignee"] else None,
                            "created_at": i["created_at"],
                            "url": i["html_url"],
                        }
                        for i in issues if "pull_request" not in i
                    ]

    async def _sync_prs(self):
        """Fetch and cache open PRs."""
        if not self.github_token:
            return

        url = f"https://api.github.com/repos/{self.github_repo}/pulls?state=open"
        async with aiohttp.ClientSession() as session, session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    prs = await response.json()
                    self.prs_cache = [
                        {
                            "number": pr["number"],
                            "title": pr["title"],
                            "user": pr["user"]["login"],
                            "created_at": pr["created_at"],
                            "url": pr["html_url"],
                        }
                        for pr in prs
                    ]

    async def _sync_contributors(self):
        """Sync contributors from GitHub."""
        if not self.github_token:
            return

        url = f"https://api.github.com/repos/{self.github_repo}/contributors"
        async with aiohttp.ClientSession() as session, session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    contributors = await response.json()
                    self.contributors_cache = {
                        c["login"]: {
                            "contributions": c["contributions"],
                            "avatar": c["avatar_url"],
                            "profile": c["html_url"],
                        }
                        for c in contributors
                    }

    @tasks.loop(minutes=15)
    async def sync_prs_to_channel(self):
        """Check for new PRs and post to PR review channel with role ping."""
        await self.bot.wait_until_ready()
        if not self.github_token:
            return

        channel = self.bot.get_channel(config.PR_REVIEW_CHANNEL_ID)
        if not channel:
            return

        url = f"https://api.github.com/repos/{self.github_repo}/pulls?state=open&per_page=50"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    return
                prs = await resp.json()

        for pr in prs:
            pr_number = str(pr["number"])
            if pr_number in self.pr_store and self.pr_store[pr_number] != "UNVERIFIED":
                continue

            requested = pr.get("requested_reviewers", [])
            reviewer_names = [r["login"] for r in requested]
            reviewer_text = ", ".join(f"`{n}`" for n in reviewer_names) if reviewer_names else "None yet"

            embed = discord.Embed(
                title=f"🔀 PR #{pr_number}: {pr['title']}",
                url=pr["html_url"],
                color=discord.Color.from_str("#28a745"),
            )
            embed.add_field(
                name="Author", value=f"`{pr['user']['login']}`", inline=True
            )
            embed.add_field(
                name="Status",
                value="Draft" if pr.get("draft") else "Ready for Review",
                inline=True,
            )
            embed.add_field(
                name="Requested Reviewers",
                value=reviewer_text,
                inline=False,
            )
            embed.add_field(
                name="Description",
                value=(pr.get("body") or "_No description_")[:200],
                inline=False,
            )
            embed.set_footer(text=f"Created {pr['created_at'][:10]} • React ✅ to approve, ❌ to request changes")

            role = discord.utils.get(channel.guild.roles, name=self.pr_role_name)
            ping = role.mention if role else "@here"
            try:
                msg = await channel.send(
                    content=f"{ping} New PR ready for review!",
                    embed=embed,
                )
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")
            except discord.HTTPException as exc:
                logger.error("Failed to post PR #%s: %s", pr_number, exc)
                continue

            self.pr_store[pr_number] = str(msg.id)
            self.pr_messages[msg.id] = int(pr_number)
            self._save_pr_store()
            logger.info("Posted PR #%s → message %s", pr_number, msg.id)

    async def _verify_pr_messages_on_startup(self):
        """Verify stored PR messages still exist. Remove stale entries."""
        channel = self.bot.get_channel(config.PR_REVIEW_CHANNEL_ID)
        if not channel:
            return

        stale = []
        for pr_num_str, msg_id_str in self.pr_store.items():
            if msg_id_str == "UNVERIFIED":
                stale.append(pr_num_str)
                continue
            try:
                msg = await channel.fetch_message(int(msg_id_str))
                self.pr_messages[msg.id] = int(pr_num_str)
            except discord.NotFound:
                stale.append(pr_num_str)
            except discord.HTTPException:
                pass  # skip on transient errors

        if stale:
            for k in stale:
                self.pr_store.pop(k, None)
            self._save_pr_store()
            logger.info("Removed %d stale PR entries from store", len(stale))

    @sync_prs_to_channel.before_loop
    async def before_pr_sync(self):
        await self.bot.wait_until_ready()
        await self._verify_pr_messages_on_startup()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Handle ✅/❌ reactions on PR review messages."""
        if payload.guild_id is None:
            return
        if payload.emoji.name not in ("✅", "❌"):
            return
        if payload.message_id not in self.pr_messages:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        pr_number = self.pr_messages[payload.message_id]
        channel = guild.get_channel(payload.channel_id)
        if not channel:
            return

        label = "approved" if payload.emoji.name == "✅" else "requested changes"
        await channel.send(
            f"🗳 **{member.display_name}** {label} on PR **#{pr_number}** "
            f"([View PR](https://github.com/{self.github_repo}/pull/{pr_number}))"
        )

    @app_commands.command(name="github", description="GitHub repository information")
    async def github_command(self, interaction: discord.Interaction):
        """Show GitHub repo info and quick links."""
        embed = discord.Embed(
            title="LILA Lab GitHub Repository",
            description=f"**Repository:** [{self.github_repo}](https://github.com/{self.github_repo})",
            color=discord.Color.from_str("#24292e"),  # GitHub dark
        )

        # Repo stats
        if self.contributors_cache:
            total_contributions = sum(c["contributions"] for c in self.contributors_cache.values())
            embed.add_field(
                name="Repository Stats",
                value=(
                    f"**Contributors:** {len(self.contributors_cache)}\n"
                    f"**Total Contributions:** {total_contributions}\n"
                    f"**Open Issues:** {len(getattr(self, 'issues_cache', []))}\n"
                    f"**Open PRs:** {len(getattr(self, 'prs_cache', []))}"
                ),
                inline=False,
            )

        # Quick links
        embed.add_field(
            name="Quick Links",
            value=(
                f"📦 [Repository](https://github.com/{self.github_repo})\n"
                f"🐛 [Issues](https://github.com/{self.github_repo}/issues)\n"
                f"🔀 [Pull Requests](https://github.com/{self.github_repo}/pulls)\n"
                f"📄 [Contributing Guide](https://github.com/{self.github_repo}/blob/main/CONTRIBUTING.md)\n"
                f"🤝 [Collaboration Framework](https://github.com/{self.github_repo}/blob/main/COLLABORATION.md)"
            ),
            inline=False,
        )

        # Contribution types
        embed.add_field(
            name="How to Contribute",
            value=(
                "1. **Fork** the repository\n"
                "2. **Create** a feature branch\n"
                "3. **Make** your changes\n"
                "4. **Submit** a Pull Request\n\n"
                "Use `/contribute` for detailed contribution models."
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="issues", description="View open GitHub issues")
    @app_commands.describe(label="Filter by label (extension, bug, contribution, question)")
    async def issues_command(self, interaction: discord.Interaction, label: str | None = None):
        """Show open issues with optional label filter."""
        issues = getattr(self, "issues_cache", [])

        if label:
            issues = [i for i in issues if label.lower() in [l.lower() for l in i["labels"]]]

        if not issues:
            await interaction.response.send_message(
                "No open issues found." + (f" (filtered by label: {label})" if label else ""),
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"Open Issues ({len(issues)})",
            color=discord.Color.from_str("#006D77"),
        )

        # Show top 10 issues
        for issue in issues[:10]:
            labels = ", ".join(issue["labels"][:3]) if issue["labels"] else "No labels"
            assignee = issue["assignee"] or "Unassigned"
            embed.add_field(
                name=f"#{issue['number']}: {issue['title'][:50]}",
                value=(
                    f"**Labels:** {labels}\n"
                    f"**Assignee:** {assignee}\n"
                    f"[View Issue]({issue['url']})"
                ),
                inline=False,
            )

        if len(issues) > 10:
            embed.set_footer(text=f"Showing 10 of {len(issues)} issues. View all on GitHub.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="prs", description="View open Pull Requests")
    async def prs_command(self, interaction: discord.Interaction):
        """Show open pull requests."""
        prs = getattr(self, "prs_cache", [])

        if not prs:
            await interaction.response.send_message("No open pull requests.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Open Pull Requests ({len(prs)})",
            color=discord.Color.from_str("#28a745"),  # GitHub green
        )

        for pr in prs[:10]:
            embed.add_field(
                name=f"#{pr['number']}: {pr['title'][:50]}",
                value=(
                    f"**Author:** {pr['user']}\n"
                    f"[View PR]({pr['url']})"
                ),
                inline=False,
            )

        if len(prs) > 10:
            embed.set_footer(text=f"Showing 10 of {len(prs)} PRs. View all on GitHub.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="contributors", description="View repository contributors")
    async def contributors_command(self, interaction: discord.Interaction):
        """Show top contributors."""
        if not self.contributors_cache:
            await interaction.response.send_message(
                "Contributors data not available. GitHub token may not be configured.",
                ephemeral=True,
            )
            return

        # Sort by contributions
        sorted_contributors = sorted(
            self.contributors_cache.items(),
            key=lambda x: x[1]["contributions"],
            reverse=True,
        )

        embed = discord.Embed(
            title="LILA Lab Contributors",
            color=discord.Color.from_str("#E29578"),  # Warm Gold
        )

        # Top 10 contributors
        for username, data in sorted_contributors[:10]:
            embed.add_field(
                name=username,
                value=(
                    f"**Contributions:** {data['contributions']}\n"
                    f"[Profile]({data['profile']})"
                ),
                inline=True,
            )

        embed.set_footer(text="Thank you to all contributors!")
        await interaction.response.send_message(embed=embed, ephemeral=True)




class TicketSystem(commands.Cog):
    """Ticket management system for contributor support."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tickets = {}  # ticket_id -> ticket_data
        self.ticket_counter = 0
        self.tickets_file = Path(__file__).parent.parent / "data" / "tickets.json"
        self._load_tickets()

    def _load_tickets(self):
        """Load tickets from file."""
        if self.tickets_file.exists():
            try:
                with open(self.tickets_file) as f:
                    data = json.load(f)
                    self.tickets = data.get("tickets", {})
                    self.ticket_counter = data.get("counter", 0)
            except Exception:
                self.tickets = {}
                self.ticket_counter = 0

    def _save_tickets(self):
        """Save tickets to file."""
        self.tickets_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tickets_file, "w") as f:
            json.dump(
                {
                    "tickets": self.tickets,
                    "counter": self.ticket_counter,
                },
                f,
                indent=2,
            )

    @app_commands.command(name="ticket", description="Create a support ticket")
    @app_commands.describe(
        title="Ticket title",
        description="Describe your question or issue",
        category="Ticket category",
    )
    @app_commands.choices(
        category=[
            app_commands.Choice(name="Contribution Help", value="contribution"),
            app_commands.Choice(name="Language Data", value="language"),
            app_commands.Choice(name="Pipeline Setup", value="pipeline"),
            app_commands.Choice(name="Paper/Writing", value="paper"),
            app_commands.Choice(name="Other", value="other"),
        ]
    )
    async def ticket_command(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        category: app_commands.Choice[str],
    ):
        """Create a new support ticket."""
        self.ticket_counter += 1
        ticket_id = f"TKT-{self.ticket_counter:04d}"

        ticket_data = {
            "id": ticket_id,
            "title": title,
            "description": description,
            "category": category.value,
            "creator": interaction.user.id,
            "creator_name": interaction.user.display_name,
            "created_at": datetime.utcnow().isoformat(),
            "status": "open",
            "messages": [],
        }

        self.tickets[ticket_id] = ticket_data
        self._save_tickets()

        # Create embed
        embed = discord.Embed(
            title=f"Ticket Created: {ticket_id}",
            description=(
                f"**Title:** {title}\n"
                f"**Category:** {category.name}\n"
                f"**Created by:** {interaction.user.mention}\n\n"
                f"**Description:**\n{description}"
            ),
            color=discord.Color.from_str("#006D77"),
        )
        embed.set_footer(text="Use /ticket-reply to add messages. Use /ticket-close to close.")

        await interaction.response.send_message(embed=embed)

        # Notify staff
        support_channel = interaction.guild.get_channel(config.GENERAL_CHANNEL_ID)
        if support_channel:
            await support_channel.send(
                f"🎫 **New Ticket:** {ticket_id}\n"
                f"**From:** {interaction.user.mention}\n"
                f"**Title:** {title}\n"
                f"**Category:** {category.name}"
            )

    @app_commands.command(name="ticket-reply", description="Reply to a ticket")
    @app_commands.describe(
        ticket_id="The ticket ID (e.g., TKT-0001)",
        message="Your reply message",
    )
    async def ticket_reply_command(
        self,
        interaction: discord.Interaction,
        ticket_id: str,
        message: str,
    ):
        """Add a reply to a ticket."""
        ticket_id = ticket_id.upper()

        if ticket_id not in self.tickets:
            await interaction.response.send_message(
                f"Ticket {ticket_id} not found.",
                ephemeral=True,
            )
            return

        ticket = self.tickets[ticket_id]

        # Check if user is ticket creator or staff
        is_creator = ticket["creator"] == interaction.user.id
        is_staff = discord.utils.get(interaction.user.roles, name=config.ROLES["admin"]) is not None

        if not is_creator and not is_staff:
            await interaction.response.send_message(
                "You can only reply to your own tickets.",
                ephemeral=True,
            )
            return

        # Add reply
        reply = {
            "author": interaction.user.display_name,
            "author_id": interaction.user.id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        ticket["messages"].append(reply)
        self._save_tickets()

        # Create embed
        embed = discord.Embed(
            title=f"Ticket Reply: {ticket_id}",
            description=(
                f"**{interaction.user.display_name}** replied:\n\n"
                f"{message}"
            ),
            color=discord.Color.from_str("#E29578"),
        )
        embed.set_footer(text=f"Ticket: {ticket_id} | Status: {ticket['status']}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ticket-close", description="Close a ticket")
    @app_commands.describe(ticket_id="The ticket ID to close")
    async def ticket_close_command(
        self,
        interaction: discord.Interaction,
        ticket_id: str,
    ):
        """Close a support ticket."""
        ticket_id = ticket_id.upper()

        if ticket_id not in self.tickets:
            await interaction.response.send_message(
                f"Ticket {ticket_id} not found.",
                ephemeral=True,
            )
            return

        ticket = self.tickets[ticket_id]

        # Check permissions
        is_creator = ticket["creator"] == interaction.user.id
        is_staff = discord.utils.get(interaction.user.roles, name=config.ROLES["admin"]) is not None

        if not is_creator and not is_staff:
            await interaction.response.send_message(
                "You can only close your own tickets.",
                ephemeral=True,
            )
            return

        # Close ticket
        ticket["status"] = "closed"
        ticket["closed_at"] = datetime.utcnow().isoformat()
        ticket["closed_by"] = interaction.user.display_name
        self._save_tickets()

        # Create summary embed
        embed = discord.Embed(
            title=f"Ticket Closed: {ticket_id}",
            description=(
                f"**Title:** {ticket['title']}\n"
                f"**Closed by:** {interaction.user.mention}\n"
                f"**Messages:** {len(ticket['messages'])}"
            ),
            color=discord.Color.from_str("#6c757d"),  # Gray
        )

        if ticket["messages"]:
            last_message = ticket["messages"][-1]
            embed.add_field(
                name="Last Reply",
                value=f"**{last_message['author']}:** {last_message['message'][:200]}",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="tickets", description="View your open tickets")
    async def tickets_command(self, interaction: discord.Interaction):
        """List user's open tickets."""
        user_tickets = [
            t for t in self.tickets.values()
            if t["creator"] == interaction.user.id and t["status"] == "open"
        ]

        if not user_tickets:
            await interaction.response.send_message(
                "You have no open tickets.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"Your Open Tickets ({len(user_tickets)})",
            color=discord.Color.from_str("#006D77"),
        )

        for ticket in user_tickets:
            embed.add_field(
                name=f"{ticket['id']}: {ticket['title'][:30]}",
                value=(
                    f"**Category:** {ticket['category']}\n"
                    f"**Created:** {ticket['created_at'][:10]}\n"
                    f"**Replies:** {len(ticket['messages'])}"
                ),
                inline=False,
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    """Add cogs to bot."""
    await bot.add_cog(GitHubIntegration(bot))
    await bot.add_cog(TicketSystem(bot))
