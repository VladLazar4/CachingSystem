import json
import redis
from time import perf_counter

r = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
JSON_FILE = "../../data/users_100000.json"

def import_json_to_db():
    with open(JSON_FILE, 'r') as f:
        users = json.load(f)
#     "f_name": "Diana",
#     "l_name": "Vasilescu",
#     "lat": 46.005323,
#     "long": 28.343329     
    for (idx, u) in enumerate(users):
        long = float(u['long'])
        lat = float(u['lat'])
        r.execute_command("GEOADD", "users", long, lat, f"{idx}")
        r.execute_command(
            "HSET", f"{idx}",
            "f_name", f"{u['f_name']}",
            "l_name", f"{u['l_name']}",
            "lat", f"{u['lat']}",
            "long", f"{u['long']}"
        )

    print(f"Inserted {len(users)} into Redis db!\n")

if __name__ == "__main__":
    import_json_to_db()