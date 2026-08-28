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


def count_rows(table_name):
    """Retourne le nombre de lignes d'une table."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM {table_name};
                    """
                )

                return cur.fetchone()[0]


def count_nulls(table_name):
    """Retourne le nombre de valeurs NULL pour chaque colonne d'une table."""
    columns = list_columns(table_name)
    results = {}

    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                for column_name, _ in columns:
                    cur.execute(
                        f"""
                        SELECT COUNT(*)
                        FROM {table_name}
                        WHERE {column_name} IS NULL;
                        """
                    )

                    results[column_name] = cur.fetchone()[0]

    return results


def count_null_parent_station_by_location_type():
    """Compte les parent_station NULL par location_type."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT location_type, COUNT(*)
                    FROM stops
                    WHERE parent_station IS NULL
                    GROUP BY location_type
                    ORDER BY location_type;
                    """
                )

                return cur.fetchall()


def find_duplicate_stop_ids():
    """Retourne les stop_id présents plusieurs fois."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT stop_id, COUNT(*)
                    FROM stops
                    GROUP BY stop_id
                    HAVING COUNT(*) > 1
                    ORDER BY stop_id;
                    """
                )

                return cur.fetchall()


def find_invalid_coordinates():
    """Retourne les arrêts avec des coordonnées invalides."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT stop_id, stop_name, stop_lat, stop_lon
                    FROM stops
                    WHERE stop_lat < -90
                       OR stop_lat > 90
                       OR stop_lon < -180
                       OR stop_lon > 180;
                    """
                )

                return cur.fetchall()


def find_times_after_midnight():
    """Retourne quelques horaires GTFS supérieurs ou égaux à 24:00."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT trip_id, stop_id, arrival_time, departure_time
                    FROM stop_times
                    WHERE arrival_time >= '24:00:00'
                       OR departure_time >= '24:00:00'
                    ORDER BY arrival_time
                    LIMIT 20;
                    """
                )

                return cur.fetchall()


def find_duplicates(table_name, column_name):
    """Retourne les valeurs présentes plusieurs fois dans une colonne."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT {column_name}, COUNT(*)
                    FROM {table_name}
                    GROUP BY {column_name}
                    HAVING COUNT(*) > 1
                    ORDER BY COUNT(*) DESC;
                    """
                )

                return cur.fetchall()


def list_route_types():
    """Retourne les types de transport présents dans routes."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT route_type, COUNT(*)
                    FROM routes
                    GROUP BY route_type
                    ORDER BY route_type;
                    """
                )

                return cur.fetchall()


def list_routes():
    """Retourne les lignes et leur type de transport."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT route_short_name, route_long_name, route_type
                    FROM routes
                    ORDER BY route_type, route_short_name;
                    """
                )

                return cur.fetchall()


def get_tram_stops():
    """Retourne les arrêts de tram avec leur ligne et leurs coordonnées."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DISTINCT
                        r.route_short_name,
                        s.stop_id,
                        s.stop_name,
                        s.stop_lat,
                        s.stop_lon
                    FROM routes AS r
                    JOIN trips AS t
                        ON t.route_id = r.route_id
                    JOIN stop_times AS st
                        ON st.trip_id = t.trip_id
                    JOIN stops AS s
                        ON s.stop_id = st.stop_id
                    WHERE r.route_type = 0
                        AND r.route_short_name LIKE 'T%'
                    ORDER BY r.route_short_name, s.stop_name;
                    """
                )

                return cur.fetchall()
