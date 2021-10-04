"""FavoriteBooks URL Configuration

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
     path('logout/', views.logout),
    path('register/', views.register),
    path('login/', views.login),
    path('books/', views.books),
    path('books/add/', views.add_book),
    path('books/<int:book_id>/delete/', views.delete_book),
    path('books/<int:book_id>/update/', views.update_book),
    path('books/<int:book_id>/favorite/', views.add_to_favorite),
    path('books/<int:book_id>/unfavorite/', views.remove_from_favorite),
    path('books/<int:book_id>', views.book_info),
    path('home/', views.homepage),
]
