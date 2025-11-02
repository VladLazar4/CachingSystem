JSON_FILE = "../../data/users_1000.json"


DB_CONFIG_MASTER = {
    "dbname": "master_db",
    "user": "vlad",
    "password": "vlad123",
    "host": "db",
    "port": 5432
}

DB_SHARDS = {
    "shard_north_db": {
        "dbname": "shard_north_db",
        "user": "vlad",
        "password": "vlad123",
        "host": "db",
        "port": 5432
    },
    "shard_south_db": {
        "dbname": "shard_south_db",
        "user": "vlad",
        "password": "vlad123",
        "host": "db",
        "port": 5432
    }
}

SHARDS_INFO = {
    "shard_north_db":{
        "lat_min": 46.0,
        "lat_max": 49.0,
        "long_min": 20.0,
        "long_max": 40.0,
    },
    "shard_south_db":{
        "lat_min": 43.0,
        "lat_max": 45.99,
        "long_min": 20.0,
        "long_max": 40.0,
    }

}
