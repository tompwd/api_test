import sqlite3
from src.config import table_definitions
import pandas as pd

conn = sqlite3.connect("sqlite.db")
cur = conn.cursor()

# create 3 source tables in sqlite db
for table_def in table_definitions:
    cur.execute(table_def)

source_data = ['policy_data', 'finance_data', 'calendar']

for table in source_data:
    df = pd.read_csv(f'./raw_data/{table}.csv')
    df.to_sql(table.split('_')[0], conn, if_exists='append', index=False)

# close connection after initial load complete
conn.close()
