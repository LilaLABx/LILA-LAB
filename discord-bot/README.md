# LILA Lab Discord Bot

A Discord bot for managing the LILA Lab research community.

**Language Intelligence for Low-resource Applications**

---

## Features

### Welcome & Onboarding
- Automatic role assignment on join (`Newcomer`)
- Welcome message with resources
- DM with detailed getting started guide
- Self-service role selection (`/roles`)

### Utility Commands
- `/help` - Show all available commands
- `/about` - About LILA Lab
- `/resources` - Get contribution resource links
- `/contribute` - Learn how to contribute
- `/languages` - See which languages need speakers
- `/extensions` - View extension proposals
- `/stats` - Show community statistics

### Moderation (Admin only)
- `/announce` - Send announcements
- `/pin` - Pin messages
- `/cleanup` - Delete messages (1-100)
- `/timeout` - Timeout members
- `/kick` - Kick members
- `/ban` - Ban members
- `/slowmode` - Set channel slowmode

---

## Setup

### Prerequisites
- Python 3.10+
- Discord account
- Discord server with admin permissions

### Step 1: Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Name it **LILA Lab Bot**
4. Go to **Bot** tab
5. Click **Add Bot**
6. Under **Privileged Gateway Intents**, enable:
   - **Message Content Intent**
   - **Server Members Intent**
   - **Presence Intent**
7. Copy the **Bot Token** (keep this secret!)

### Step 2: Invite Bot to Server

1. Go to **OAuth2 > URL Generator**
2. Under **Scopes**, select:
   - `bot`
   - `applications.commands`
3. Under **Bot Permissions**, select:
   - **General:**
     - View Channels
     - Send Messages
     - Embed Links
     - Attach Files
     - Read Message History
     - Add Reactions
     - Use External Emojis
     - Change Nickname
   - **Text:**
     - Send Messages in Threads
     - Create Public Threads
     - Create Private Threads
     - Manage Messages
     - Manage Threads
     - Read Message History
     - Send Messages
     - Use External Emojis
     - Use External Stickers
     - Add Reactions
     - Embed Links
     - Attach Files
   - **Voice:**
     - Connect
     - Speak
4. Copy the generated URL
5. Open URL in browser and add bot to your server

### Step 3: Configure Bot

1. Copy `.env.example` to `.env`
2. Fill in your bot token and server ID:

```bash
cp .env.example .env
```

Edit `.env`:
```
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here
```

**To find your Server ID:**
1. Enable Developer Mode in Discord (Settings > Advanced > Developer Mode)
2. Right-click your server icon
3. Click **Copy Server ID**

### Step 4: Create Server Roles

Create these roles in your Discord server (Settings > Roles):

**Hierarchy Roles:**
- `Newcomer` (lowest)
- `Contributor`
- `Annotator`
- `Researcher`
- `Admin` (highest)

**Language Roles:**
- `Bangla Speaker`
- `Assamese Speaker`
- `Nepali Speaker`
- `Sylheti Speaker`
- `Chittagonian Speaker`
- `Hindi Speaker`
- `English Speaker`

**Contribution Roles:**
- `Linguist`
- `NLP Researcher`
- `Economist`
- `Data Scientist`
- `Student`
- `Policy Researcher`

### Step 5: Create Channels

Create these channels in your server:

**Information:**
- `#welcome` - New member greeting
- `#announcements` - Read-only announcements
- `#rules` - Server rules

**Community:**
- `#general` - General discussion
- `#introductions` - New member introductions
- `#support` - Help and support

**Research:**
- `#linguistic-data` - Annotation coordination
- `#pipelines` - Technical discussion
- `#extensions` - Extension proposals
- `#paper-writing` - Drafting and review

**Events:**
- `#monthly-lab-call` - Call coordination

### Step 6: Update Channel IDs

After creating channels, update `.env` with channel IDs:

```
WELCOME_CHANNEL_ID=123456789012345678
ANNOUNCEMENTS_CHANNEL_ID=123456789012345678
GENERAL_CHANNEL_ID=123456789012345678
```

**To find Channel IDs:**
1. Enable Developer Mode (Settings > Advanced > Developer Mode)
2. Right-click the channel
3. Click **Copy Channel ID**

### Step 7: Install and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

---

## Deployment

### Option 1: Local (Development)

```bash
python bot.py
```

Bot runs until you stop it (Ctrl+C).

### Option 2: Always-On (Recommended)

Use a VPS or cloud service:

**Railway (Free tier available):**
1. Push code to GitHub
2. Connect repo to Railway
3. Add environment variables
4. Deploy

**Render (Free tier available):**
1. Push code to GitHub
2. Create new Web Service
3. Select Python
4. Add start command: `python bot.py`
5. Add environment variables

**Oracle Cloud Free Tier:**
1. Create Ubuntu instance
2. Install Python
3. Clone repo
4. Use systemd to run bot as service

### Option 3: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t lila-bot .
docker run -d --name lila-bot --env-file .env lila-bot
```

---

## Commands Reference

### General Commands
| Command | Description | Permission |
|---------|-------------|------------|
| `/help` | Show all commands | Everyone |
| `/about` | About LILA Lab | Everyone |
| `/resources` | Get resource links | Everyone |
| `/stats` | Show statistics | Everyone |

### Role Commands
| Command | Description | Permission |
|---------|-------------|------------|
| `/roles` | Self-assign roles | Everyone |
| `/remove-role <role>` | Remove a role | Everyone |

### Contribution Commands
| Command | Description | Permission |
|---------|-------------|------------|
| `/contribute` | How to contribute | Everyone |
| `/languages` | Languages needing speakers | Everyone |
| `/extensions` | Extension proposals | Everyone |

### Moderation Commands
| Command | Description | Permission |
|---------|-------------|------------|
| `/announce <message>` | Send announcement | Admin |
| `/pin <message_id>` | Pin a message | Admin |
| `/cleanup <amount>` | Delete messages | Admin |
| `/timeout <member> <minutes>` | Timeout member | Admin |
| `/untimeout <member>` | Remove timeout | Admin |
| `/kick <member>` | Kick member | Admin |
| `/ban <member>` | Ban member | Admin |
| `/slowmode <seconds>` | Set slowmode | Admin |

---

## Customization

### Adding New Commands

1. Open relevant cog file in `cogs/`
2. Add new command:

```python
@app_commands.command(name="newcommand", description="Description")
async def new_command(self, interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")
```

### Adding New Roles

1. Edit `config.py`:
```python
LANGUAGE_ROLES.append("New Language Speaker")
```

2. Create role in Discord server

### Changing Welcome Message

Edit `WELCOME_MESSAGE` in `config.py`.

---

## Troubleshooting

### Bot doesn't respond
- Check bot token is correct
- Ensure bot is online (check Developer Portal)
- Verify bot has necessary permissions

### Commands not syncing
- Wait a few minutes after starting bot
- Check console for sync errors
- Ensure `applications.commands` scope was included in invite

### Bot can't send messages
- Verify bot has `Send Messages` permission
- Check channel permissions
- Ensure bot role is above target role

### Bot can't assign roles
- Verify bot role is higher than roles it's assigning
- Check bot has `Manage Roles` permission

---

## Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers)
- [LILA Lab GitHub](https://github.com/nabil0x/economic-narrative-indices)
- [LILA Lab Website](https://lila-lab.org)

---

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

## Support

For issues or questions:
- Open a GitHub Issue
- Email: ann.n.nabil@gmail.com
- Discord: #support channel
