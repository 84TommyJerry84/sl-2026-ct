# sl-2026-ct

## Cartographier la base et produire un jeu de données documenté

## Présentation

Ce projet utilise une base de données PostgreSQL distante avec les données GTFS
des transport dl'île-de-France : métro, RER et tram

L'objectif est de :

* cartographier la bdd avec du code python et du schéma de postgreSQL;
* analyser la structure et la qualité des données;
* extraire un jeu de donées ciblés et reutilisables;
* exporter cet extrait au format CSV et Parquet;
* doucmenter les données à l'aide d'un dictionnaire de données;

le cas d'usage est l'extraction des arrêts de tram avec leurs lignes 
et leurs coordonnées géographiques.

## Source des données

Les données utilisées proviennent d'une base PostgreSQL distante contenant 
des données GTFS des transports d'Île-de-France.

La base contient notamment les données liées au métro, au RER et au tram.

La connexion à PostgreSQL est configurée à l'aide de variables d'environnement
stockées dans un fichier .env local.
Ce fichier contient les paramètres nécessaires à la connexion :

* DB_HOST
* DB_PORT
* DB_NAME
* DB_USER
* DB_PASSWORD
* DB_SSLMODE

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

* `src/connection.py` : configure et ouvre la connexion à la base PostegreSQL.
* `src/queries.py` : regroupe toutes les requetes SQL utilisées pour explorer la bdd, effectuer le controle qualité et extraire les données.
* `src/analyses.py` : 
* `src/export` : génere les livrables demandés(cartographie,CSV,Parquet et dictionnaire de données).
* `cartographie.md` : documente les tables, leurs colonnes, leurs types, leur volumétrie et les premiers aspects qualité de la donnée.
* `dictionnaire_données.md` : 
* `data/` : contient le CSV et le Parquet généré localement, non versionnés par Git.
* `.env.example` : indique les variables d'environnement nécessaires à la connexion sans secret.
* `requirements.txt` : contient les dépandances Python nécessaires au projet avec leur versions figées.

4. Configurer la connexion PostgreSQL

## Installation et configuration

### 1. Cloner le repository

```bash
git clone <URL_DU_REPOSITORY>
cd sl-2026-ct
```

### 2. Créer un environnement virtuel

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

Une fois l'environnement activé, `(env)` apparaît dans le terminal.

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les principales dépendances utilisées sont :

* `python-dotenv` pour charger les variables d'environnement ;
* `psycopg2-binary` pour se connecter à PostgreSQL ;
* `pandas` pour manipuler et exporter le jeu de données ;
* `pyarrow` pour l'export au format Parquet ;
* `ruff` pour le formatage et le contrôle de qualité du code.

### 4. Configurer la connexion PostgreSQL

Créer un fichier `.env` à partir du fichier `.env.example`.

Il doit contenir les variables suivantes :

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_SSLMODE=
```

Renseigner les paramètres de connexion fournis pour accéder à la base PostgreSQL distante.

Pour cette base distante, le mode SSL utilisé est :

```env
DB_SSLMODE=require
```

Le fichier `.env` reste local et n'est pas versionné dans Git.


## Génération des livrables

Une fois l'environnement virutel mis en place, les dépendances installées et le
fichier .env correctement rempli et configuré on peut générer tous les livrables
en une seule commande qui est la suivante :

```bash
py -m src.export
```

cette commande va créer :

* `cartographie.md` : cartographie de la base de donnée PostgreSQL;
* `dictionnaire_données` : definition des données de l'extrait;
* `data/tram_stops.csv` : extrait au format csv;
* `data/tram_stops.parquet` : extrait au format parquet;

Les fichiers CSV et Parquet sont générés localement dans le dossier data/ et ne sont pas
versionnés dans Git. Ils peuvent être reconstruits à tout moment à partir du code.

La commande s’appuie sur la fonction principale de `src/export.py`, qui exécute
successivement les différentes fonctions d’export.

## Jeu de données extrait

Le choix s'est fait sur l'extraction de tous les arrêts de tram
, leur ligne et leurs coordonnées géographiques.

le jeu de données est disponible sous deux formats :
* `data/tram_stops.csv`
* `data/tram_stops.parquet`

Cet extrait contien au total 564 lignes et 5 colonnes :

* `line_name` : nom court de la ligne de tram ;
* `stop_id` : identifiant GTFS de l'arrêt ;
* `stop_name` : nom de l'arrêt ;
* `latitude` : latitude de l'arrêt en degrés ;
* `longitude` : longitude de l'arrêt en degrés.

Une ligne représente l'association entre une ligne de tram et un point d'arrêt GTFS.

Les données sont obtenues en reliant les tables :
```
routes
  ↓
