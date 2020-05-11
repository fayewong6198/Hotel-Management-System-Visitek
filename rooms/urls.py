from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('room/<int:room_id>/', views.room, name='room'),
]
