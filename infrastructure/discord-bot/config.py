"""LILA Lab Discord Bot Configuration."""

import os

from dotenv import load_dotenv

load_dotenv()

# Bot Settings
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
BOT_PERMISSIONS = 8866461766385655  # Permission integer for OAuth2 URL

# Channel IDs
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "0"))
ANNOUNCEMENTS_CHANNEL_ID = int(os.getenv("ANNOUNCEMENTS_CHANNEL_ID", "0"))
GENERAL_CHANNEL_ID = int(os.getenv("GENERAL_CHANNEL_ID", "0"))
RESEARCH_CHANNEL_ID = int(os.getenv("RESEARCH_CHANNEL_ID", "0"))
CONTRIBUTIONS_CHANNEL_ID = int(os.getenv("CONTRIBUTIONS_CHANNEL_ID", "0"))
SUPPORT_CHANNEL_ID = int(os.getenv("SUPPORT_CHANNEL_ID", "0"))
JOBS_CHANNEL_ID = int(os.getenv("JOBS_CHANNEL_ID", "0"))
ISSUE_TRACKING_CHANNEL_ID = int(os.getenv("ISSUE_TRACKING_CHANNEL_ID", "0"))
PR_REVIEW_CHANNEL_ID = int(os.getenv("PR_REVIEW_CHANNEL_ID", "0"))
CONTRIBUTIONS_ANNOUNCE_CHANNEL_ID = int(os.getenv("CONTRIBUTIONS_ANNOUNCE_CHANNEL_ID", "0"))

# Role Names (must match Discord server roles)
ROLES = {
    "newcomer": "Newcomer",
    "visitor": "Visitor",
    "contributor": "Contributor",
    "active_contributor": "Active Contributor",
    "core_contributor": "Core Contributor",
    "maintainer_candidate": "Maintainer Candidate",
    "annotator": "Annotator",
    "researcher": "Researcher",
    "admin": "Admin",
}

# Contribution Points per Action
POINTS = {
    "pr_merged": 10,
    "pr_opened": 5,
    "issue_closed": 5,
    "issue_created": 2,
    "comment": 1,
}

# Role Ladder: (role_name_key, min_points)
# Roles are assigned in ascending order — crossing a threshold promotes the user.
ROLE_LADDER = [
    ("contributor", 0),
    ("active_contributor", 50),
    ("core_contributor", 150),
    ("maintainer_candidate", 300),
]

# Milestones: triggered when a user hits the required count
MILESTONES = {
    "bronze": {"name": "🥉 Bronze Contributor", "prs_merged": 10},
    "silver": {"name": "🥈 Silver Contributor", "prs_merged": 25},
    "gold": {"name": "🥇 Gold Contributor", "prs_merged": 50},
    "platinum": {"name": "💎 Platinum Contributor", "total_contributions": 100},
}

# Language Roles (for self-assignment)
LANGUAGE_ROLES = [
    "Bangla Speaker",
    "Assamese Speaker",
    "Nepali Speaker",
    "Sylheti Speaker",
    "Chittagonian Speaker",
    "Hindi Speaker",
    "English Speaker",
]

# Contribution Roles
CONTRIBUTION_ROLES = [
    "Linguist",
    "NLP Researcher",
    "Economist",
    "Data Scientist",
    "Student",
    "Policy Researcher",
]

# Resource Links
RESOURCES = {
"collaboration": "https://github.com/LilaLABx/LILA-LAB/blob/main/COLLABORATION.md",
        "contribution_guide": "https://github.com/LilaLABx/LILA-LAB/blob/main/CONTRIBUTING.md",
        "linguistic_guide": "https://github.com/LilaLABx/LILA-LAB/blob/main/LINGUISTIC_CONTRIBUTION_GUIDE.md",
        "extension_template": "https://github.com/LilaLABx/LILA-LAB/blob/main/technical-reports/extensions/EXTENSION_TEMPLATE.md",
        "github": "https://github.com/LilaLABx/LILA-LAB",
    "website": "https://lila-lab.org",
    "osf": "https://osf.io/",
    "huggingface": "https://huggingface.co/nabil0x",
}

# Welcome Message
WELCOME_MESSAGE = """
Welcome to **LILA Lab**, {user.mention}! :wave:

**Language Intelligence for Low-resource Applications**

We're a research collective building NLP infrastructure for languages underserved by current AI.

**Getting Started:**
1. Read <#{collaboration_channel}> to understand how to contribute
2. Introduce yourself in <#{general_channel}>
3. Choose your roles using `/roles` command

**Quick Links:**
:link: <{collaboration}>
:link: <{contribution_guide}>
:link: <{github}>

**Your first steps:**
- Say hello in <#{general_channel}>
- React to this message to get your **Newcomer** role
- Use `/help` to see all available commands
"""

# Help Text
HELP_TEXT = """
**LILA Lab Bot Commands**

**General:**
- `/help` - Show this help message
- `/about` - About LILA Lab
- `/resources` - Get contribution resources

**Roles:**
- `/roles` - Self-assign language and contribution roles
- `/remove-role <role>` - Remove a role from yourself

**Community:**
- `/contribute` - How to contribute to LILA Lab
- `/languages` - See which languages need speakers
- `/extensions` - View extension proposals

**Moderation (Admin only):**
- `/announce <message>` - Send announcement to #announcements
- `/pin <message_id>` - Pin a message
- `/cleanup <amount>` - Delete messages (1-100)

**Need help?** Open a ticket in <#support> or email lila.lab0x@gmail.com
"""

# About Text
ABOUT_TEXT = """
**LILA Lab** - Language Intelligence for Low-resource Applications

**Mission:** Building NLP measurement infrastructure for languages underserved by current AI.

**Pipelines:**
- **BENI** - Bangla Exploration & Native-language Intelligence
- **AENI** - Assamese Exploration & Native-language Intelligence (coming soon)
- **NENI** - Nepali Exploration & Native-language Intelligence (planned)

**Research Focus:**
- Economic narrative indices for low-resource languages
- LLM-assisted annotation and validation
- Cross-language comparative analysis

**Founder:** Ann Naser Nabil (Jahangirnagar University)

**Connect:**
:link: GitHub: <{github}>
:link: Website: <{website}>
:link: OSF: <{osf}>
:link: Hugging Face: <{huggingface}>
"""
