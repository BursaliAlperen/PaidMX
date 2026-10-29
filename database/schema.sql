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
