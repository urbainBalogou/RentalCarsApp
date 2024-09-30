from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="main"),
    path('nos_Services/', views.Services, name="nos_Services"),
]
