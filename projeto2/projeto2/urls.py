"""projeto2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , app_views.home),
    path('list/', app_views.listrecipes, name="list_recipes"),
    path('listFiltered/', app_views.applyFilters, name="list_recipesFiltered"),
    path('add/', app_views.add_receita, name='add_receita'),
    path('edit/', app_views.edit_receita, name='edit_receita'),
    path('add_recipe/', app_views.add_recipe, name='add_recipe'),
    path('edit_recipe/', app_views.edit_recipe, name='edit_recipe'),
    path('del/', app_views.del_recipe, name='del'),
    path('delete/', app_views.delete, name='delete'),
    path('showrec/<str:recipe>/', app_views.show_recipe, name='show_recipe'),
]
