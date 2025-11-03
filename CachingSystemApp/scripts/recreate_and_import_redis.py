import json
import redis
from tqdm import tqdm
from time import perf_counter
from config import JSON_FILE

r = redis.StrictRedis(host="redis_1k", port=6379, decode_responses=True)

def import_json_to_db():
    with open(JSON_FILE, 'r') as f:
        users = json.load(f)
#     "f_name": "Diana",
#     "l_name": "Vasilescu",
#     "lat": 46.005323,
#     "long": 28.343329  
#     "friends": [...]   
    for u in tqdm(users, desc="Populating Redis db"):
        long = float(u['long'])
        lat = float(u['lat'])
        r.execute_command("GEOADD", "users", long, lat, f"{u['id']}")
        r.execute_command(
            "HSET", f"{u['id']}",
            "f_name", f"{u['f_name']}",
            "l_name", f"{u['l_name']}",
            "lat", f"{u['lat']}",
            "long", f"{u['long']}"
        )
        #add friendships
        for friend_id in u['friends']:
            r.execute_command("SADD", f"friends:{u['id']}", friend_id)
            r.execute_command("SADD", f"friends:{friend_id}", u['id'])

    print(f"Inserted {len(users)} into Redis db!\n")

if __name__ == "__main__":
    import_json_to_db()