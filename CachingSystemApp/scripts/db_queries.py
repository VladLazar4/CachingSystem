import math
import psycopg2
import json
from tqdm import tqdm

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# trebuie scos . dinaine de config pentru rularea din linia de comanda
from .config import DB_CONFIG_MASTER, DB_SHARDS, SHARDS_INFO, JSON_FILE

def create_databases(DB_CONFIG_MASTER, DB_SHARDS):
    default_conn = psycopg2.connect(
        dbname="postgres",
        user=DB_CONFIG_MASTER["user"],
        password=DB_CONFIG_MASTER["password"],
        host=DB_CONFIG_MASTER["host"],
        port=DB_CONFIG_MASTER["port"]
    )
    default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = default_conn.cursor()

    print("Dropping existing databases...")
    all_dbs = [DB_CONFIG_MASTER["dbname"]] + [cfg["dbname"] for cfg in DB_SHARDS.values()]
    for db_name in all_dbs:
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        if cur.fetchone():
            cur.execute(f"DROP DATABASE {db_name};")
            print(f"Database {db_name} dropped.")

    print(f"Creating database {DB_CONFIG_MASTER['dbname']}...")
    cur.execute(f"CREATE DATABASE {DB_CONFIG_MASTER['dbname']};")

    for shard_name, cfg in DB_SHARDS.items():
        print(f"Creating database {cfg['dbname']}...")
        cur.execute(f"CREATE DATABASE {cfg['dbname']};")

    cur.close()
    default_conn.close()
    print("All databases created successfully.")

def recreate_master():
    conn = psycopg2.connect(**DB_CONFIG_MASTER)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS shard_metadata CASCADE;')
    cur.execute('DROP TABLE IF EXISTS friendship CASCADE;')

    cur.execute("""
        CREATE TABLE shard_metadata (
            shard_name VARCHAR PRIMARY KEY,
            lat_min DOUBLE PRECISION,
            lat_max DOUBLE PRECISION,
            long_min DOUBLE PRECISION,
            long_max DOUBLE PRECISION
        );
    """)

    cur.execute("""
                CREATE TABLE friendship (
                user_id   INTEGER NOT NULL,
                friend_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, friend_id)
            );
            """)

    conn.commit()
    cur.close()
    conn.close()
    print("Master DB created with shard metadata and friendship table.")

def recreate_shard(DB_CONFIG):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS userlocation CASCADE;')

    cur.execute("""
        CREATE TABLE userlocation (
            id INTEGER PRIMARY KEY,
            f_name VARCHAR(100),
            l_name VARCHAR(100),
            lat DOUBLE PRECISION,
            long DOUBLE PRECISION
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print(f"Shard DB {DB_CONFIG['dbname']} created.")


def populate_master():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG_MASTER)
    cur = conn.cursor()

    for shard in tqdm(SHARDS_INFO, desc="Initializing master metadata"):
        lat_min = SHARDS_INFO[shard]["lat_min"]
        lat_max = SHARDS_INFO[shard]["lat_max"]
        long_min = SHARDS_INFO[shard]["long_min"]
        long_max = SHARDS_INFO[shard]["long_max"]
        cur.execute(r"""
            INSERT INTO shard_metadata (shard_name, lat_min, lat_max, long_min, long_max)
            VALUES (%s, %s, %s, %s, %s);
        """, [shard, lat_min, lat_max, long_min, long_max])

    for u in tqdm(users, desc="Populating friends for each user..."):
        user_id = u["id"]
        for friend_id in u["friends"]:
            cur.execute("""
                    INSERT INTO friendship (user_id, friend_id)
                    VALUES (%s, %s) ON CONFLICT DO NOTHING;
                    """, (user_id, friend_id))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Friendships added to master DB.")

def populate_shard(DB_CONFIG, lat_min, lat_max, long_min, long_max):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    shard_users = [u for u in users if lat_min <= u["lat"] <= lat_max and long_min <= u["long"] <= long_max]
    data_to_insert = [(u["id"], u["f_name"], u["l_name"], u["lat"], u["long"]) for u in shard_users]

    cur.executemany("""
        INSERT INTO userlocation (id, f_name, l_name, lat, long)
        VALUES (%s, %s, %s, %s, %s)
    """, data_to_insert)

    conn.commit()
    cur.close()
    conn.close()
    print(f"{len(shard_users)} users imported into {DB_CONFIG['dbname']}.")


def get_shards_for_query(lat, lon, distance_km):
    km_per_deg_lat = 111
    km_per_deg_lon = 111 * math.cos(math.radians(lat))

    lat_min_q = lat - distance_km / km_per_deg_lat
    lat_max_q = lat + distance_km / km_per_deg_lat
    lon_min_q = lon - distance_km / km_per_deg_lon
    lon_max_q = lon + distance_km / km_per_deg_lon

    result_shards = []

    for shard_name, shard in SHARDS_INFO.items():
        if not (shard["lat_max"] < lat_min_q or shard["lat_min"] > lat_max_q or
                shard["long_max"] < lon_min_q or shard["long_min"] > lon_max_q):
            result_shards.append(shard_name)

    return result_shards

if __name__ == "__main__":
    create_databases(DB_CONFIG_MASTER, DB_SHARDS)

    recreate_master()
    recreate_shard(DB_SHARDS["shard_nv_db"])
    recreate_shard(DB_SHARDS["shard_ne_db"])
    recreate_shard(DB_SHARDS["shard_sv_db"])
    recreate_shard(DB_SHARDS["shard_se_db"])

    populate_master()
    populate_shard(DB_SHARDS["shard_nv_db"], lat_min=SHARDS_INFO["shard_nv_db"]["lat_min"], lat_max=SHARDS_INFO["shard_nv_db"]["lat_max"],
                                            long_min=SHARDS_INFO["shard_nv_db"]["long_min"], long_max=SHARDS_INFO["shard_nv_db"]["long_max"])
    populate_shard(DB_SHARDS["shard_ne_db"], lat_min=SHARDS_INFO["shard_ne_db"]["lat_min"], lat_max=SHARDS_INFO["shard_ne_db"]["lat_max"],
                                            long_min=SHARDS_INFO["shard_ne_db"]["long_min"], long_max=SHARDS_INFO["shard_ne_db"]["long_max"])
    populate_shard(DB_SHARDS["shard_sv_db"], lat_min=SHARDS_INFO["shard_sv_db"]["lat_min"], lat_max=SHARDS_INFO["shard_sv_db"]["lat_max"],
                                            long_min=SHARDS_INFO["shard_sv_db"]["long_min"], long_max=SHARDS_INFO["shard_sv_db"]["long_max"])
    populate_shard(DB_SHARDS["shard_se_db"], lat_min=SHARDS_INFO["shard_se_db"]["lat_min"], lat_max=SHARDS_INFO["shard_se_db"]["lat_max"],
                                            long_min=SHARDS_INFO["shard_se_db"]["long_min"], long_max=SHARDS_INFO["shard_se_db"]["long_max"])
