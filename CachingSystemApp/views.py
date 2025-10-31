from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .services import find_nearby_users

def nearby_users(request):
    lat = float(request.GET.get('lat', 0))
    long = float(request.GET.get('long', 0))
    distance = float(request.GET.get('distance', 5))
    data = find_nearby_users(lat, long, distance)
    return JsonResponse({"nearby_users": data})

@require_GET
def proximity_search(request):
    try:
        lat = float(request.GET.get("lat"))
        long = float(request.GET.get("long"))
        distance_km = float(request.GET.get("distance"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    users, query_time_ms, no_users = find_nearby_users(lat, long, distance_km)

    response = {
        "users": users,
        "pg_query_time_ms": query_time_ms,
        "no_users": no_users
    }
    return JsonResponse(response)

