-- PaidMX operational foundation: run once after database/schema.sql.
ALTER TABLE paidmx_users
  ADD COLUMN IF NOT EXISTS referrer_telegram_id BIGINT REFERENCES paidmx_users(telegram_id),
  ADD COLUMN IF NOT EXISTS referral_count BIGINT NOT NULL DEFAULT 0 CHECK (referral_count >= 0),
  ADD COLUMN IF NOT EXISTS is_blocked BOOLEAN NOT NULL DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS paidmx_users_referrer_idx ON paidmx_users(referrer_telegram_id);
CREATE INDEX IF NOT EXISTS paidmx_users_created_at_idx ON paidmx_users(created_at DESC);

CREATE TABLE IF NOT EXISTS paidmx_referrals (
  id BIGSERIAL PRIMARY KEY,
  referrer_telegram_id BIGINT NOT NULL REFERENCES paidmx_users(telegram_id),
  referred_telegram_id BIGINT NOT NULL UNIQUE REFERENCES paidmx_users(telegram_id),
  status TEXT NOT NULL DEFAULT 'registered' CHECK (status IN ('registered','qualified','rewarded','rejected')),
  reward_points BIGINT NOT NULL DEFAULT 0 CHECK (reward_points >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  qualified_at TIMESTAMPTZ,
  rewarded_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS paidmx_referrals_referrer_idx ON paidmx_referrals(referrer_telegram_id, created_at DESC);

CREATE TABLE IF NOT EXISTS paidmx_payment_events (
  id BIGSERIAL PRIMARY KEY,
  telegram_id BIGINT REFERENCES paidmx_users(telegram_id),
  provider TEXT NOT NULL DEFAULT 'manual',
  provider_event_id TEXT,
  event_type TEXT NOT NULL CHECK (event_type IN ('deposit','payout','payout_approved','payout_rejected','payout_paid','payment_failed')),
  amount NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (amount >= 0),
  currency TEXT NOT NULL DEFAULT 'USDT',
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','processing','succeeded','failed','cancelled')),
  note TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(provider, provider_event_id)
);
CREATE INDEX IF NOT EXISTS paidmx_payment_events_user_idx ON paidmx_payment_events(telegram_id, created_at DESC);
CREATE INDEX IF NOT EXISTS paidmx_payment_events_status_idx ON paidmx_payment_events(status, created_at DESC);

CREATE TABLE IF NOT EXISTS paidmx_notifications (
  id BIGSERIAL PRIMARY KEY,
  telegram_id BIGINT REFERENCES paidmx_users(telegram_id),
  kind TEXT NOT NULL,
  message TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued','sent','failed')),
  telegram_message_id BIGINT,
  error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sent_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS paidmx_notifications_user_idx ON paidmx_notifications(telegram_id, created_at DESC);

CREATE TABLE IF NOT EXISTS paidmx_admin_audit (
  id BIGSERIAL PRIMARY KEY,
  admin_telegram_id BIGINT NOT NULL,
  action TEXT NOT NULL,
  target_telegram_id BIGINT,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
