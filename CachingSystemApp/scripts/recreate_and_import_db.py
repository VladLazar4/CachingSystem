import psycopg2
import json

DB_CONFIG = {
    "dbname": "proximity_db",
    "user": "vlad",
    "password": "vlad123",
    "host": "db",
    "port": 5432
}

JSON_FILE = "../../data/users_100000.json"

def recreate_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS "CachingSystemApp_userlocation";')

    cur.execute("""
        CREATE TABLE "CachingSystemApp_userlocation" (
            id SERIAL PRIMARY KEY,
            f_name VARCHAR(100),
            l_name VARCHAR(100),
            lat DOUBLE PRECISION,
            long DOUBLE PRECISION
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")

def import_json_to_db():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    data_to_insert = [(u["f_name"], u["l_name"], u["lat"], u["long"]) for u in users]

    cur.executemany("""
        INSERT INTO "CachingSystemApp_userlocation" (f_name, l_name, lat, long)
        VALUES (%s, %s, %s, %s)
    """, data_to_insert)

    conn.commit()
    cur.close()
    conn.close()
    print(f"{len(users)} users imported.")

if __name__ == "__main__":
    recreate_table()
    import_json_to_db()
