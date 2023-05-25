from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('cars/<str:slug>/', views.car_detail, name='car')
]
