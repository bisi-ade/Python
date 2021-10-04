"""Handy_Helper2 URL Configuration

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
    path('', views.index),
    path('dashboard', views.dashboard),
    path('jobs/edit/<int:id>', views.jobsEdit),
    path('jobs/new', views.jobsNew),
    path('jobs_info/<int:id>', views.jobs_info),
    path('rd/register', views.register),
    path('rd/login', views.login),
    path('rd/logout', views.logout),
    path('rd/new_job', views.new_job),
    path('rd/edit_job/<int:id>', views.edit_job),
    path('rd/remove_job/<int:id>', views.remove_job),
    path('rd/take_job/<int:id>', views.take_job),
    path('rd/give_up_job/<int:id>', views.give_up_job),
]
