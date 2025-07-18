from pathlib import Path
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import MediaUploadForm
from .utils import iter_media_files

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}


def _classify(path_str: str) -> str:
    """Return 'image' | 'video' | 'other' based on extension."""
    ext = Path(path_str).suffix.lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext in {".mp4", ".mov", ".m4v", ".avi", ".mkv"}:
        return "video"
    return "other"


class MediaListView(TemplateView):
    """
    GET  – zoznam + upload formulár
    POST – uloží súbor a redirectne späť
    """
    template_name = "web_file_storager/list_media.html"
    storage = FileSystemStorage(location=settings.MEDIA_DIR)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        files = sorted(iter_media_files())
        ctx["media"] = [
            {
                "name": f,
                "type": _classify(f),
                "url": f"{settings.MEDIA_URL}{f}",
            }
            for f in files
        ]
        ctx["form"] = MediaUploadForm()
        ctx["MEDIA_URL"] = settings.MEDIA_URL  # pre template k priamemu použitiu
        return ctx

    def post(self, request, *args, **kwargs):
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            self.storage.save(file.name, file)
        return redirect("media-list")
