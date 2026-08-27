from datetime import date
from pathlib import Path

import pandas as pd

from src.analyses import get_database_map
from src.queries import get_tram_stops


def export_database_map():
    """Génère le document Markdown de cartographie de la base."""
    database_map = get_database_map()

    with open("cartographie.md", "w", encoding="utf-8") as file:
        file.write("# Cartographie de la base GTFS Île-de-France\n\n")

        for table in database_map:
            file.write(f"## {table['table']}\n\n")

            file.write(f"**Rôle :** {table['description']}\n\n")
            file.write(f"**Volume :** {table['row_count']} lignes\n\n")

            key_columns = ", ".join(table["key_columns"])
            file.write(f"**Colonnes clés :** {key_columns}\n\n")

            file.write("### Colonnes\n\n")
            file.write("| Colonne | Type |\n")
            file.write("| --- | --- |\n")

            file.writelines(
                f"| {column_name} | {data_type} |\n"
                for column_name, data_type in table["columns"]
            )

            file.write("\n### Qualité\n\n")
            file.write(f"{table['quality_note']}\n\n")


def export_tram_stops():
    """Exporte les arrêts de tram en CSV et en Parquet."""
    tram_stops = get_tram_stops()

    columns = [
        "line_name",
        "stop_id",
        "stop_name",
        "latitude",
        "longitude",
    ]

    dataframe = pd.DataFrame(tram_stops, columns=columns)

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    dataframe.to_csv(
        output_dir / "tram_stops.csv",
        index=False,
    )

    dataframe.to_parquet(
        output_dir / "tram_stops.parquet",
        index=False,
    )


def export_data_dictionary():
    """Génère le dictionnaire de données de l'extrait des arrêts de tram."""
    extraction_date = date.today()  # noqa: DTZ011

    columns = [
        {
            "name": "line_name",
            "type": "text",
            "domain": "Nom court de la ligne de tram.",
            "source": "routes.route_short_name",
        },
        {
            "name": "stop_id",
            "type": "text",
            "domain": "Identifiant GTFS de l'arrêt.",
            "source": "stops.stop_id",
        },
        {
            "name": "stop_name",
            "type": "text",
            "domain": "Nom de l'arrêt.",
            "source": "stops.stop_name",
        },
        {
            "name": "latitude",
            "type": "nombre décimal",
            "domain": "Latitude en degrés.",
            "source": "stops.stop_lat",
        },
        {
            "name": "longitude",
            "type": "nombre décimal",
            "domain": "Longitude en degrés.",
            "source": "stops.stop_lon",
        },
    ]

    with open("dictionnaire_donnees.md", "w", encoding="utf-8") as file:
        file.write("# Dictionnaire de données\n\n")
        file.write(f"**Date d'extraction :** {extraction_date}\n\n")

        file.write(
            "| Colonne | Type | Unité / domaine de valeurs | Source | Fraîcheur |\n"
        )
        file.write("| --- | --- | --- | --- | --- |\n")

        file.writelines(
            f"| {column['name']} "
            f"| {column['type']} "
            f"| {column['domain']} "
            f"| {column['source']} "
            f"| {extraction_date} |\n"
            for column in columns
        )


def main():
    """Génère tous les livrables du projet."""
    export_database_map()
    export_tram_stops()
    export_data_dictionary()


if __name__ == "__main__":
    main()