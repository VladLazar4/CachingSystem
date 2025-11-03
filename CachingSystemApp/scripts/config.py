import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "..", "..", "data", "users_1000.json")

DB_CONFIG_MASTER = {
    "dbname": "master_db",
    "user": "vlad",
    "password": "vlad123",
    "host": "db",
    "port": 5432
}

DB_SHARDS = {
    "shard_nv_db": {
        "dbname": "shard_nv_db",
        "user": "vlad",
        "password": "vlad123",
        "host": "db",
        "port": 5432
    },
    "shard_ne_db": {
        "dbname": "shard_ne_db",
        "user": "vlad",
        "password": "vlad123",
        "host": "db",
        "port": 5432
    },
    "shard_sv_db": {
        "dbname": "shard_sv_db",
        "user": "vlad",
        "password": "vlad123",
        "host": "db",
        "port": 5432
    },
    "shard_se_db": {
        "dbname": "shard_se_db",
        "user": "vlad",
        "password": "vlad123",
        "host": "db",
        "port": 5432
    }
}

SHARDS_INFO = {
    "shard_nv_db":{
        "lat_min": 46.5,
        "lat_max": 50.0,
        "long_min": 20.0,
        "long_max": 25.0,
    },
    "shard_ne_db":{
        "lat_min": 46.5,
        "lat_max": 50.0,
        "long_min": 25.0,
        "long_max": 30.0,
    },
    "shard_sv_db": {
        "lat_min": 43.0,
        "lat_max": 46.5,
        "long_min": 20.0,
        "long_max": 25.0,
    },
    "shard_se_db": {
        "lat_min": 43.0,
        "lat_max": 46.5,
        "long_min": 25.0,
        "long_max": 30.0,
    }
}
