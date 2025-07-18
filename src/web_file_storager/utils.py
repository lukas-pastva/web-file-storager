from pathlib import Path
from django.conf import settings


def iter_media_files():
    """
    Vyhľadá všetky súbory v /data (rekurzívne) a vráti iba tie, ktoré majú
    povolenú príponu definovanú v settings.ALLOWED_MEDIA_EXTS.
    Cesty vracia relatívne k /data, aby sa predišlo path‑traversalu.
    """
    base: Path = settings.MEDIA_DIR

    for path in base.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() in settings.ALLOWED_MEDIA_EXTS:
            try:
                rel = path.relative_to(base)
            except ValueError:
                # Súbor mimo /data – ignorujeme
                continue
            yield rel.as_posix()
