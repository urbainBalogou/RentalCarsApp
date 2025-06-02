from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('cars/<str:slug>/', views.car_detail, name='car'),
path('reservation/success/', views.succes_page, name='succes_page'),
path('mes_reservations/', views.reservations, name='reservation')
]
