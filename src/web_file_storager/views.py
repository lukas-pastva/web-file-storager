from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .utils import iter_media_files
from .forms import MediaUploadForm


class MediaListView(TemplateView):
    """
    GET  → zobrazí zoznam médií + upload form
    POST → uloží súbor do /data (ak prípona povolená) a redirectne späť
    """
    template_name = "web_file_storager/list_media.html"
    storage = FileSystemStorage(location=settings.MEDIA_DIR)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["media_files"] = sorted(iter_media_files())
        ctx["form"] = MediaUploadForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            # FileSystemStorage zabráni path‑traversalu a pri kolízii pridá suffix
            self.storage.save(file.name, file)
        return redirect("media-list")
