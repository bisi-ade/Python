"""semi_restful_tv_show URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.shows),
    path('shows/new', views.new_show),
    path('create_new_show', views.create_new_show),
    path('shows/<int:id>/edit', views.edit),
    path('shows/<int:id>/destroy', views.destroy),
    path('update', views.update),
    path('shows/<int:id>', views.show)
]
