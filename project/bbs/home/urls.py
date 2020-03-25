from django.contrib import admin
from django.urls import path
from .views import home

app_name = "home"
urlpatterns = [
    path("", home, name='index'),
]