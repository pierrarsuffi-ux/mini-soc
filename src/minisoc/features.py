"""Calcule les features (caractéristiques) de chaque connexion pour le Machine Learning."""

import duckdb

from ingest import DB_FILE

FEATURES_QUERY = """
CREATE OR REPLACE TABLE features AS
WITH ip_stats AS (
    SELECT
        source_ip,
        COUNT(*) AS ip_nb_attempts,
        COUNT(DISTINCT username) AS ip_nb_usernames,
        AVG(CASE WHEN event = 'login_failed' THEN 1 ELSE 0 END) AS ip_fail_rate
    FROM raw_logs
    GROUP BY source_ip
)
SELECT
    r.timestamp,
    r.username,
    r.source_ip,
    r.event,
    r.label,
    EXTRACT(hour FROM r.timestamp) AS hour,
    CASE WHEN r.event = 'login_failed' THEN 1 ELSE 0 END AS is_failed,
    s.ip_nb_attempts,
    s.ip_nb_usernames,
    s.ip_fail_rate
FROM raw_logs AS r
JOIN ip_stats AS s ON r.source_ip = s.source_ip
ORDER BY r.timestamp
"""


def main():
    with duckdb.connect(DB_FILE) as con:
        con.execute(FEATURES_QUERY)
        nb_rows = con.execute("SELECT COUNT(*) FROM features").fetchone()[0]

    print(f"{nb_rows} lignes dans la table features de {DB_FILE}")


if __name__ == "__main__":
    main()