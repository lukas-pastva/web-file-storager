from django.views.generic import TemplateView
from .utils import iter_media_files


class MediaListView(TemplateView):
    template_name = "web_file_storager/list_media.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["media_files"] = sorted(iter_media_files())
        return ctx
