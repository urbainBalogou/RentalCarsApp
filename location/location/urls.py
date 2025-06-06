"""
URL configuration for location project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import login_user, logout_user
from django.views.generic import TemplateView

from .import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', include('accounts.urls')),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('list_care/', include("list.urls")),
    path('google978439f45eca2181.html', TemplateView.as_view(template_name="google978439f45eca2181.html", content_type='text/html')),
    path('', include("main.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
