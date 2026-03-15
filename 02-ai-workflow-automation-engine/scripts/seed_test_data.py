"""Seed placeholder metric data into PostgreSQL for local demos."""

from app.db.connection import get_connection


def main() -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO workflow_metrics (metric_name, metric_value, metric_unit)
                VALUES (%s, %s, %s)
                """,
                ("manual_seed_example", 1, "count"),
            )
        connection.commit()

    print("Seeded placeholder metric data.")


if __name__ == "__main__":
    main()
