from contextlib import closing

from src.connection import get_connection


def list_tables():
    """Retourne la liste des tables du schéma public."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                    """
                )

                return cur.fetchall()


def list_columns(table_name):
    """Retourne les colonnes et leurs types pour une table."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = %s
                    ORDER BY ordinal_position;
                    """,
                    (table_name,),
                )

                return cur.fetchall()
