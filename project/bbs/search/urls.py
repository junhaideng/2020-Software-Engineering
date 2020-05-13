from django.urls import path
from .views import *
app_name = "search"
urlpatterns = [
    path("", search, name='search'),
    path("course/", search_course, name="search_course"),
    path("post/", search_post, name="search_post"),
]