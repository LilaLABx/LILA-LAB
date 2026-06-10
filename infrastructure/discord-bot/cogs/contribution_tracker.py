"""Contribution Tracker Cog.

Tracks GitHub contributions, assigns roles based on weighted points,
announces milestones, and maintains a leaderboard.
"""

import json
import logging
import os
from pathlib import Path

import aiohttp
import config
import discord
from discord import app_commands
from discord.ext import commands, tasks

logger = logging.getLogger("lila-bot.contribution_tracker")

# ──────────────────────────────────────────────
# STORE SCHEMA
#   version: 1
#   users: {
#     "<discord_user_id>": {
#       "github_username": str | None,
#       "total_points": int,
#       "prs_merged": int,
#       "prs_opened": int,
#       "issues_closed": int,
#       "issues_created": int,
#       "comments": int,
#       "current_role": str,
#       "milestones_achieved": list[str],
#       "badges_claimed": list[str],
#     }
#   }
# ──────────────────────────────────────────────
STORE_VERSION = 1


class ContributionTracker(commands.Cog):
    """Track GitHub contributions and manage role progression."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO", "LilaLABx/LILA-LAB")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.github_token}" if self.github_token else None,
        }

        # JSON store — discord_user_id → contribution data
        self.store_file = Path(__file__).parent.parent / "data" / "contribution_tracker.json"
        self.store: dict = {"version": STORE_VERSION, "users": {}}
        self._load_store()

        # Start background polling
        if self.github_token:
            self.poll_contributions.start()

    # ── Store persistence ───────────────────────

    def _load_store(self):
        """Load store from disk, resetting on corruption."""
        if not self.store_file.exists():
            self.store = {"version": STORE_VERSION, "users": {}}
            return

        try:
            raw = json.loads(self.store_file.read_text())
        except Exception:
            logger.warning("Contribution tracker store corrupt — starting fresh")
            self.store = {"version": STORE_VERSION, "users": {}}
            return

        if isinstance(raw, dict) and "users" in raw:
            self.store = raw
            return

        self.store = {"version": STORE_VERSION, "users": {}}

    def _save_store(self):
        """Atomically persist the store to disk."""
        self.store_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.store_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.store, indent=2))
        tmp.rename(self.store_file)  # atomic on POSIX

    # ── Background polling ──────────────────────

    @tasks.loop(minutes=15)
    async def poll_contributions(self):
        """Fetch GitHub contributions and recalculate points for linked users.

        Recalculates from scratch on each poll to prevent double-counting.
        Detects role promotions and milestone achievements.
        """
        await self.bot.wait_until_ready()
        if not self.github_token:
            return

        # Build reverse map: github_username → discord_user_id
        linked_users = {
            data["github_username"]: uid
            for uid, data in self.store["users"].items()
            if data.get("github_username")
        }
        if not linked_users:
            return

        # Fetch all PRs and issues from GitHub
        prs = await self._fetch_all_prs()
        issues = await self._fetch_all_issues()
        if prs is None and issues is None:
            return

        # Recalculate stats from scratch per user
        user_stats: dict[str, dict[str, int]] = {}

        if prs:
            for pr in prs:
                author = pr.get("user", {}).get("login")
                if not author or author not in linked_users:
                    continue
                uid = linked_users[author]
                stats = user_stats.setdefault(uid, {
                    "prs_merged": 0,
                    "prs_opened": 0,
                    "issues_closed": 0,
                    "issues_created": 0,
                })
                stats["prs_opened"] += 1
                if pr.get("merged_at"):
                    stats["prs_merged"] += 1

        if issues:
            for issue in issues:
                if "pull_request" in issue:
                    continue
                author = issue.get("user", {}).get("login")
                if not author or author not in linked_users:
                    continue
                uid = linked_users[author]
                stats = user_stats.setdefault(uid, {
                    "prs_merged": 0,
                    "prs_opened": 0,
                    "issues_closed": 0,
                    "issues_created": 0,
                })
                stats["issues_created"] += 1
                if issue.get("state") == "closed":
                    stats["issues_closed"] += 1

        # Apply changes and check roles / milestones
        announce_channel = self.bot.get_channel(config.CONTRIBUTIONS_ANNOUNCE_CHANNEL_ID)
        store_changed = False

        for uid, fresh in user_stats.items():
            user_data = self.store["users"].get(uid)
            if not user_data:
                continue

            old_prs_merged = user_data.get("prs_merged", 0)
            old_prs_opened = user_data.get("prs_opened", 0)
            old_issues_closed = user_data.get("issues_closed", 0)
            old_issues_created = user_data.get("issues_created", 0)
            # Only update if something actually changed
            if (fresh["prs_merged"] == old_prs_merged
                    and fresh["prs_opened"] == old_prs_opened
                    and fresh["issues_closed"] == old_issues_closed
                    and fresh["issues_created"] == old_issues_created):
                continue

            user_data["prs_merged"] = fresh["prs_merged"]
            user_data["prs_opened"] = fresh["prs_opened"]
            user_data["issues_closed"] = fresh["issues_closed"]
            user_data["issues_created"] = fresh["issues_created"]

            # Recalculate total points from scratch
            new_total = (
                fresh["prs_merged"] * config.POINTS["pr_merged"]
                + fresh["prs_opened"] * config.POINTS["pr_opened"]
                + fresh["issues_closed"] * config.POINTS["issue_closed"]
                + fresh["issues_created"] * config.POINTS["issue_created"]
            )
            user_data["total_points"] = new_total

            # ── Role promotion check ──────────────
            old_role_key = user_data.get("current_role", config.ROLE_LADDER[0][0])
            new_role_key = self._calculate_role(new_total)

            if new_role_key != old_role_key:
                user_data["current_role"] = new_role_key
                store_changed = True
                if announce_channel:
                    await self._update_member_role(uid, old_role_key, new_role_key)
                    await self._announce_role_change(announce_channel, uid, old_role_key, new_role_key)

            # ── Milestone check ──────────────────
            milestones_achieved = user_data.get("milestones_achieved", [])
            for milestone_key, milestone_def in config.MILESTONES.items():
                if milestone_key in milestones_achieved:
                    continue

                prs_merged_req = milestone_def.get("prs_merged", 0)
                total_contribs_req = milestone_def.get("total_contributions", 0)

                achieved = True
                if prs_merged_req and fresh["prs_merged"] < prs_merged_req:
                    achieved = False
                if total_contribs_req:
                    total_actions = (
                        fresh["prs_merged"] + fresh["prs_opened"]
                        + fresh["issues_closed"] + fresh["issues_created"]
                    )
                    if total_actions < total_contribs_req:
                        achieved = False

                if achieved:
                    milestones_achieved.append(milestone_key)
                    user_data["milestones_achieved"] = milestones_achieved
                    store_changed = True
                    if announce_channel:
                        await self._announce_milestone(announce_channel, uid, milestone_key)

        if store_changed:
            self._save_store()

    @poll_contributions.before_loop
    async def before_poll(self):
        await self.bot.wait_until_ready()

    # ── Role calculation & management ─────────

    def _calculate_role(self, points: int) -> str:
        """Return the highest role key the given points qualify for."""
        current = config.ROLE_LADDER[0][0]
        for role_key, threshold in config.ROLE_LADDER:
            if points >= threshold:
                current = role_key
        return current

    async def _update_member_role(self, uid: str, old_role_key: str, new_role_key: str):
        """Remove the old lower role and assign the new higher role."""
        guild_id = int(os.getenv("GUILD_ID", "0"))
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return

        try:
            member = guild.get_member(int(uid))
        except (ValueError, TypeError):
            return
        if not member:
            return

        old_role_name = config.ROLES.get(old_role_key)
        new_role_name = config.ROLES.get(new_role_key)
        if not old_role_name or not new_role_name:
            return

        new_role = discord.utils.get(guild.roles, name=new_role_name)
        if not new_role:
            return

        old_role = discord.utils.get(guild.roles, name=old_role_name) if old_role_name != new_role_name else None

        to_remove = []
        if old_role and old_role in member.roles and old_role != new_role:
            to_remove.append(old_role)

        try:
            if to_remove:
                await member.remove_roles(*to_remove)
            await member.add_roles(new_role)
        except discord.Forbidden:
            logger.warning("Missing permissions to update roles for user %s", uid)

    async def _announce_role_change(self, channel, uid: str, old_key: str, new_key: str):
        """Post a role promotion announcement."""
        member = await self._resolve_member(uid)
        display = member.mention if member else f"<@{uid}>"
        old_name = config.ROLES.get(old_key, old_key)
        new_name = config.ROLES.get(new_key, new_key)

        embed = discord.Embed(
            title="Role Promoted!",
            description=(
                f"{display} has been promoted from **{old_name}** "
                f"to **{new_name}**!"
            ),
            color=discord.Color.from_str("#28a745"),
        )
        await channel.send(embed=embed)

    async def _announce_milestone(self, channel, uid: str, milestone_key: str):
        """Post a milestone achievement announcement."""
        member = await self._resolve_member(uid)
        display = member.mention if member else f"<@{uid}>"
        milestone = config.MILESTONES.get(milestone_key, {})
        milestone_name = milestone.get("name", milestone_key)

        embed = discord.Embed(
            title="Milestone Achieved!",
            description=f"{display} has achieved **{milestone_name}**!",
            color=discord.Color.from_str("#E29578"),
        )
        await channel.send(embed=embed)

    async def _resolve_member(self, uid: str):
        """Try to get a guild member by user ID."""
        guild_id = int(os.getenv("GUILD_ID", "0"))
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return None
        try:
            return guild.get_member(int(uid))
        except (ValueError, TypeError):
            return None

    # ── GitHub API helpers ────────────────────

    async def _fetch_all_prs(self) -> list | None:
        """Fetch all pull requests (open + closed) with pagination."""
        return await self._paginated_get(
            f"https://api.github.com/repos/{self.github_repo}/pulls",
            {"state": "all"},
        )

    async def _fetch_all_issues(self) -> list | None:
        """Fetch all issues (open + closed) with pagination."""
        return await self._paginated_get(
            f"https://api.github.com/repos/{self.github_repo}/issues",
            {"state": "all"},
        )

    async def _paginated_get(self, url: str, params: dict | None = None) -> list | None:
        """Walk paginated GitHub API endpoints, returning all results."""
        results: list = []
        page = 1
        per_page = 100

        try:
            async with aiohttp.ClientSession() as session:
                while True:
                    req_params = dict(params or {})
                    req_params["per_page"] = str(per_page)
                    req_params["page"] = str(page)

                    async with session.get(url, headers=self.headers, params=req_params) as resp:
                        if resp.status != 200:
                            logger.warning("GitHub API returned %d for %s", resp.status, url)
                            return None
                        data = await resp.json()
                        if not data:
                            break
                        results.extend(data)
                        if len(data) < per_page:
                            break
                        page += 1
        except (aiohttp.ClientError, Exception) as exc:
            logger.error("GitHub request failed: %s", exc)
            return None

        return results

    # ── Lifecycle ─────────────────────────────

    def cog_unload(self):
        """Cancel the background poll task on cog unload."""
        if self.poll_contributions.is_running():
            self.poll_contributions.cancel()

    # ── Internal helpers ──────────────────────

    def _get_user_data(self, uid: str) -> dict:
        """Get or create a user data entry."""
        if uid not in self.store["users"]:
            self.store["users"][uid] = {
                "github_username": None,
                "total_points": 0,
                "prs_merged": 0,
                "prs_opened": 0,
                "issues_closed": 0,
                "issues_created": 0,
                "comments": 0,
                "current_role": config.ROLE_LADDER[0][0],
                "milestones_achieved": [],
                "badges_claimed": [],
            }
        return self.store["users"][uid]

    def _get_next_role(self, points: int) -> tuple[str | None, int]:
        """Return (next_role_key, threshold) or (None, 0) if at max."""
        for role_key, threshold in config.ROLE_LADDER:
            if points < threshold:
                return role_key, threshold
        return None, 0

    @staticmethod
    def _build_progress_bar(current: int, target: int, length: int = 10) -> str:
        """Build a text progress bar string."""
        if target <= 0:
            return "█" * length
        filled = min(int(current / target * length), length)
        return "▓" * filled + "░" * (length - filled)

    # ── Slash Commands ────────────────────────

    @app_commands.command(
        name="link",
        description="Link your GitHub username to your Discord account",
    )
    @app_commands.describe(github_username="Your GitHub username")
    async def link_command(self, interaction: discord.Interaction, github_username: str):
        """Link a GitHub username to the caller's Discord account."""
        uid = str(interaction.user.id)
        user_data = self._get_user_data(uid)
        old_username = user_data.get("github_username")
        user_data["github_username"] = github_username
        self._save_store()

        if old_username:
            msg = f"GitHub account updated from `{old_username}` to `{github_username}`."
        else:
            msg = f"GitHub account linked as `{github_username}`."

        embed = discord.Embed(
            title="GitHub Account Linked",
            description=msg,
            color=discord.Color.from_str("#28a745"),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="mycontributions",
        description="View your contribution stats, role, and milestone progress",
    )
    async def mycontributions_command(self, interaction: discord.Interaction):
        """Show the caller's contribution stats, role, and milestone progress."""
        uid = str(interaction.user.id)
        user_data = self._get_user_data(uid)

        total_points = user_data.get("total_points", 0)
        current_role_key = user_data.get("current_role", config.ROLE_LADDER[0][0])
        current_role_name = config.ROLES.get(current_role_key, current_role_key)
        next_role_key, next_threshold = self._get_next_role(total_points)

        embed = discord.Embed(
            title=f"Contributions — {interaction.user.display_name}",
            color=discord.Color.from_str("#006D77"),
        )

        # Rank / role section
        role_text = f"**Current Role:** {current_role_name}"
        if next_role_key:
            next_role_name = config.ROLES.get(next_role_key, next_role_key)
            points_needed = next_threshold - total_points
            progress = self._build_progress_bar(total_points, next_threshold)
            role_text += (
                f"\n**Next Role:** {next_role_name} ({points_needed} points away)"
                f"\n{progress} `{total_points}/{next_threshold}`"
            )
        else:
            role_text += "\n**Max role achieved!**"

        embed.add_field(name="Rank", value=role_text, inline=False)

        # Stats breakdown
        stats = (
            f"**Total Points:** {total_points}\n"
            f"**PRs Merged:** {user_data.get('prs_merged', 0)}\n"
            f"**PRs Opened:** {user_data.get('prs_opened', 0)}\n"
            f"**Issues Closed:** {user_data.get('issues_closed', 0)}\n"
            f"**Issues Created:** {user_data.get('issues_created', 0)}\n"
            f"**Comments:** {user_data.get('comments', 0)}"
        )
        embed.add_field(name="Stats", value=stats, inline=False)

        # Milestones achieved
        milestones = user_data.get("milestones_achieved", [])
        if milestones:
            milestone_names = [
                config.MILESTONES[m]["name"] for m in milestones if m in config.MILESTONES
            ]
            embed.add_field(
                name="Milestones Achieved",
                value="\n".join(f"• {name}" for name in milestone_names),
                inline=False,
            )
        else:
            embed.add_field(
                name="Milestones",
                value="None yet. Keep contributing!",
                inline=False,
            )

        # Badges claimed
        badges = user_data.get("badges_claimed", [])
        if badges:
            badge_names = [
                config.MILESTONES[b]["name"] for b in badges if b in config.MILESTONES
            ]
            embed.add_field(
                name="Badges Claimed",
                value="\n".join(f"• {name}" for name in badge_names),
                inline=False,
            )

        gh_username = user_data.get("github_username")
        if gh_username:
            embed.set_footer(text=f"GitHub: {gh_username}")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="leaderboard",
        description="View top contributors by points",
    )
    @app_commands.describe(page="Page number (default: 1, 10 per page)")
    async def leaderboard_command(
        self,
        interaction: discord.Interaction,
        page: int = 1,
    ):
        """Show paginated leaderboard of contributors by total points."""
        users = self.store.get("users", {})
        if not users:
            embed = discord.Embed(
                title="Contributor Leaderboard",
                description="No contributors yet. Link your GitHub with `/link` to get started!",
                color=discord.Color.from_str("#006D77"),
            )
            await interaction.response.send_message(embed=embed)
            return

        # Filter users who have any points
        ranked = [
            (uid, data)
            for uid, data in users.items()
            if data.get("total_points", 0) > 0
        ]
        ranked.sort(key=lambda x: x[1].get("total_points", 0), reverse=True)

        if not ranked:
            embed = discord.Embed(
                title="Contributor Leaderboard",
                description="No points earned yet. Link your GitHub with `/link` and start contributing!",
                color=discord.Color.from_str("#006D77"),
            )
            await interaction.response.send_message(embed=embed)
            return

        per_page = 10
        total_pages = (len(ranked) + per_page - 1) // per_page
        page = max(1, min(page, total_pages))
        start = (page - 1) * per_page
        end = start + per_page
        page_users = ranked[start:end]

        embed = discord.Embed(
            title=f"Contribution Leaderboard (Page {page}/{total_pages})",
            color=discord.Color.from_str("#006D77"),
        )

        guild = interaction.guild
        for rank_offset, (uid, data) in enumerate(page_users):
            rank = start + rank_offset + 1
            total_points = data.get("total_points", 0)
            role_key = data.get("current_role", config.ROLE_LADDER[0][0])
            role_name = config.ROLES.get(role_key, role_key)

            member = guild.get_member(int(uid)) if uid.isdigit() else None
            display_name = member.display_name if member else f"User {uid[:8]}..."
            gh_username = data.get("github_username") or ""

            medal = ""
            if rank == 1:
                medal = "🥇 "
            elif rank == 2:
                medal = "🥈 "
            elif rank == 3:
                medal = "🥉 "

            embed.add_field(
                name=f"{medal}#{rank} {display_name}",
                value=(
                    f"**Points:** {total_points}\n"
                    f"**Role:** {role_name}"
                    + (f"\n**GitHub:** `{gh_username}`" if gh_username else "")
                ),
                inline=False,
            )

        embed.set_footer(text="Use /mycontributions to see your stats | Use /roleinfo for requirements")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="roleinfo",
        description="Display role ladder, point values, and milestone requirements",
    )
    async def roleinfo_command(self, interaction: discord.Interaction):
        """Show the role ladder, point thresholds, and milestone definitions."""
        embed = discord.Embed(
            title="Contribution Roles & Milestones",
            color=discord.Color.from_str("#006D77"),
        )

        # Role ladder
        ladder_lines = []
        for role_key, threshold in config.ROLE_LADDER:
            role_name = config.ROLES.get(role_key, role_key)
            if threshold == 0:
                ladder_lines.append(f"• **{role_name}** — Starting role")
            else:
                ladder_lines.append(f"• **{role_name}** — {threshold} points")
        embed.add_field(
            name="Role Ladder",
            value="\n".join(ladder_lines),
            inline=False,
        )

        # Point values
        point_lines = []
        for key, value in config.POINTS.items():
            label = key.replace("_", " ").title()
            plural = "s" if value != 1 else ""
            point_lines.append(f"• **{label}:** {value} point{plural}")
        embed.add_field(
            name="Point Values",
            value="\n".join(point_lines),
            inline=False,
        )

        # Milestones
        milestone_lines = []
        for key, milestone in config.MILESTONES.items():
            reqs = []
            if "prs_merged" in milestone:
                reqs.append(f"{milestone['prs_merged']} PRs merged")
            if "total_contributions" in milestone:
                reqs.append(f"{milestone['total_contributions']} total contributions")
            milestone_lines.append(
                f"• **{milestone['name']}** — {' + '.join(reqs)}"
            )
        embed.add_field(
            name="Milestones",
            value="\n".join(milestone_lines),
            inline=False,
        )

        # Badge info
        embed.add_field(
            name="Claiming Badges",
            value=(
                "Use `/claimbadge` to claim a badge once you've met "
                "the milestone requirements."
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="claimbadge",
        description="Claim a milestone badge",
    )
    @app_commands.describe(badge="The badge to claim")
    @app_commands.choices(
        badge=[
            app_commands.Choice(name="🥉 Bronze Contributor", value="bronze"),
            app_commands.Choice(name="🥈 Silver Contributor", value="silver"),
            app_commands.Choice(name="🥇 Gold Contributor", value="gold"),
            app_commands.Choice(name="💎 Platinum Contributor", value="platinum"),
        ]
    )
    async def claimbadge_command(
        self,
        interaction: discord.Interaction,
        badge: app_commands.Choice[str],
    ):
        """Claim a milestone badge if requirements are met."""
        uid = str(interaction.user.id)
        user_data = self._get_user_data(uid)
        badge_key = badge.value

        if badge_key not in config.MILESTONES:
            await interaction.response.send_message("Invalid badge.", ephemeral=True)
            return

        # Already claimed?
        badges_claimed = user_data.get("badges_claimed", [])
        if badge_key in badges_claimed:
            await interaction.response.send_message(
                "You've already claimed this badge!",
                ephemeral=True,
            )
            return

        # Milestone achieved?
        milestones = user_data.get("milestones_achieved", [])
        if badge_key not in milestones:
            await interaction.response.send_message(
                "You haven't met the requirements for this badge yet. "
                "Use `/roleinfo` to see the requirements.",
                ephemeral=True,
            )
            return

        badges_claimed.append(badge_key)
        user_data["badges_claimed"] = badges_claimed
        self._save_store()

        milestone = config.MILESTONES[badge_key]
        embed = discord.Embed(
            title="Badge Claimed!",
            description=(
                f"{interaction.user.mention} has claimed the "
                f"**{milestone['name']}** badge!"
            ),
            color=discord.Color.from_str("#28a745"),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="adjust-points",
        description="Adjust a user's contribution points (Admin)",
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        user="The user to adjust",
        points="Points to add (positive) or remove (negative)",
        reason="Reason for adjustment",
    )
    async def adjust_points_command(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        points: int,
        reason: str,
    ):
        """Manually adjust a user's contribution points."""
        uid = str(user.id)
        user_data = self._get_user_data(uid)

        old_points = user_data.get("total_points", 0)
        new_points = max(0, old_points + points)
        user_data["total_points"] = new_points

        # Recalculate role
        old_role_key = user_data.get("current_role", config.ROLE_LADDER[0][0])
        new_role_key = self._calculate_role(new_points)
        user_data["current_role"] = new_role_key

        self._save_store()

        embed = discord.Embed(
            title="Points Adjusted",
            description=(
                f"**User:** {user.mention}\n"
                f"**Adjustment:** {points:+d} points\n"
                f"**Previous Points:** {old_points}\n"
                f"**New Points:** {new_points}\n"
                f"**Reason:** {reason}"
            ),
            color=discord.Color.from_str("#E29578"),
        )

        if new_role_key != old_role_key:
            old_name = config.ROLES.get(old_role_key, old_role_key)
            new_name = config.ROLES.get(new_role_key, new_role_key)
            embed.add_field(
                name="Role Change",
                value=f"Changed from **{old_name}** to **{new_name}**",
                inline=False,
            )
            await self._update_member_role(uid, old_role_key, new_role_key)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="sync-contributions",
        description="Force sync GitHub contributions now (Admin)",
    )
    @app_commands.default_permissions(administrator=True)
    async def sync_contributions_command(self, interaction: discord.Interaction):
        """Manually trigger a contribution poll cycle."""
        await interaction.response.defer(ephemeral=True)
        if not self.github_token:
            await interaction.followup.send(
                "GitHub token not configured.",
                ephemeral=True,
            )
            return

        await self.poll_contributions()
        await interaction.followup.send(
            "Contribution sync complete. Points and roles have been updated.",
            ephemeral=True,
        )


    @app_commands.command(
        name="contribution-guide",
        description="Complete guide to tracking your contributions and earning roles",
    )
    async def contribution_guide_command(self, interaction: discord.Interaction):
        """Show a complete guide to the contribution tracking system."""
        embed = discord.Embed(
            title="Contribution Tracking Guide",
            description=(
                "Track your GitHub contributions, earn points, climb the role ladder, "
                "and unlock milestone badges. Here's everything you need to know."
            ),
            color=discord.Color.from_str("#006D77"),
        )

        embed.add_field(
            name="1. Link Your GitHub Account",
            value=(
                "Use `/link <github_username>` to connect your Discord and GitHub accounts.\n"
                "This is the **only** setup step — do it once and the bot handles the rest.\n"
                "```/link nabil0x```"
            ),
            inline=False,
        )

        embed.add_field(
            name="2. Contribute to LILA Lab on GitHub",
            value=(
                "The bot automatically tracks these actions on the `LilaLABx/LILA-LAB` repo:\n\n"
                "• **Open a PR** — `+5 pts`\n"
                "• **Get a PR merged** — `+10 pts` (also counts as opened)\n"
                "• **Create an Issue** — `+2 pts`\n"
                "• **Close an Issue** — `+5 pts`\n"
                "• **Comment** — `+1 pt`\n\n"
                "Points are recalculated every **15 minutes** — no manual updates needed."
            ),
            inline=False,
        )

        embed.add_field(
            name="3. Check Your Progress",
            value=(
                "• `/mycontributions` — View your points, stats, current role, and milestones\n"
                "• `/leaderboard` — See who's leading the community\n"
                "• `/roleinfo` — Review the full role ladder and point values"
            ),
            inline=False,
        )

        embed.add_field(
            name="4. Climb the Role Ladder",
            value=(
                "Roles are **automatically assigned** as you earn points. "
                "The bot removes your old role and gives you the new one.\n\n"
                "• **Contributor** — `0 pts` (starting role)\n"
                "• **Active Contributor** — `50 pts`\n"
                "• **Core Contributor** — `150 pts`\n"
                "• **Maintainer Candidate** — `300 pts`"
            ),
            inline=False,
        )

        embed.add_field(
            name="5. Earn Milestone Badges",
            value=(
                "Milestones are **auto-detected** during polling, but you must claim "
                "the badge manually:\n\n"
                "• **Bronze Contributor** — 10 PRs merged\n"
                "• **Silver Contributor** — 25 PRs merged\n"
                "• **Gold Contributor** — 50 PRs merged\n"
                "• **Platinum Contributor** — 100 total contributions\n\n"
                "Use `/claimbadge <badge>` to claim yours!"
            ),
            inline=False,
        )

        embed.add_field(
            name="6. Admin Commands",
            value=(
                "• `/adjust-points <user> <points> <reason>` — Manual point adjustment\n"
                "• `/sync-contributions` — Force an immediate GitHub sync\n"
                "(Admin-only, requires Administrator permission)"
            ),
            inline=False,
        )

        embed.set_footer(
            text="LILA Lab Contribution System | Points recalculated every 15 min"
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    """Add the cog to the bot."""
    await bot.add_cog(ContributionTracker(bot))
