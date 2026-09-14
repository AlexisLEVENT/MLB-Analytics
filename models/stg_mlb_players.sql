{{ config(materialized='table') }}

WITH raw_data AS (
    SELECT * FROM read_json_auto('all_mlb_stats_2026.json')
    WHERE name IS NOT NULL 
      AND name != 'Nom du joueur'
      AND LOWER(name) NOT LIKE '%nom%'
),

cleaned_data AS (
    SELECT 
        COALESCE(name, 'Inconnu') as player_name,
        COALESCE(team, 'N/A') as team,
        'HITTER' as player_type,
        COALESCE(try_cast(gamesPlayed AS INTEGER), 0) as games,
        COALESCE(try_cast(atBats AS INTEGER), 0) as atBats,
        COALESCE(try_cast(hits AS DOUBLE), 0.0) as hits,
        COALESCE(try_cast(doubles AS DOUBLE), 0.0) as doubles,
        COALESCE(try_cast(triples AS DOUBLE), 0.0) as triples,
        COALESCE(try_cast(homeRuns AS DOUBLE), 0.0) as homeRuns,
        COALESCE(try_cast(rbi AS DOUBLE), 0.0) as rbi,
        COALESCE(try_cast(runs AS DOUBLE), 0.0) as runs,
        COALESCE(try_cast(baseOnBalls AS DOUBLE), 0.0) as walks,
        COALESCE(try_cast(strikeOuts AS DOUBLE), 0.0) as strikeouts,
        COALESCE(try_cast(stolenBases AS DOUBLE), 0.0) as stolenBases,
        COALESCE(try_cast(hitByPitch AS DOUBLE), 0.0) as hbp,

        -- Calcul du score Sorare
        (
            (COALESCE(try_cast(runs AS DOUBLE), 0.0) * 3) +
            (COALESCE(try_cast(rbi AS DOUBLE), 0.0) * 3) +
            -- Single = hits - doubles - triples - HR
            ((COALESCE(try_cast(hits AS DOUBLE), 0.0) - COALESCE(try_cast(doubles AS DOUBLE), 0.0) - COALESCE(try_cast(triples AS DOUBLE), 0.0) - COALESCE(try_cast(homeRuns AS DOUBLE), 0.0)) * 2) +
            (COALESCE(try_cast(doubles AS DOUBLE), 0.0) * 5) +
            (COALESCE(try_cast(triples AS DOUBLE), 0.0) * 8) +
            (COALESCE(try_cast(homeRuns AS DOUBLE), 0.0) * 10) +
            (COALESCE(try_cast(baseOnBalls AS DOUBLE), 0.0) * 2) +
            (COALESCE(try_cast(strikeOuts AS DOUBLE), 0.0) * -1) +
            (COALESCE(try_cast(stolenBases AS DOUBLE), 0.0) * 5) +
            (COALESCE(try_cast(hitByPitch AS DOUBLE), 0.0) * 2)
        ) as sorare_score
    FROM raw_data
)

SELECT * FROM cleaned_data