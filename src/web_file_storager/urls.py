from django.urls import path
from .views import MediaListView

urlpatterns = [
    path("", MediaListView.as_view(), name="media-list"),
]
