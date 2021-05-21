policy_table = """CREATE TABLE policy
	(
	policy_id         TEXT PRIMARY KEY,
	user_id           TEXT,
	subscription_id   TEXT,
	policy_start_date TIMESTAMPTZ,
	policy_end_date   TIMESTAMPTZ,
	underwriter       TEXT
);"""

finance_table = """CREATE TABLE finance
(
	finance_transaction_id TEXT PRIMARY KEY,
	created_at             TIMESTAMPTZ,
	policy_id              TEXT,
	reason                 TEXT,
	premium                INT,
	ipt                    INT
);"""

calendar_table = """CREATE TABLE calendar
(
	date         DATE PRIMARY KEY,
	year         INT,
	month_number INT,
	month_name   TEXT,
	day_of_month INT,
	day_of_week  INT,
	year_month   TEXT
)"""

table_definitions = [policy_table, finance_table, calendar_table]
