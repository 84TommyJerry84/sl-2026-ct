from src.queries import count_rows, list_columns, list_tables

TABLE_DESCRIPTIONS = {
    "agency": "Organismes ou opérateurs de transport.",
    "calendar": "Jours de fonctionnement des services sur une période.",
    "calendar_dates": "Exceptions de service pour des dates précises.",
    "routes": "Lignes de transport.",
    "stop_times": "Horaires de passage des trajets aux arrêts.",
    "stops": "Arrêts et stations avec leurs coordonnées.",
    "transfers": "Correspondances entre les arrêts.",
    "trips": "Circulations associées aux lignes et aux services.",
}

TABLE_KEY_COLUMNS = {
    "agency": ["agency_id"],
    "calendar": ["service_id"],
    "calendar_dates": ["service_id", "date"],
    "routes": ["route_id", "agency_id"],
    "stop_times": ["trip_id", "stop_id", "stop_sequence"],
    "stops": ["stop_id", "parent_station"],
    "transfers": ["from_stop_id", "to_stop_id"],
    "trips": ["trip_id", "route_id", "service_id"],
}

QUALITY_NOTES = {
    "agency": ("Aucune valeur NULL. Aucun doublon détecté sur agency_id."),
    "calendar": ("Aucune valeur NULL. Aucun doublon détecté sur service_id."),
    "calendar_dates": ("Aucune valeur NULL détectée."),
    "routes": ("Aucune valeur NULL. Aucun doublon détecté sur route_id."),
    "stop_times": (
        "Aucune valeur NULL. "
        "Des horaires supérieurs ou égaux à 24:00 sont présents ; "
        "ils sont autorisés dans le contexte GTFS."
    ),
    "stops": (
        "771 valeurs NULL dans parent_station, toutes associées "
        "à location_type = 1. Aucun doublon sur stop_id et aucune "
        "coordonnée hors des limites géographiques."
    ),
    "transfers": ("Aucune valeur NULL détectée."),
    "trips": ("Aucune valeur NULL. Aucun doublon détecté sur trip_id."),
}


def get_table_volumes():
    """Retourne le nombre de lignes pour chaque table."""
    volumes = []

    for table in list_tables():
        table_name = table[0]
        row_count = count_rows(table_name)

        volumes.append((table_name, row_count))

    return volumes


def get_database_map():
    """Retourne la cartographie des tables de la base."""
    database_map = []

    for table in list_tables():
        table_name = table[0]

        columns = list_columns(table_name)
        row_count = count_rows(table_name)
        description = TABLE_DESCRIPTIONS[table_name]
        key_columns = TABLE_KEY_COLUMNS[table_name]
        quality_note = QUALITY_NOTES[table_name]

        database_map.append(
            {
                "table": table_name,
                "description": description,
                "row_count": row_count,
                "key_columns": key_columns,
                "columns": columns,
                "quality_note": quality_note,
            }
        )

    return database_map
