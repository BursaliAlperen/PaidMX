#!/usr/bin/env bash
set -Eeuo pipefail

# Run from the repository root in Stormkit's protected build environment.
# Required Stormkit server-side environment variables:
#   FIREBASE_SERVICE_ACCOUNT_JSON  Full service-account JSON (secret)
#   BOT_TOKEN                      Telegram bot token (secret)
#   ADMIN_IDS                      Comma-separated Telegram numeric IDs
#   CORS_ORIGINS                   Comma-separated exact frontend origins
#
# Never prefix secrets with VITE_ and never print their values.

: "${FIREBASE_SERVICE_ACCOUNT_JSON:?Missing FIREBASE_SERVICE_ACCOUNT_JSON}"
: "${BOT_TOKEN:?Missing BOT_TOKEN}"
: "${ADMIN_IDS:?Missing ADMIN_IDS}"
: "${CORS_ORIGINS:?Missing CORS_ORIGINS}"

PROJECT_ID="paidmx"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FUNCTIONS_DIR="$ROOT_DIR/functions"
TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
  rm -f "$FUNCTIONS_DIR/.env.paidmx"
}
trap cleanup EXIT

umask 077
printf '%s' "$FIREBASE_SERVICE_ACCOUNT_JSON" > "$TMP_DIR/firebase-service-account.json"
printf '%s' "$BOT_TOKEN" > "$TMP_DIR/bot-token"

export GOOGLE_APPLICATION_CREDENTIALS="$TMP_DIR/firebase-service-account.json"

# Runtime configuration is generated only for deployment and removed afterwards.
# BOT_TOKEN is uploaded separately to Secret Manager, never written to dotenv.
printf 'ADMIN_IDS="%s"\nCORS_ORIGINS="%s"\n' "$ADMIN_IDS" "$CORS_ORIGINS" > "$FUNCTIONS_DIR/.env.paidmx"

cd "$ROOT_DIR"
npx --yes firebase-tools@latest functions:secrets:set BOT_TOKEN \
  --data-file "$TMP_DIR/bot-token" --project "$PROJECT_ID" --force

npx --yes firebase-tools@latest deploy \
  --only functions,firestore:rules \
  --project "$PROJECT_ID" --non-interactive

echo "PaidMX Firebase Functions and Firestore rules deployment completed."
