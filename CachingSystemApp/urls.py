from django.urls import path
from . import views

urlpatterns = [
    path('nearby/', views.nearby_users, name='nearby_users'),
    path('proximity/', views.proximity_search, name='proximity_search'),
]
