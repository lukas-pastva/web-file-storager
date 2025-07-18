from django.core.management.base import BaseCommand
from web_file_storager.utils import iter_media_files


class Command(BaseCommand):
    help = "Prečíta /data a vypíše počet podporovaných médií."

    def handle(self, *args, **options):
        media = list(iter_media_files())
        self.stdout.write(f"Nájdených {len(media)} podporovaných súborov.")
