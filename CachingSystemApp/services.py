import time

from django.db import connection

def find_nearby_friends(user_id, lat_ref, long_ref, distance_km):
    with connection.cursor() as cursor:
        start = time.perf_counter()
        query = """
            SELECT *
            FROM (
                SELECT u.id, u.f_name, u.l_name, u.lat, u.long,
                    6371 * acos(
                        cos(radians(%s)) * cos(radians(lat)) *
                        cos(radians(long) - radians(%s)) +
                        sin(radians(%s)) * sin(radians(lat))
                    ) AS distance
                FROM "CachingSystemApp_userlocation" u
                WHERE u.id IN (
                    SELECT f.friend_id
                    FROM "CachingSystemApp_friendship" f
                    WHERE f.user_id = %s
                )
            ) AS sub
            WHERE distance < %s
            ORDER BY distance;
        """

        cursor.execute(query, [lat_ref, long_ref, lat_ref, user_id, distance_km])

        rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "f_name": row[1],
            "l_name": row[2],
            "lat": row[3],
            "long": row[4],
            "distance": round(row[5], 2)
        })
    query_time_ms = round((time.perf_counter() - start) * 1000, 2)
    return result, query_time_ms, len(rows)
