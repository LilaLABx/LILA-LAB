# LILA Lab Bot — Development Guidelines

> Rules for building bot features that survive crashes, restarts, and Discord's failure modes.

---

## 1. Idempotency — Thou Shalt Not Duplicate

Every action that writes to Discord **must** be safe to repeat arbitrarily many times. If the bot crashes between two lines of code, restarts, and the same operation runs again, the user experience must be identical to a single clean run.

### 1.1 The Store Pattern

Maintain a **persistent store** (JSON file in `data/`) mapping external IDs to Discord message IDs:

```json
{
  "version": 2,
  "issues": {
    "52": "1345678901234567890",
    "53": "1345678901234567891"
  }
}
```

**Rules:**
- Before posting **anything** to Discord, check the store first.
- After posting successfully, **immediately** persist the mapping to disk.
- Use atomic writes: write to `.tmp` then rename (POSIX atomic).

### 1.2 Startup Verification

On `on_ready`, for every entry in the store, **fetch the message** from the channel:

```
store = load("data/posted_issues.json")
for issue_num, msg_id in store:
    try:
        msg = await channel.fetch_message(msg_id)
        # message exists → keep in store
    except NotFound:
        # message was deleted → remove from store (will re-post)
```

This self-heals across crashes without ever duplicating an existing message.

### 1.3 Code Pattern for Any Writer

```python
async def post_something_idempotent(self, external_id):
    if external_id in self.store:
        return  # already done — skip

    msg = await channel.send(embed=...)

    # PERSIST IMMEDIATELY — crash safety point
    self.store[external_id] = str(msg.id)
    self._save_store()
```

The critical invariant: **the store is always the source of truth**. If it says something is posted, it is posted. If a crash happens before `_save_store()`, the post is lost but no duplicate happens.

---

## 2. State Management — You Own Your Data

### 2.1 Scoped JSON Stores

Each cog that needs persistence gets its own JSON file:

| File | Cog | Purpose |
|---|---|---|
| `data/posted_issues.json` | `issue_tracking.py` | Issue number → Discord message ID |
| `data/posted_prs.json` | `github.py` | PR number → Discord message ID |
| `data/tickets.json` | `github.py` (TicketSystem) | Support tickets |
| `data/contributors.json` | `contributors.py` | Contributor records |

### 2.2 Schema Versioning

Every store has a `version` field. When the schema changes, write a migration:

```python
def _load_store(self):
    raw = json.loads(path.read_text())
    if isinstance(raw, list):
        # v1 → v2 migration
        self.store = {str(i): "UNVERIFIED" for i in raw}
        self._save_store()
    elif isinstance(raw, dict) and "issues" in raw:
        self.store = raw["issues"]
```

### 2.3 No Shared Mutable State

Cogs must not mutate each other's stores or caches. Each cog owns its data file exclusively. Cross-cog communication goes through **Discord channels** (messages, embeds) or through **shared env config** (`config.py`).

---

## 3. Crash Recovery — Assume Every Line Can Fail

### 3.1 Failure Classes

| Failure | Effect | Mitigation |
|---|---|---|
| Crash between `send()` and `_save_store()` | Post is lost | Next sync will re-post. Duplicate impossible. |
| Crash during `_save_store()` | Store is incomplete | Atomic `.tmp` + `rename()` prevents corruption. |
| Discord rate-limit (429) | Post is delayed | `aiohttp` handles retries; log and skip on persistent failure. |
| GitHub API timeout | Sync is skipped | Log error, retry on next loop iteration. |
| JSON file corruption on restart | Store is lost | Log warning, start fresh, re-post nothing. |

### 3.2 The `try/except` Boundaries

Every external call (Discord API, GitHub API, file I/O) must be wrapped:

```python
try:
    msg = await channel.send(embed=embed)
except discord.HTTPException as exc:
    logger.error("Failed to post: %s", exc)
    continue  # don't crash the whole sync
```

