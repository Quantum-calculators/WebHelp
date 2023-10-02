from django.contrib import admin
from django.urls import path
from .views import MainView, check_domain

urlpatterns = [
    path("", MainView.as_view()),
    path("check_domain/", check_domain),
]
