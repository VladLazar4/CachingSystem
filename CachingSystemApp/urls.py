from django.urls import path
from . import views

urlpatterns = [
    path('nearby/', views.nearby_users, name='nearby_users'),
    path('proximity/', views.proximity_search, name='proximity_search'),
    path('proximity_redis/', views.proximity_search_redis, name='proximity_search_redis'),
]
