# Cartographie de la base GTFS Île-de-France

## agency

**Rôle :** Organismes ou opérateurs de transport.

**Volume :** 7 lignes

**Colonnes clés :** agency_id

### Colonnes

| Colonne | Type |
| --- | --- |
| agency_id | text |
| agency_name | text |
| agency_url | text |
| agency_timezone | text |

### Qualité

Aucune valeur NULL. Aucun doublon détecté sur agency_id.

## calendar

**Rôle :** Jours de fonctionnement des services sur une période.

**Volume :** 858 lignes

**Colonnes clés :** service_id

### Colonnes

| Colonne | Type |
| --- | --- |
| service_id | text |
| monday | smallint |
| tuesday | smallint |
| wednesday | smallint |
| thursday | smallint |
| friday | smallint |
| saturday | smallint |
| sunday | smallint |
| start_date | date |
| end_date | date |

### Qualité

Aucune valeur NULL. Aucun doublon détecté sur service_id.

## calendar_dates

**Rôle :** Exceptions de service pour des dates précises.

**Volume :** 2603 lignes

**Colonnes clés :** service_id, date

### Colonnes

| Colonne | Type |
| --- | --- |
| service_id | text |
| date | date |
| exception_type | smallint |

### Qualité

Aucune valeur NULL détectée.

## routes

**Rôle :** Lignes de transport.

**Volume :** 38 lignes

**Colonnes clés :** route_id, agency_id

### Colonnes

| Colonne | Type |
| --- | --- |
| route_id | text |
| agency_id | text |
| route_short_name | text |
| route_long_name | text |
| route_type | integer |

### Qualité

Aucune valeur NULL. Aucun doublon détecté sur route_id.

## stop_times

**Rôle :** Horaires de passage des trajets aux arrêts.

**Volume :** 2219678 lignes

**Colonnes clés :** trip_id, stop_id, stop_sequence

### Colonnes

| Colonne | Type |
| --- | --- |
| trip_id | text |
| stop_id | text |
| arrival_time | text |
| departure_time | text |
| stop_sequence | integer |

### Qualité

Aucune valeur NULL. Des horaires supérieurs ou égaux à 24:00 sont présents ; ils sont autorisés dans le contexte GTFS.

## stops

**Rôle :** Arrêts et stations avec leurs coordonnées.

**Volume :** 2396 lignes

**Colonnes clés :** stop_id, parent_station

### Colonnes

| Colonne | Type |
| --- | --- |
| stop_id | text |
| stop_name | text |
| stop_lat | double precision |
| stop_lon | double precision |
| location_type | integer |
| parent_station | text |

### Qualité

771 valeurs NULL dans parent_station, toutes associées à location_type = 1. Aucun doublon sur stop_id et aucune coordonnée hors des limites géographiques.

## transfers

**Rôle :** Correspondances entre les arrêts.

**Volume :** 3441 lignes

**Colonnes clés :** from_stop_id, to_stop_id

### Colonnes

| Colonne | Type |
| --- | --- |
| from_stop_id | text |
| to_stop_id | text |
| transfer_type | smallint |
| min_transfer_time | integer |

### Qualité

Aucune valeur NULL détectée.

## trips

**Rôle :** Circulations associées aux lignes et aux services.

**Volume :** 103914 lignes

**Colonnes clés :** trip_id, route_id, service_id

### Colonnes

| Colonne | Type |
| --- | --- |
| trip_id | text |
| route_id | text |
| service_id | text |
| trip_headsign | text |
| direction_id | smallint |

### Qualité

Aucune valeur NULL. Aucun doublon détecté sur trip_id.

