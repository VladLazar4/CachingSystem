import psycopg2
import json

DB_CONFIG = {
    "dbname": "proximity_db",
    "user": "vlad",
    "password": "vlad123",
    "host": "db",
    "port": 5432
}

JSON_FILE = "../../data/users_1000.json"

def recreate_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS "CachingSystemApp_userlocation" CASCADE;')
    cur.execute('DROP TABLE IF EXISTS "CachingSystemApp_friendship" CASCADE;')

    cur.execute("""
        CREATE TABLE "CachingSystemApp_userlocation" (
            id INTEGER PRIMARY KEY,
            f_name VARCHAR(100),
            l_name VARCHAR(100),
            lat DOUBLE PRECISION,
            long DOUBLE PRECISION
        );
    """)

    cur.execute("""
        CREATE TABLE "CachingSystemApp_friendship" (
                user_id INTEGER REFERENCES "CachingSystemApp_userlocation"(id) ON DELETE CASCADE,
                friend_id INTEGER REFERENCES "CachingSystemApp_userlocation"(id) ON DELETE CASCADE,
                PRIMARY KEY (user_id, friend_id)
            );
    """);


    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")

def import_json_to_db():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    data_to_insert = [(u["id"], u["f_name"], u["l_name"], u["lat"], u["long"]) for u in users]

    cur.executemany("""
        INSERT INTO "CachingSystemApp_userlocation" (id, f_name, l_name, lat, long)
        VALUES (%s, %s, %s, %s, %s)
    """, data_to_insert)

    for user in users:
        user_id = user["id"]
        for friend_id in user["friends"]:
            cur.execute("""
                        INSERT INTO "CachingSystemApp_friendship" (user_id, friend_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING;
                        """, (user_id, friend_id))

    conn.commit()
    cur.close()
    conn.close()
    print(f"{len(users)} users imported.")

if __name__ == "__main__":
    recreate_table()
    import_json_to_db()
