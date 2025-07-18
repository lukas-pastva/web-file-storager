from pathlib import Path
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import MediaUploadForm
from .utils import iter_media_files

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}


def _classify(path_str: str) -> str:
    ext = Path(path_str).suffix.lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext in VIDEO_EXTS:
        return "video"
    return "other"


class MediaListView(TemplateView):
    template_name = "web_file_storager/list_media.html"
    storage = FileSystemStorage(location=settings.MEDIA_DIR)

    # ────────────────────────────────────────────────────────────
    #  CONTEXT DATA
    # ────────────────────────────────────────────────────────────
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        files = sorted(iter_media_files())
        ctx["media"] = [
            {"name": f, "type": _classify(f), "url": f"{settings.MEDIA_URL}{f}"}
            for f in files
        ]
        ctx["form"] = MediaUploadForm()
        return ctx

    # ────────────────────────────────────────────────────────────
    #  POST – UPLOAD alebo DELETE
    # ────────────────────────────────────────────────────────────
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", "upload")

        # ——— DELETE ————————————————————————————————
        if action == "delete":
            rel = request.POST.get("filename", "")
            if not rel:
                return HttpResponseBadRequest("Missing filename.")

            try:
                file_path = (settings.MEDIA_DIR / Path(rel)).resolve()
                file_path.relative_to(settings.MEDIA_DIR)      # path‑traversal guard
            except Exception:
                return HttpResponseBadRequest("Invalid path")

            if file_path.exists():
                file_path.unlink()
            return redirect("media-list")

        # ——— UPLOAD (default) ——————————————
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            self.storage.save(file.name, file)
        return redirect("media-list")
