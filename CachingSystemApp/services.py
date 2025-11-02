import time
import psycopg2

from .scripts.db_queries import get_shards_for_query
from .scripts.config import DB_SHARDS, DB_CONFIG_MASTER

def find_nearby_friends(user_id, lat_ref, long_ref, distance_km):
    start = time.perf_counter()
    results = []
    total_friends = 0

    master_conn = psycopg2.connect(**DB_CONFIG_MASTER)
    master_cur = master_conn.cursor()
    master_cur.execute("SELECT friend_id FROM friendship WHERE user_id = %s;", (user_id,))
    friend_ids = [row[0] for row in master_cur.fetchall()]
    master_cur.close()
    master_conn.close()

    if not friend_ids:
        return [], 0, 0

    shards = get_shards_for_query(lat_ref, long_ref, distance_km)

    for shard_name in shards:
        DB_CONFIG = DB_SHARDS[shard_name]
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        query = f"""
            SELECT id, f_name, l_name, lat, long, distance
            FROM (
                SELECT id, f_name, l_name, lat, long,
                    6371 * acos(
                        cos(radians(%s)) * cos(radians(lat)) *
                        cos(radians(long) - radians(%s)) +
                        sin(radians(%s)) * sin(radians(lat))
                    ) AS distance
                FROM userlocation
                WHERE id = ANY(%s)
            ) AS sub
            WHERE distance < %s
            ORDER BY distance;
        """

        cur.execute(query, [lat_ref, long_ref, lat_ref, friend_ids,
                            distance_km])
        rows = cur.fetchall()

        total_friends += len(rows)
        for row in rows:
            results.append({
                "id": row[0],
                "f_name": row[1],
                "l_name": row[2],
                "lat": row[3],
                "long": row[4],
                "distance": round(row[5], 2)
            })

        cur.close()
        conn.close()

    query_time_ms = round((time.perf_counter() - start) * 1000, 2)
    results.sort(key=lambda x: x["distance"])
    return results, query_time_ms, total_friends

    # with connection.cursor() as cursor:
    #     start = time.perf_counter()
    #     query = """
    #         SELECT *
    #         FROM (
    #             SELECT u.id, u.f_name, u.l_name, u.lat, u.long,
    #                 6371 * acos(
    #                     cos(radians(%s)) * cos(radians(lat)) *
    #                     cos(radians(long) - radians(%s)) +
    #                     sin(radians(%s)) * sin(radians(lat))
    #                 ) AS distance
    #             FROM "CachingSystemApp_userlocation" u
    #             WHERE u.id IN (
    #                 SELECT f.friend_id
    #                 FROM "CachingSystemApp_friendship" f
    #                 WHERE f.user_id = %s
    #             )
    #         ) AS sub
    #         WHERE distance < %s
    #         ORDER BY distance;
    #     """
    #
    #     cursor.execute(query, [lat_ref, long_ref, lat_ref, user_id, distance_km])
    #
    #     rows = cursor.fetchall()
    #
    # result = []
    # for row in rows:
    #     result.append({
    #         "id": row[0],
    #         "f_name": row[1],
    #         "l_name": row[2],
    #         "lat": row[3],
    #         "long": row[4],
    #         "distance": round(row[5], 2)
    #     })
    # query_time_ms = round((time.perf_counter() - start) * 1000, 2)
    # return result, query_time_ms, len(rows)
