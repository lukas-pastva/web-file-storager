from django.urls import path, include, re_path
from django.conf import settings
from django.http import FileResponse, Http404
from pathlib import Path
import logging

urlpatterns = [
    path("", include("web_file_storager.urls")),
]

# ─────────────────────────────────────────────────────────────
#  VLASTNÉ SERVOVANIE MÉDIÍ – funguje aj keď DEBUG=False
# ─────────────────────────────────────────────────────────────
logger = logging.getLogger("media")

def media_serve(request, path: str):
    """
    Bezpečne vráti súbor z /data.
    • Stráži path‑traversal.
    • Loguje do stdout, aby si v pod/cont‑logu videl, čo sa servuje.
    """
    file_path = (settings.MEDIA_DIR / path).resolve()

    try:
        # path‑traversal guard
        file_path.relative_to(settings.MEDIA_DIR)
    except ValueError:
        logger.warning("❌  Traversal attempt: %s", path)
        raise Http404()

    if not file_path.exists():
        logger.warning("❌  File not found: %s", file_path)
        raise Http404()

    logger.info("📤  Serving media: %s", file_path)
    return FileResponse(open(file_path, "rb"))

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", media_serve, name="media"),
]
