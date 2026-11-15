"""charge les logs bruts dans une base de donnée DuckDB."""
from pathlib import Path
import duckdb
from generator import OUTPUT_FILE
DB_FILE = Path("data/minisoc.duckdb")

def main():
    with duckdb.connect(DB_FILE) as con :
        con.execute(
        "CREATE OR REPLACE TABLE raw_logs AS SELECT * FROM read_json_auto(?)", [str(OUTPUT_FILE)],
        )
        nb_rows = con.execute("SELECT COUNT(*) FROM raw_logs").fetchone()[0]
    print(f"{nb_rows} lignes chargées dans la table raw_logs de {DB_FILE}")

if __name__ == "__main__":
    main()        
