# PaidMX Firebase backend

Project: `paidmx`

## Architecture
- Static Telegram Mini App frontend: `web/` (deployable with Firebase Hosting or another static host).
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

The function validates Telegram initData (maximum age: 1 hour), creates/updates the Telegram user profile transactionally, rejects accounts marked `banned`, and exposes an `authCheck` handshake. Other RPC methods intentionally return `501 rpc_not_migrated`; no fake success responses are returned.

### OfferwallApi rewards (backend foundation)
- Configure the provider postback URL as `https://us-central1-paidmx.cloudfunctions.net/api/offerwallapi/postback`.
- Store the OfferwallApi Secret Key with `firebase functions:secrets:set OFFERWALLAPI_SECRET`; never place it in frontend code.
- The endpoint verifies `signature2` (HMAC-SHA256) and supports the legacy MD5 signature, ignores provider test callbacks, deduplicates by `transId`, and handles chargebacks idempotently.
- Credits are written to `wallets/{telegramUserId}` as integer `balanceMicros` (1 PMX = 1,000,000 micros) with `debtMicros` for chargebacks that exceed the available balance. Every callback is recorded in `providerTransactions`.
- This webhook is only the provider-to-server crediting foundation. The `web/` directory now contains a responsive Telegram Mini App dashboard, wallet overview, task placeholder, and referral screen. The frontend calls the authenticated `getDashboard` RPC. OfferwallApi feed/launch, real task catalog, transaction history, and withdrawal RPCs are still not implemented; do not enable earning/withdrawals in production yet.
- Test callback URL with the provider's integration tester; test events are acknowledged but never credited.

## Local checks
From the `functions` directory, run `npm test` to execute the dependency-free Node.js test suite, or `npm run check` to run syntax checks and tests together. The OfferwallApi helper tests cover integer reward conversion, invalid decimal rejection, HMAC-SHA256 verification, legacy MD5 compatibility, and tampered signatures. Firestore transaction and provider sandbox tests are still required before production.

## Security
- Firestore client reads and writes are denied globally. Cloud Functions use the Admin SDK.
- Never put `BOT_TOKEN`, service-account private keys, or other secrets in Stormkit frontend variables or the browser bundle.
- `apiKey` in the Firebase web config is a public client identifier, not an authorization control.
- All balance, reward, game score, referral, task, promo, withdrawal, and admin operations must be validated server-side and use Firestore transactions/idempotency.
- Admin UI visibility is not authorization. Configure the comma-separated `ADMIN_IDS` server environment variable and check it on every admin RPC; the source code no longer contains a default administrator ID.

## Stormkit frontend variables
After the backend RPC migration and deployment, set:
```env
VITE_API_URL=https://us-central1-paidmx.cloudfunctions.net/api
```
The current frontend still uses the legacy Telegram Serverless RPC bridge; it must be migrated to `fetch(VITE_API_URL)` before production cutover.

## Continuous integration
GitHub Actions runs Node.js 22 syntax checks and the built-in test suite whenever backend files change on `main` or in a pull request. Telegram initData verification is isolated in `functions/lib/telegram-auth.js` and covered by tests for valid signatures, tampering, expired/future timestamps, malformed identities, and missing bot-token configuration.

## Telegram Mini App frontend
- Frontend source: `web/index.html`, `web/styles.css`, and `web/app.js`.
- Public settings: edit `web/config.js` and set `botUsername` to the bot username without `@`. Never put bot tokens or provider secrets in this file.
- Configure the Telegram bot domain with BotFather `/setdomain`, then set the Mini App URL/menu button to the deployed HTTPS frontend URL.
- The frontend sends the raw `Telegram.WebApp.initData` in the `X-Telegram-Init-Data` header. The server verifies its signature and freshness; client-side `initDataUnsafe` is not trusted for authentication.
- The referral link format is `https://t.me/<bot>?startapp=ref_<code>`. Referral attribution is accepted only on a user's first authenticated registration, resolved server-side through `referralCodes`, and recorded once in `referrals/{telegramUserId}`. Self-referrals and banned referrers are ignored. Referral count is tracked; monetary referral rewards are intentionally not enabled until a reward policy is configured.
- Firebase Hosting is configured to serve the `web/` directory. After creating/enabling the Hosting site and setting `CORS_ORIGINS` to the exact deployed origin, deploy with `firebase deploy --project paidmx --only hosting`.
- The frontend currently shows task and withdrawal sections as unavailable rather than pretending those backend systems are active.


## OfferwallApi kısa görev akışı

PaidMX'in kendi görev kartları OfferwallApi REST feed'lerinden veri alır. Şu an yalnızca kısa süreli PTC reklamları (en fazla 180 saniye), video izleme ve shortlink görevleri gösterilir. Uygulama indirme/yükleme, kayıt, deneme, abonelik ve para yatırma ifadeleri içeren kampanyalar filtrelenir. Uzun/kanıt gerektiren Microtasks ve yüksek değerli Offers feed'i bu kısa görev ekranına dahil değildir.

API Key ve Bearer Token yalnızca Firebase Functions Secret Manager'da tutulmalıdır; web/config.js içine yazılmamalıdır:

```bash
firebase functions:secrets:set OFFERWALLAPI_KEY
firebase functions:secrets:set OFFERWALLAPI_BEARER
firebase functions:secrets:set OFFERWALLAPI_SECRET
firebase deploy --only functions
```

OfferwallApi panelindeki API Key, Bearer Token ve Secret Key değerlerini ilgili komutlar sorunca gir. API Key ve Bearer Token görev akışını; Secret Key ise doğrulanmış S2S ödül postback'lerini kullanır. Web arayüzü `getQuickTasks` RPC'siyle görevleri alır; görev URL'leri sağlayıcı tarafından oluşturulur ve kullanıcı kimliği URL'ye önceden eklenmiştir. Ödül yalnızca imzası doğrulanmış postback ile cüzdana işlenir.

Kampanya metni filtreleri ek bir korumadır; sağlayıcının kampanya açıklamalarını her zaman doğru sınıflandıracağını garanti etmez. Panelden uygulama indirme, kayıt, satın alma, deneme ve depozitolu kampanya kategorilerini ayrıca kapat.
