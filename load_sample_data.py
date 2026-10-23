"""Load the checked-in sample CSV into PostgreSQL.

Safe to re-run: rows are upserted by (date, model), so the sample records do
not accumulate duplicates.
"""

import os
from contextlib import closing
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()


def main() -> None:
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise SystemExit("Set DB_PASSWORD in your local .env file first.")

    csv_path = Path(__file__).with_name("data.csv")
    data = pd.read_csv(csv_path)
    data.columns = [str(column).strip().lower() for column in data.columns]
    data = data.rename(columns={"responsetime": "response_time"})

    required = {"date", "model", "prompts", "tokens", "cost", "response_time"}
    missing = required - set(data.columns)
    if missing:
        raise SystemExit(f"CSV is missing expected columns: {', '.join(sorted(missing))}")

    data["date"] = pd.to_datetime(data["date"], errors="raise").dt.date
    data["model"] = data["model"].astype(str).str.strip()
    data = data[list(sorted(required, key=["date", "model", "prompts", "tokens", "cost", "response_time"].index))]
    records = list(data.itertuples(index=False, name=None))
    if not records:
        raise SystemExit("The sample CSV has no records.")

    connection_settings = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "ai_data_usage"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": password,
        "connect_timeout": 5,
    }

    with closing(psycopg2.connect(**connection_settings)) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS usage_data (
                        date DATE NOT NULL,
                        model TEXT NOT NULL,
                        prompts BIGINT NOT NULL DEFAULT 0,
                        tokens BIGINT NOT NULL DEFAULT 0,
                        cost NUMERIC(14, 4) NOT NULL DEFAULT 0,
                        response_time NUMERIC(14, 4) NOT NULL DEFAULT 0,
                        PRIMARY KEY (date, model)
                    )
                    """
                )
                execute_values(
                    cursor,
                    """
                    INSERT INTO usage_data
                        (date, model, prompts, tokens, cost, response_time)
                    VALUES %s
                    ON CONFLICT (date, model) DO UPDATE SET
                        prompts = EXCLUDED.prompts,
                        tokens = EXCLUDED.tokens,
                        cost = EXCLUDED.cost,
                        response_time = EXCLUDED.response_time
                    """,
                    records,
                )

    print(f"Loaded {len(records):,} sample records from {csv_path.name}.")


if __name__ == "__main__":
    main()
