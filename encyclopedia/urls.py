from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display_content, name="display_content"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("search_content", views.search_content, name="search_content"),
    path("edit/<str:entry_title>/", views.edit, name="edit"),
    path("random", views.get_random_entry, name="get_random_entry"),
]
