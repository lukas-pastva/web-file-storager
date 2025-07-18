from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # main web-file-storager app
    path("", include("web_file_storager.urls")),
]

# ------------------------------------------------------------------
# MEDIA FILES
# ------------------------------------------------------------------
# For this small utility app we expose /media/ directly from Django,
# so image thumbnails & full‑size files work out‑of‑the‑box even if
# DEBUG=False (e.g. in Docker/Gunicorn without Nginx in front).
#
# In a larger production stack you’d typically move this to Nginx:
#     location /media/ { alias /data/; }
# but keeping it here keeps the container self‑contained.
# ------------------------------------------------------------------
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
    show_indexes=True,   # directory index if someone hits /media/
)
