{{ config(materialized='table') }}

WITH raw_data AS (
    SELECT * FROM read_json_auto('all_mlb_stats_2026.json')
    WHERE name IS NOT NULL 
      AND name != 'Nom du joueur'
      AND LOWER(name) NOT LIKE '%nom%'
),

cleaned_data AS (
    SELECT 
        name as player_name,
        team,
        'HITTER' as player_type,
        COALESCE(gamesPlayed, 0) as games,
        COALESCE(atBats, 0) as atBats,
        COALESCE(hits, 0) as hits,
        COALESCE(doubles, 0) as doubles,
        COALESCE(triples, 0) as triples,
        COALESCE(homeRuns, 0) as homeRuns,
        COALESCE(rbi, 0) as rbi,
        COALESCE(runs, 0) as runs,
        COALESCE(baseOnBalls, 0) as walks,
        COALESCE(strikeOuts, 0) as strikeouts,
        COALESCE(stolenBases, 0) as stolenBases,
        COALESCE(hitByPitch, 0) as hbp,
        -- Force la conversion des colonnes potentiellement textuelles
        TRY_CAST(NULLIF(ops, '-.--') AS DOUBLE) as ops,
        COALESCE(totalBases, 0) as total_bases,

        -- Calcul du score Sorare
        (
            (COALESCE(runs, 0) * 3) +
            (COALESCE(rbi, 0) * 3) +
            ((COALESCE(hits, 0) - COALESCE(doubles, 0) - COALESCE(triples, 0) - COALESCE(homeRuns, 0)) * 2) +
            (COALESCE(doubles, 0) * 5) +
            (COALESCE(triples, 0) * 8) +
            (COALESCE(homeRuns, 0) * 10) +
            (COALESCE(baseOnBalls, 0) * 2) +
            (COALESCE(strikeOuts, 0) * -1) +
            (COALESCE(stolenBases, 0) * 5) +
            (COALESCE(hitByPitch, 0) * 2)
        ) as sorare_score,

        ROUND(
            (
                (COALESCE(runs, 0) * 3) +
                (COALESCE(rbi, 0) * 3) +
                ((COALESCE(hits, 0) - COALESCE(doubles, 0) - COALESCE(triples, 0) - COALESCE(homeRuns, 0)) * 2) +
                (COALESCE(doubles, 0) * 5) +
                (COALESCE(triples, 0) * 8) +
                (COALESCE(homeRuns, 0) * 10) +
                (COALESCE(baseOnBalls, 0) * 2) +
                (COALESCE(strikeOuts, 0) * -1) +
                (COALESCE(stolenBases, 0) * 5) +
                (COALESCE(hitByPitch, 0) * 2)
            ) / NULLIF(COALESCE(gamesPlayed, 0), 0), 2
        ) as sorare_avg_per_game
    FROM raw_data
)

SELECT * FROM cleaned_data