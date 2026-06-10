"""Issue Tracking Cog.

Syncs GitHub issues to a Discord channel with crash-proof idempotency.
Every posted issue maps to a Discord message ID so restarts never cause duplicates.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, time
from pathlib import Path

import aiohttp
import config
import discord
from discord import app_commands
from discord.ext import commands, tasks

logger = logging.getLogger("lila-bot.issue_tracking")

# ──────────────────────────────────────────────
# STORE SCHEMA
#   version: 2 (current)
#   issues: { "<issue_number>": "<discord_message_id>", ... }
#
# Migration from v1 (flat list) is handled automatically.
# ──────────────────────────────────────────────
STORE_VERSION = 2


class IssueTracking(commands.Cog):
    """Sync GitHub issues to Discord with message-verified idempotency."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO", "LilaLABx/LILA-LAB")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.github_token}" if self.github_token else None,
        }

        # Store: issue_number (str) → discord_message_id (str)
        self.store_file = Path(__file__).parent.parent / "data" / "posted_issues.json"
        self.store: dict[str, str] = {}  # issue_number → message_id
        self._load_store()

        # Runtime mapping: discord_message_id → claim intent
        self.claim_intents: dict[int, dict] = {}
        self._rebuild_claim_intents()

        self._startup_synced = False

        if self.github_token:
            self.sync_issues_to_channel.start()
            self.daily_digest.start()

    # ── Store persistence ───────────────────────

    def _load_store(self):
        """Load store with auto-migration from v1 flat list."""
        if not self.store_file.exists():
            self.store = {}
            return

        try:
            raw = json.loads(self.store_file.read_text())
        except Exception:
            logger.warning("Posted-issues store corrupt — starting fresh")
            self.store = {}
            return

        # v1 was a flat list [1, 2, 3]
        if isinstance(raw, list):
            logger.info("Migrating posted-issues store from v1 (flat list) to v2 (issue→message mapping)")
            self.store = {str(i): "UNVERIFIED" for i in raw}
            self._save_store()
            return

        # v2 dict
        if isinstance(raw, dict) and "issues" in raw:
            self.store = raw["issues"]
            return

        self.store = {}

    def _save_store(self):
        """Atomically persist the store to disk."""
        self.store_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.store_file.with_suffix(".tmp")
        tmp.write_text(json.dumps({"version": STORE_VERSION, "issues": self.store}, indent=2))
        tmp.rename(self.store_file)  # atomic on POSIX

    def _rebuild_claim_intents(self):
        """Rebuild in-memory claim_intents from the store after a restart."""
        self.claim_intents.clear()
        for issue_number_str, message_id_str in self.store.items():
            try:
                mid = int(message_id_str)
                if mid <= 0:
                    continue
                self.claim_intents[mid] = {
                    "issue_number": int(issue_number_str),
                    "claimer_id": None,
                }
            except (ValueError, TypeError):
                continue

    # ── Crash-safe startup verification ────────

    @commands.Cog.listener()
    async def on_ready(self):
        """On startup: verify every stored message still exists in the channel.

        If a message was deleted, remove it from the store so the issue gets
        re-posted. This makes the store self-healing across crashes.
        """
        if not self.github_token or self._startup_synced:
            return
        self._startup_synced = True

        channel = self.bot.get_channel(config.ISSUE_TRACKING_CHANNEL_ID)
        if not channel:
            logger.warning("Issue tracking channel not found — skipping startup verification")
            return

        if not self.store:
            logger.info("No previously posted issues found — will post all open issues")
            await self.sync_issues_to_channel()
            return

        verified: dict[str, str] = {}
        stale = 0
        for issue_str, msg_id_str in list(self.store.items()):
            try:
                msg_id = int(msg_id_str)
                await channel.fetch_message(msg_id)
                verified[issue_str] = msg_id_str
            except (discord.NotFound, discord.Forbidden):
                stale += 1
                logger.info("Stale entry — issue %s message %s gone from channel", issue_str, msg_id_str)
            except Exception as exc:
                logger.warning("Could not verify issue %s: %s", issue_str, exc)
                verified[issue_str] = msg_id_str  # keep on error, don't re-post

        if stale:
            logger.info("Removed %d stale entries, %d verified", stale, len(verified))
            self.store = verified
            self._save_store()
            self._rebuild_claim_intents()

        # Now sync any new issues GitHub has that aren't in the store
        await self.sync_issues_to_channel()

    # ── Lifecycle ───────────────────────────────

    def cog_unload(self):
        if self.sync_issues_to_channel.is_running():
            self.sync_issues_to_channel.cancel()
        if self.daily_digest.is_running():
            self.daily_digest.cancel()

    # ── Issue sync (idempotent) ────────────────

    @tasks.loop(minutes=30)
    async def sync_issues_to_channel(self):
        """Fetch open issues and post any not yet in the store.

        Idempotent by design: each issue is checked against the store before
        posting. The store is flushed to disk after EACH post so a crash
        between posts loses at most one issue.
        """
        await self.bot.wait_until_ready()
        if not self.github_token:
            return

        channel = self.bot.get_channel(config.ISSUE_TRACKING_CHANNEL_ID)
        if not channel:
            return

        issues = await self._fetch_open_issues()
        if issues is None:
            return

        new_count = 0
        for issue in issues:
            if "pull_request" in issue:
                continue
            issue_id = str(issue["number"])
            if issue_id in self.store:
                continue  # already posted — full idempotency

            embed = self._build_issue_embed(issue)
            try:
                msg = await channel.send(embed=embed)
                await msg.add_reaction("✋")
            except discord.HTTPException as exc:
                logger.error("Failed to post issue #%s: %s", issue_id, exc)
                continue

            # Persist immediately: crash after this line loses at most one issue
            self.store[issue_id] = str(msg.id)
            self._save_store()
            self.claim_intents[msg.id] = {
                "issue_number": int(issue_id),
                "claimer_id": None,
            }
            new_count += 1

        if new_count:
            summary = await channel.send(
                f"📬 **{new_count}** new issue{'s' if new_count > 1 else ''} posted. "
                f"React with ✋ to claim one!"
            )
            logger.info("Posted %d new issue(s) — summary at message %s", new_count, summary.id)

    # ── Daily digest ───────────────────────────

    @tasks.loop(time=time(hour=9, minute=0))
    async def daily_digest(self):
        """Post a daily summary of open issues to the tracking channel."""
        await self.bot.wait_until_ready()
        if not self.github_token:
            return

        channel = self.bot.get_channel(config.ISSUE_TRACKING_CHANNEL_ID)
        if not channel:
            return

        issues = await self._fetch_open_issues()
        if issues is None:
            return

        real_issues = [i for i in issues if "pull_request" not in i]
        label_counts = {}
        for i in real_issues:
            for label in i.get("labels", []):
                name = label["name"]
                label_counts[name] = label_counts.get(name, 0) + 1

        unassigned = sum(1 for i in real_issues if not i.get("assignee"))
        already_posted = sum(1 for i in real_issues if str(i["number"]) in self.store)
        label_summary = "\n".join(
            f"• **{name}:** {count}"
            for name, count in sorted(label_counts.items(), key=lambda x: -x[1])[:8]
        ) or "None"

        embed = discord.Embed(
            title=f"📋 Daily Issue Digest — {len(real_issues)} Open",
            description=(
                f"**Unassigned:** {unassigned}\n"
                f"**Assigned:** {len(real_issues) - unassigned}\n"
                f"**In this channel:** {already_posted}/{len(real_issues)}\n\n"
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

    # ── Reaction claiming ──────────────────────

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Handle ✋ reaction for claiming issues."""
        if payload.guild_id is None:
            return
        if payload.emoji.name != "✋":
            return

        mid = payload.message_id
        if mid not in self.claim_intents:
            return

        entry = self.claim_intents[mid]
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
            msg = await channel.fetch_message(mid)
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

    # ── Helpers ─────────────────────────────────

    async def _fetch_open_issues(self):
        """Return parsed open issues, or None on failure."""
        url = f"https://api.github.com/repos/{self.github_repo}/issues?state=open&per_page=100"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status != 200:
                        logger.warning("GitHub API returned %d fetching issues", resp.status)
                        return None
                    return await resp.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            logger.error("GitHub request failed: %s", exc)
            return None

    def _build_issue_embed(self, issue):
        labels = issue.get("labels", [])
        label_text = " ".join(f"[{l['name']}]" for l in labels[:5]) or "No labels"

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

    # ── Slash commands ─────────────────────────

    @app_commands.command(name="claim", description="Claim a GitHub issue (assigns via API)")
    @app_commands.describe(issue_number="The GitHub issue number to claim")
    async def claim_command(self, interaction: discord.Interaction, issue_number: int):
        """Claim a GitHub issue by assigning it to the caller."""
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

    @app_commands.command(name="sync-issues", description="Force sync new GitHub issues to this channel (Admin)")
    @app_commands.default_permissions(administrator=True)
    async def sync_issues_command(self, interaction: discord.Interaction):
        """Manually trigger an issue sync. Only posts issues NOT already in the store."""
        await interaction.response.defer(ephemeral=True)
        if not self.github_token:
            await interaction.followup.send("GitHub token not configured.", ephemeral=True)
            return

        # Does NOT clear the store — only syncs genuinely new issues
        await self.sync_issues_to_channel()
        await interaction.followup.send(
            f"✅ Sync complete. Only new issues were posted to <#{config.ISSUE_TRACKING_CHANNEL_ID}>.",
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
