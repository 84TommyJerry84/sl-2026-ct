from src.analyses import get_database_map


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

            file.writelines(f"| {column_name} | {data_type} |\n" for column_name, data_type in table["columns"])

            file.write("\n### Qualité\n\n")
            file.write(f"{table['quality_note']}\n\n")


if __name__ == "__main__":
    export_database_map()