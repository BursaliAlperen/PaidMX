# PaidMX

PaidMX is a Telegram Mini App starter for a rewards experience.

## First-run flow

1. Welcome screen
2. Choose one of nine languages
3. Choose a color theme
4. Enter the app

Languages: Türkçe, English, العربية, Русский, Español, Português, हिन्दी, Bahasa Indonesia and 中文.

Themes: Midnight, Ocean, Emerald, Rose, Violet and Sunset.

The interface is original and borrows only the broad design language of modern rewards dashboards.

## Stack

- Static frontend: HTML, CSS and JavaScript
- Serverless API: Vercel Functions, Node.js 20+
- Telegram identity: server-side Telegram Mini App initData HMAC validation
- Storage: PostgreSQL via Neon serverless driver

## Local setup

1. Install Node.js 20+.
2. Run `npm install`.
3. Copy `.env.example` to `.env` and configure `BOT_TOKEN`, `SESSION_SECRET` (at least 32 characters) and `DATABASE_URL`.
4. Run `database/schema.sql` once against your PostgreSQL/Neon database.
5. Start API routes with `npx vercel dev`.
6. Run `npm run check`.

Opening the static HTML as a file is for UI preview only; API authentication and persisted preferences require Vercel dev or deployment.

## Telegram setup

1. Configure your bot with BotFather and set the deployed HTTPS Mini App URL.
2. Add `BOT_TOKEN`, `SESSION_SECRET` and `DATABASE_URL` as server-side Vercel environment variables.
3. Run the database schema once.
4. Deploy and configure the bot's Menu Button / Mini App URL.

Never put the bot token or database URL into frontend code or commit real secrets.

## Status and limitations

This is the first implementation scaffold. Reward-ad providers, server-side ad callbacks, fraud controls, payout provider, wallet network and withdrawal thresholds are not configured. The demo UI does not credit points or claim to pay users. Do not represent a reward or withdrawal as live until the corresponding trusted provider and server-side validation are integrated.
