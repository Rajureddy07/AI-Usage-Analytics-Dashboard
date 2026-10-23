"""Small command-line helper for inspecting AI usage records."""

import os
from contextlib import closing

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise SystemExit("Set DB_PASSWORD in your local .env file first.")

    settings = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "ai_data_usage"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": password,
        "connect_timeout": 5,
    }

    with closing(psycopg2.connect(**settings)) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT date, model, prompts, tokens, cost, response_time "
                "FROM usage_data ORDER BY date LIMIT 100"
            )
            for row in cursor.fetchall():
                print(row)


if __name__ == "__main__":
    main()
