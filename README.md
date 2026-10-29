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
- Serverless API: Stormkit Cloud Node.js functions in the top-level `api/` directory, with `lib/stormkit-compat.js` adapting native Node request/response objects
- Telegram identity: server-side Telegram Mini App initData HMAC validation and automatic signed-session restore
- TON wallet UI: TON Connect UI with a host-aware serverless manifest endpoint
- Storage: PostgreSQL via Neon serverless driver

## Local setup

1. Use Node.js 22 LTS (pinned by `mise.toml`, `.node-version` and `package.json`).
2. Run `npm install`.
3. Copy `.env.example` to `.env` and configure `BOT_TOKEN`, `ADMIN_IDS`, `SESSION_SECRET` (at least 32 characters), `DATABASE_URL`, `PUBLIC_APP_URL`, and `TELEGRAM_WEBHOOK_SECRET`.
4. Run `database/schema.sql`, then `database/migration-001-referrals-admin.sql` against your PostgreSQL/Neon database.
5. Run `npm run check`, `npm test`, or `npm run build`.
6. Deploy using Stormkit with its Serverless option enabled and API Folder set to `api`.

Opening the static HTML as a file is for UI preview only; authentication, webhook, referral, admin and database APIs require the Stormkit serverless runtime.

## Telegram setup

1. Configure your bot with BotFather and set the deployed HTTPS Mini App URL.
2. In Stormkit, open **PaidMX → production → Config → Environment Variables** and add `BOT_TOKEN`, `ADMIN_IDS`, `SESSION_SECRET`, `DATABASE_URL`, `PUBLIC_APP_URL` and `TELEGRAM_WEBHOOK_SECRET`. Add `PAYMENT_WEBHOOK_SECRET` only after a real payment provider is integrated.
3. Run `database/schema.sql`, then `database/migration-001-referrals-admin.sql` against the same PostgreSQL database.
4. Deploy the app and set the Telegram bot's Menu Button / Mini App URL to `PUBLIC_APP_URL`.
5. Register the Telegram webhook once from a trusted terminal where `BOT_TOKEN`, `PUBLIC_APP_URL` and `TELEGRAM_WEBHOOK_SECRET` are available:
   `curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" -d "url=${PUBLIC_APP_URL}/api/telegram/webhook" -d "secret_token=${TELEGRAM_WEBHOOK_SECRET}"`

Never put the bot token or database URL into frontend code or commit real secrets.

## Status and limitations

This is the first implementation scaffold. Reward-ad providers, server-side ad callbacks, fraud controls, payout provider, wallet network and withdrawal thresholds are not configured. The demo UI does not credit points or claim to pay users. Do not represent a reward or withdrawal as live until the corresponding trusted provider and server-side validation are integrated.


## Automatic Telegram login and TON Connect

- On launch, the frontend first checks the signed HttpOnly session at `GET /api/me`; if it is missing, it authenticates fresh Telegram `initData` with `POST /api/auth/telegram`.
- TON Connect UI is loaded from a pinned CDN version. The manifest is served by `GET /api/tonconnect-manifest` using the deployed host.
- The current TON Connect integration connects/restores a wallet in the client. It does **not** prove wallet ownership to the backend, link the wallet to the user's account, or authorize payouts. Before enabling deposits, rewards or withdrawals, implement and verify TON Proof (nonce, domain, timestamp, signature and replay protection) server-side.
- The manifest currently uses the repository owner's GitHub avatar as a temporary PNG icon. Replace it with a PaidMX-owned 180x180 PNG icon before public launch.

## Referral, Telegram bot and admin operations

The operational scaffold adds these routes:

- `POST /api/telegram/webhook`: handles private-chat `/start`, sends a localized welcome message in the Telegram user's language, and attributes a valid `ref_<telegram_id>` start parameter.
- `GET /api/referral`: returns the signed-in user's referral counts.
- `GET /api/admin/overview`: admin-only counts, latest users, referral records and payment-event history.
- `POST /api/admin/notify`: admin-only manual event recording plus a Telegram notification.
- `POST /api/payments/webhook`: idempotent normalized payment-event intake, user notification and admin alerts. It requires `x-paidmx-webhook-secret` to match `PAYMENT_WEBHOOK_SECRET`.

### Required setup

1. Apply `database/schema.sql`, then run `database/migration-001-referrals-admin.sql` against the same PostgreSQL database.
2. Configure server-side environment variables: `BOT_TOKEN`, `SESSION_SECRET` (32+ characters), `DATABASE_URL`, `TELEGRAM_WEBHOOK_SECRET`, `PUBLIC_APP_URL`, and `ADMIN_IDS` (comma-separated numeric Telegram IDs). Never expose these values in frontend code.
3. Configure the Telegram webhook using a random secret token. Example from a trusted terminal where the environment variables are set:
   ```sh
   curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
     -d "url=${PUBLIC_APP_URL}/api/telegram/webhook" \
     -d "secret_token=${TELEGRAM_WEBHOOK_SECRET}"
   ```
4. Open `/admin.html` from the deployed domain after signing in through the Telegram Mini App. The signed-in Telegram ID must be included in `ADMIN_IDS`. The server validates admin access; hiding the page is not the security boundary.
5. For automatic payment notifications, configure the chosen payment provider's server-side adapter to call `/api/payments/webhook` with the normalized event fields `eventId`, `provider`, `telegramId`, `eventType`, `amount`, `currency`, and optional `note`, plus the secret header. The event ID must be stable and unique per provider event. This endpoint logs and notifies; it deliberately does **not** credit balances or transfer money. Provider-specific signature validation and settlement rules must be added for the actual provider before real funds are handled.

## Deploying and fixing Stormkit's “Repository is inaccessible” error

That message is a GitHub authorization/repository visibility problem; it is not proof of a source-code or build error. In Stormkit, open the app's Git integration/settings and reconnect GitHub, then ensure the GitHub App installation has access to `BursaliAlperen/PaidMX`. If the repository is private, explicitly grant that repository to the installation. Refresh the app and retry the deployment after the repository is visible. Do not paste access tokens into chat.

PaidMX is configured for Stormkit Cloud serverless. The API files in the top-level `api/` directory export Node.js handlers through `lib/stormkit-compat.js`, which parses JSON bodies and adapts `res.status(...).json(...)` to Stormkit's native response stream. In Stormkit's **production → Config** screen set **Build command** to `npm run build`, **Output folder** to `public`, enable **Serverless**, and set **API Folder** to `api`. Stormkit's environment-variable settings are available to serverless functions at runtime. A static-only deployment will serve the interface but will not run authentication, Telegram webhook, referral, admin or payment APIs. The retained `vercel.json` is optional legacy configuration and is not the Stormkit API router.

## Important production boundaries

- Referral attribution is recorded, but automatic referral rewards are not enabled; qualification and anti-fraud rules must be defined before crediting points.
- The admin event form is a manual audit/notification tool, not a payment processor.
- The normalized payment webhook is an integration boundary. A provider-specific signature/identity check and idempotent settlement logic must be verified before accepting real payment callbacks.
- TON Connect is currently a client wallet connection only. Do not enable withdrawals until TON Proof verification, payout ledger rules, and provider-specific settlement checks are implemented.
- Run `npm run check` and `npm test` after environment and database setup. A successful Git commit does not mean a deployment or live Telegram webhook has been verified.
