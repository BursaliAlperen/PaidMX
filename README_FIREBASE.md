# PaidMX Firebase backend

Project: `paidmx`

## Architecture
- Stormkit: static frontend hosting only.
- Firebase Cloud Functions (Node.js 22): HTTPS API.
- Cloud Firestore: only database.
- Telegram Mini App: sends raw `Telegram.WebApp.initData` to the API.
- No SQLite, tgcloud runtime, Stormkit serverless API, or Firebase Hosting.

## Current migration status
This branch contains the Firebase project scaffold, deny-by-default Firestore rules, and the first HTTPS API foundation. The legacy RPC endpoints have **not** all been migrated yet. Do not point the production frontend at this API until the remaining RPC methods are implemented and tested.

## Firebase setup
1. Install Node.js 22 and Firebase CLI.
2. Run `firebase login`.
3. From this repository run `npm --prefix functions install`.
4. Create the Firestore database in project `paidmx` (choose a region deliberately; Firestore location cannot be changed later).
5. Set the Telegram bot token as a Firebase secret: `firebase functions:secrets:set BOT_TOKEN`.
6. Set the allowed Stormkit frontend origin as a non-secret environment variable named `CORS_ORIGINS` for the function runtime. Use the exact deployed frontend origin, without a trailing slash.
7. Deploy only after review: `firebase deploy --project paidmx --only firestore:rules,functions`.

## API
After deployment in `us-central1`:
- Base URL: `https://us-central1-paidmx.cloudfunctions.net/api`
- Health check: `GET /health`
- Authenticated POST requests must include `X-Telegram-Init-Data: <Telegram.WebApp.initData>`.
- JSON request shape: `{ "rpc": "methodName", "payload": { ... } }`.

The function currently validates Telegram initData, creates/updates the Telegram user profile transactionally, and exposes an `authCheck` handshake. Other RPC methods intentionally return `501 rpc_not_migrated`; no fake success responses are returned.

## Security
- Firestore client reads and writes are denied globally. Cloud Functions use the Admin SDK.
- Never put `BOT_TOKEN`, service-account private keys, or other secrets in Stormkit frontend variables or the browser bundle.
- `apiKey` in the Firebase web config is a public client identifier, not an authorization control.
- All balance, reward, game score, referral, task, promo, withdrawal, and admin operations must be validated server-side and use Firestore transactions/idempotency.
- Admin UI visibility is not authorization. Every admin RPC must check Telegram user ID `7904032877` on the server.

## Stormkit frontend variables
After the backend RPC migration and deployment, set:
```env
VITE_API_URL=https://us-central1-paidmx.cloudfunctions.net/api
```
The current frontend still uses the legacy Telegram Serverless RPC bridge; it must be migrated to `fetch(VITE_API_URL)` before production cutover.
