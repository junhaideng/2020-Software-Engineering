from django.urls import path
from .views import *

app_name = "feedback"
urlpatterns = [
    path("", index, name='index')
]
