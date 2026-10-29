CREATE TABLE IF NOT EXISTS paidmx_users (
  telegram_id BIGINT PRIMARY KEY,
  username TEXT,
  first_name TEXT NOT NULL DEFAULT '',
  language TEXT CHECK (language IN ('tr','en','ar','ru','es','pt','hi','id','zh')),
  theme TEXT CHECK (theme IN ('midnight','ocean','emerald','rose','violet','sunset')),
  points BIGINT NOT NULL DEFAULT 0 CHECK (points >= 0),
  usdt_balance NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (usdt_balance >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS paidmx_users_updated_at_idx ON paidmx_users (updated_at DESC);

-- MX -> GRAM rewards wallet. Safe to rerun on existing deployments.
ALTER TABLE paidmx_users ADD COLUMN IF NOT EXISTS gram_balance NUMERIC(24,8) NOT NULL DEFAULT 0 CHECK (gram_balance >= 0);
CREATE TABLE IF NOT EXISTS paidmx_reward_conversions (
  id BIGSERIAL PRIMARY KEY,
  telegram_id BIGINT NOT NULL REFERENCES paidmx_users(telegram_id) ON DELETE CASCADE,
  mx_amount BIGINT NOT NULL CHECK (mx_amount >= 100),
  gram_amount NUMERIC(24,8) NOT NULL CHECK (gram_amount > 0),
  points_after BIGINT NOT NULL CHECK (points_after >= 0),
  gram_balance_after NUMERIC(24,8) NOT NULL CHECK (gram_balance_after >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS paidmx_reward_conversions_user_date_idx ON paidmx_reward_conversions (telegram_id, created_at DESC);
