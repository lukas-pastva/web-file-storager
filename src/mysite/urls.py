from django.urls import path, include

urlpatterns = [
    path("", include("web_file_storager.urls")),
]
