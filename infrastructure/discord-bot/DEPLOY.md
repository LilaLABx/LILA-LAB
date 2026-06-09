# Deploy LILA Lab Discord Bot

## Option 1: Fly.io (Recommended — Free Docker Hosting)

### Prerequisites
- [Fly.io account](https://fly.io) (free, no credit card)
- Git installed

### Steps

```bash
# 1. Install Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth signup  # or fly auth login

# 3. Navigate to bot directory
cd infrastructure/discord-bot

# 4. Launch app (first time only)
fly launch

# 5. Set secrets
fly secrets set DISCORD_TOKEN=your_token_here
fly secrets set GUILD_ID=1514006930769707071

# 6. Deploy
fly deploy

# 7. Check logs
fly logs
```

### Verify Bot is Running

```bash
fly status
fly logs --tail
```

---

## Option 2: Lunafy (Free, No Docker)

1. Go to [panel.lunafy.run](https://panel.lunafy.run)
2. Create account
3. Upload bot files (ZIP or Git)
4. Add environment variables:
   - `DISCORD_TOKEN`
   - `GUILD_ID`
5. Start server

---

## Option 3: JustRunMy.App (Free Docker)

1. Go to [justrunmy.app](https://justrunmy.app)
2. Sign up
3. Deploy via Docker (this repo has a Dockerfile)
4. Add secrets in dashboard

---

## Troubleshooting

### Bot not responding?
1. Check logs: `fly logs` (Fly.io)
2. Verify token is correct
3. Check bot has permissions in server
4. Ensure bot is invited with correct permissions: `8866461766385655`

### Permission errors?
Re-invite bot with this URL (replace YOUR_CLIENT_ID):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8866461766385655&scope=bot%20applications.commands
```