### 3.3 Atomic Writes

```python
def _save_store(self):
    tmp = self.store_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(self.store, indent=2))
    tmp.rename(self.store_file)  # atomic on POSIX
```

---

## 4. Adding a New Feature — Checklist

1. **Define the store schema** — what external ID maps to what Discord artifact?
2. **Add load/save helpers** — `_load_store()`, `_save_store()` with atomic writes.
3. **Add `on_ready` verification** — verify stored messages still exist.
4. **Guard every writer** — check store before posting, persist immediately after.
5. **Log every non-trivial action** — at minimum "Posted X", "Removed Y stale entries".
6. **Test the crash scenario** — kill the container, restart it, confirm no duplicates.
7. **Update this file** if you add a new pattern.

---

## 5. Logging Conventions

All cogs use `logging.getLogger("lila-bot.<cog_name>")`.

| Level | When to use |
|---|---|
| `ERROR` | Operation failed, data may be inconsistent |
| `WARNING` | Degraded but recoverable (corrupt store, stale entries) |
| `INFO` | Normal lifecycle events (cog loaded, X items posted) |
| `DEBUG` | Per-item details (not used currently) |

---

## 6. Contribution Tracker — Gamification Rules

### 6.1 Point Weights (defined in `config.POINTS`)

| Action | Points |
|--------|--------|
| PR merged | 10 |
| PR opened | 5 |
| Issue closed | 5 |
| Issue created | 2 |
| Comment on PR/issue | 1 |

Points are **recalculated from scratch** on every poll cycle (every 15 min). This prevents double-counting across restarts.

### 6.2 Role Ladder (defined in `config.ROLE_LADDER`)

| Role | Min Points | Discord Role Name |
|------|-----------|------------------|
| Contributor | 0 | `Contributor` |
| Active Contributor | 50 | `Active Contributor` |
| Core Contributor | 150 | `Core Contributor` |
| Maintainer Candidate | 300 | `Maintainer Candidate` |

When a user crosses a threshold:
1. The **old lower role is removed** (if exists)
2. The **new higher role is added**
3. An announcement is posted to `CONTRIBUTIONS_ANNOUNCE_CHANNEL_ID`

### 6.3 Milestones (defined in `config.MILESTONES`)

| Badge | Trigger | Display Name |
|-------|---------|-------------|
| Bronze | 10 PRs merged | 🥉 Bronze Contributor |
| Silver | 25 PRs merged | 🥈 Silver Contributor |
| Gold | 50 PRs merged | 🥇 Gold Contributor |
| Platinum | 100 total contributions | 💎 Platinum Contributor |

Milestones are detected automatically during polling and announced immediately. Badges must be claimed manually via `/claimbadge`.

### 6.4 Data Flow

```
GitHub REST API (every 15 min)
    → fetch all PRs (state=all, paginated)
    → fetch all issues (state=all, paginated)
    → match authors to linked Discord users
    → recalculate points from scratch
    → check role thresholds → update roles
    → check milestone thresholds → announce
    → persist to data/contribution_tracker.json
```

### 6.5 Commands

| Command | Permission | Ephemeral |
|---------|-----------|-----------|
| `/link <github_username>` | Everyone | Yes |
| `/mycontributions` | Everyone | Yes |
| `/leaderboard [page]` | Everyone | No |
| `/roleinfo` | Everyone | Yes |
| `/claimbadge <badge>` | Everyone | No |
| `/adjust-points <user> <points> <reason>` | Admin | Yes |
| `/sync-contributions` | Admin | Yes |

---

## 7. Deployment & Restarts

The bot runs in Docker with `--restart unless-stopped`.

- On container restart → `on_ready` fires → store verification runs → new issues are synced.
- On crash → Docker restarts automatically → same flow.
- On full host reboot → Docker daemon starts the container → same flow.

The invariant: **any number of restarts produces the same channel state as one clean run.**
