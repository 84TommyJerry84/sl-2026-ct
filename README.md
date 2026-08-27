# sl-2026-ct

## Cartographier la base et produire un jeu de données documenté

## Présentation

Ce projet utilise une base de données PostgreSQL distante avec les données GTFS
des transport dl'île-de-France : métro, RER et tram

L'objectif est de :

- cartographier la bdd avec du code python et du schéma de postgreSQL;
- analyser la structure et la qualité des données;
- extraire un jeu de donées ciblés et reutilisables;
- exporter cet extrait au format CSV et Parquet;
- doucmenter les données à l'aide d'un dictionnaire de données;

le cas d'usage est l'extraction des arrêts de tram avec leurs lignes 
et leurs coordonnées géographiques.

## Source des données

Les données utilisées proviennent d'une base PostgreSQL distante contenant 
des données GTFS des transports d'Île-de-France.

La base contient notamment les données liées au métro, au RER et au tram.

La connexion à PostgreSQL est configurée à l'aide de variables d'environnement
stockées dans un fichier .env local.
Ce fichier contient les paramètres nécessaires à la connexion :

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_SSLMODE

pour la sécurité le fichier .env n'est pas versionné afin de ne pas 
exposer les informations de connexion. Un fichier .env.example est 
fourni dans le dépôt pour indiquer les variables à mettre sans contenir
de valeurs sensibles.

## Structure du projet

Le projet est organisé de la manière suivante :

```bash
sl-2026-ct/
│
├── src/
│   ├── __init__.py
│   ├── connection.py
│   ├── queries.py
│   ├── analyses.py
│   └── export.py
│
├── data/
│   ├── tram_stops.csv
│   └── tram_stops.parquet
│
├── cartographie.md
├── dictionnaire_donnees.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

### Rôle des principaux fichiers

- `src/connection.py` : configure et ouvre la connexion à la base PostegreSQL.
- `src/queries.py` : regroupe toutes les requetes SQL utilisées pour explorer la bdd, effectuer le controle qualité et extraire les données.
- `src/analyses.py` : 
- `src/export` : génere les livrables demandés(cartographie,CSV,Parquet et dictionnaire de données).
- `cartographie.md` : documente les tables, leurs colonnes, leurs types, leur volumétrie et les premiers aspects qualité de la donnée.
- `dictionnaire_données.md` : 
- `data/` : contient le CSV et le Parquet généré localement, non versionnés par Git.
- `.env.example` : indique les variables d'environnement nécessaires à la connexion sans secret.
- `requirements.txt` : contient les dépandances Python nécessaires au projet avec leur versions figées.

## Installation et configuration

1. Clone le repository

```bash
- git clone https://github.com/84TommyJerry84/sl-2026-ct.git
- cd sl-2026-ct
```

2. Créer un environnement virtuel

```bash
py -m venv env
```
Sous PowerShell :

```powershell
.\env\Scripts\Activate.ps1
```
Sous Git Bash :

```bash
source env/Scripts/activate
```
Une fois l'environnement activé, (env) apparaît dans le terminal.

3. Installer les dépendances

pip install -r requirements.txt

Les principales dépendances utilisées sont :

- python-dotenv pour charger les variables d'environnement ;
- psycopg2-binary pour se connecter à PostgreSQL ;
- pandas pour manipuler et exporter le jeu de données ;
- pyarrow pour l'export au format Parquet ;
- ruff pour le formatage et le contrôle de qualité du code.

4. Configurer la connexion PostgreSQL

```bash
pip install -r requirements.txt
```

Les principales dépendances utilisées sont :

python-dotenv pour charger les variables d'environnement ;
psycopg2-binary pour se connecter à PostgreSQL ;
pandas pour manipuler et exporter le jeu de données ;
pyarrow pour l'export au format Parquet ;
ruff pour le formatage et le contrôle de qualité du code.