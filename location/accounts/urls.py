from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup, name="signup"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView, name='password_reset_confirm')
]