trips
  ↓
stop_times
  ↓
stops
```
La table `routes` permet d'identifier la ligne, tandis que la table stops fournit le nom et les coordonnées de l'arrêt.

Un même nom d'arrêt peut apparaître plusieurs fois lorsque plusieurs `stop_id` distincts existent dans les données GTFS.
Ces lignes ne sont donc pas supprimées lorsqu'elles représentent des points d'arrêt différents.

## Dictionnaire de données et réutilisabilité

Le fichier `dictionnaire_donnees.md` documente les colonnes du jeu de données extrait.

Pour chaque colonne, il précise :

* son nom ;
* son type ;
* son unité ou domaine de valeurs ;
* sa source dans la base PostgreSQL ;
* sa date d'extraction, qui permet d'indiquer la fraîcheur de la donnée.

Ce dictionnaire permet à une personne qui ne connaît pas la base GTFS d'utiliser plus facilement le jeu de données 
sans avoir à consulter directement les tables d'origine.

Sans ce dictionnaire, certaines colonnes pourraient être difficiles à interpréter. Par exemple, il ne serait pas 
évident de savoir à quoi correspond `line_name`, ce que représente `stop_id`, dans quelle unité sont exprimées 
`latitude` et `longitude`, ou encore de quelles colonnes de la base ces données proviennent.

Le dictionnaire apporte donc le contexte nécessaire pour comprendre, exploiter et réutiliser l'extrait de manière
autonome.

## CSV et Parquet

Le jeu de données extrait est exporté à la fois en CSV et en Parquet.

Le format CSV est un format texte simple, lisible facilement avec un éditeur de texte, un tableur ou de nombreux
outils de traitement de données. Il convient bien pour des jeux de données de petite ou moyenne taille et pour 
des échanges simples entre différents outils.

Le format Parquet est un format binaire orienté colonnes. Il conserve mieux les types de données et est généralement
plus adapté lorsque les volumes deviennent importants ou lorsqu'on souhaite effectuer des traitements analytiques 
plus efficaces.

Le CSV est donc suffisant lorsque l'objectif principal est de consulter, partager ou manipuler simplement les données.

Le Parquet devient plus intéressant lorsque :

* le volume de données est important ;
* les types de données doivent être conservés ;
* seules certaines colonnes doivent être lues ;
* le jeu doit être utilisé dans des traitements analytiques ou des pipelines de données.

Les deux formats sont fournis afin de faciliter la réutilisation du jeu selon les besoins de l'utilisateur.

## Fraîcheur des données

La fraîcheur du jeu de données correspond à la date à laquelle l'extraction est générée depuis la base PostgreSQL.

Cette date est ajoutée automatiquement dans `dictionnaire_donnees.md` lors de l'exécution de :

```bash
py -m src.export
```

Elle permet à l'utilisateur de savoir à quelle date les données ont été extraites et donc d'évaluer si elles sont 
suffisamment récentes pour son usage.

## Qualité du code

Le projet utilise `ruff` afin de vérifier le formatage et la qualité du code Python.

Pour formater automatiquement le code :

```bash
ruff format .
```

Pour vérifier le code :

```bash
ruff check .
```

Le projet doit pouvoir passer ces deux commandes sans erreur avant d'être considéré comme terminé.

Ruff permet notamment de vérifier le respect des conventions de style Python, la qualité des imports et 
certaines erreurs courantes dans le code.

## Utilisation du jeu de données

Le jeu de données produit permet d'obtenir une liste des points d'arrêt de tram d'Île-de-France avec 
leur ligne et leurs coordonnées géographiques.

Il peut notamment être utilisé pour :

* localiser les arrêts de tram ;
* réaliser une cartographie des lignes et des arrêts ;
* effectuer des analyses géographiques ;
* servir de jeu d'entrée pour d'autres traitements ou outils de visualisation.

Le jeu ne contient aucune donnée personnelle. Il ne présente donc pas de problématique particulière 
liée aux données personnelles dans le cadre de ce projet.
