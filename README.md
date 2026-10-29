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
- Telegram identity: server-side Telegram Mini App initData HMAC validation and automatic signed-session restore
- TON wallet UI: TON Connect UI with a host-aware serverless manifest endpoint
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


## Automatic Telegram login and TON Connect

- On launch, the frontend first checks the signed HttpOnly session at `GET /api/me`; if it is missing, it authenticates fresh Telegram `initData` with `POST /api/auth/telegram`.
- TON Connect UI is loaded from a pinned CDN version. The manifest is served by `GET /api/tonconnect-manifest` using the deployed host.
- The current TON Connect integration connects/restores a wallet in the client. It does **not** prove wallet ownership to the backend, link the wallet to the user's account, or authorize payouts. Before enabling deposits, rewards or withdrawals, implement and verify TON Proof (nonce, domain, timestamp, signature and replay protection) server-side.
- The manifest currently uses the repository owner's GitHub avatar as a temporary PNG icon. Replace it with a PaidMX-owned 180x180 PNG icon before public launch.
