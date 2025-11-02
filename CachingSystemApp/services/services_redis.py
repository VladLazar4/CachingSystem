import redis
import time


def find_nearby_users_redis(lat_ref, long_ref, distance_km):
    with redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True) as r:
        start = time.perf_counter()
        
        results = r.execute_command(
            "GEOSEARCH", "users",
            "FROMLONLAT", long_ref, lat_ref,
            "BYRADIUS", distance_km, "km",
            "WITHDIST", "ASC"
        )
        query_time_ms = round((time.perf_counter() - start) * 1000, 2)
        
        final_result = []
        for user_id, distance in results:
            user_info = r.execute_command("HGETALL", user_id)  #this return key, value, key, value ...
            print(type(user_info), user_info)
            #user_info = dict(zip(user_info[::2], user_info[1::2]))
            final_result.append({
                "id": user_id,
                "f_name": user_info['f_name'],
                "l_name": user_info['l_name'],
                "lat": user_info['lat'],
                "long": user_info['long'],
                "distance": round(float(distance), 2)
            })
        
    return final_result, query_time_ms, len(results)