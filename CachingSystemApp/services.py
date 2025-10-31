import time

from django.db import connection
import math

def find_nearby_users(lat_ref, long_ref, distance_km):
    with connection.cursor() as cursor:
        start = time.perf_counter()
        query = """
            SELECT *
            FROM (
                SELECT id, f_name, l_name, lat, long,
                    6371 * acos(
                        cos(radians(%s)) * cos(radians(lat)) *
                        cos(radians(long) - radians(%s)) +
                        sin(radians(%s)) * sin(radians(lat))
                    ) AS distance
                FROM "CachingSystemApp_userlocation"
            ) AS sub
            WHERE distance < %s
            ORDER BY distance;
        """

        cursor.execute(query, [lat_ref, long_ref, lat_ref, distance_km])

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
