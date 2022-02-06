
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('articles/', views.get_articles),
    path('articles/<str:cat>', views.get_articles_by_cat),
]
