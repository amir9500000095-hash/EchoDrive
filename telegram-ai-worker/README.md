# Telegram AI Worker (Python + Cloudflare Workers)

This project is intentionally added as a subdirectory of EchoDrive. The existing root README and audio-game project are left untouched.

## Current scope

- Telegram HTTPS webhook with Telegram's X-Telegram-Bot-Api-Secret-Token verification.
- Persian-friendly assistant using the optional Cloudflare Workers AI binding.
- Minimal per-user memory in KV with /memory and /forget commands.
- Telegram media updates (photo, video, audio, voice, document, sticker) acknowledged with a concise description; files are not downloaded by default.
- Admin-only /status command guarded by a numeric Telegram user ID allowlist.
- D1 schema and Cron handler foundation. Reminder delivery is not enabled in this starter yet.
- No tokens, API keys, or real credentials are stored in Git.

## Requirements

- Cloudflare account with Workers enabled.
- A Telegram bot token created through BotFather.
- Workers AI enabled if AI replies are wanted.
- A KV namespace for short memory.
- A D1 database for reminders (optional until reminder commands are implemented).

## Configure

1. Create a KV namespace, then replace REPLACE_WITH_KV_NAMESPACE_ID in wrangler.toml.
2. Create a D1 database and replace REPLACE_WITH_D1_DATABASE_ID in wrangler.toml. Apply schema.sql using Wrangler D1 from this directory.
3. Set these secrets from a trusted terminal:

    npx wrangler secret put TELEGRAM_BOT_TOKEN
    npx wrangler secret put TELEGRAM_WEBHOOK_SECRET
    npx wrangler secret put ADMIN_USER_IDS

ADMIN_USER_IDS is a comma-separated list of Telegram numeric user IDs. Do not put real values in this repository.

4. Install Python Workers tooling as described in Cloudflare's official Python Workers docs, then run local development and tests. This project requires the python_workers compatibility flag.
5. Deploy only after replacing all binding placeholders and reviewing Cloudflare dashboard permissions.

## Set Telegram webhook

After deploying, set the webhook from a trusted local terminal. Do not paste the token into chat or commit it. Set TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET, and WORKER_URL in your local shell, then run:

    python -c 'import json,os,urllib.request; token=os.environ["TELEGRAM_BOT_TOKEN"]; body=json.dumps({"url":os.environ["WORKER_URL"].rstrip("/")+"/telegram/webhook","secret_token":os.environ["TELEGRAM_WEBHOOK_SECRET"],"allowed_updates":["message","callback_query"]}).encode(); req=urllib.request.Request("https://api.telegram.org/bot"+token+"/setWebhook", data=body, headers={"Content-Type":"application/json"}); print(urllib.request.urlopen(req).read().decode())'

Unset those shell variables after use. Verify webhook status with Telegram's getWebhookInfo endpoint from the same trusted terminal. Avoid sharing its output if it includes private operational details.

## Commands

- /start — welcome and command list
- /help — help
- /memory — show saved memory
- /remember text — save a short memory
- /forget — delete saved memory
- /status — admin-only health summary

## Security notes

- The webhook secret is checked before parsing the update.
- Admin IDs must be explicitly configured; an unset allowlist grants no admin privileges.
- Do not execute generated code in the production Worker. A future self-development agent should create a branch/PR, run tests in separate CI, and require human approval before deployment.
- This starter does not yet execute arbitrary generated code, modify its own production deployment, or expose admin secrets.
- Never log bot tokens, API keys, full message contents, or webhook headers.
