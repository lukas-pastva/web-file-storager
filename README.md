# Web File Storager 📂🖼️🎞️

Light‑weight Django 5 app that lets you **upload, list and preview media files**
(images & videos) **without ever touching your container’s source tree**.  
All user data lives in the **Docker volume mounted at `/data`** – so you can
re‑build or replace the image at will while keeping the files safe.

---

## ✨  Key features

| Feature | Details |
|---------|---------|
| **Upload** | Drag‑and‑drop or _Choose File_ (any file that matches the allow‑list) |
| **Gallery** | Thumbnails for images, video icon 🎞️ for videos, generic icon 📄 for others |
| **Direct links** | Every entry is a direct `<a href>` to the stored object – opens in new tab |
| **Immutable code → mutable data** | Source code lives under **`/app`** (read‑only inside container).<br>All uploads go to **`/data`** – the only writeable path. |
| **Zero DB** | No migrations or models – indexes are generated on the fly. |
| **One‑click CI build** | GitHub Actions workflow builds & pushes `lukaspastva/<repo>:<sha>` |

---

## 🗃️  Directory layout (monorepo)

```
web-file-storager/
│
├── .github/workflows/build.yaml     # CI build → Docker Hub
├── src/                             # Everything that goes into the image
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── mysite/                      # Django “project package” (settings, urls…)
│   └── web_file_storager/           # Django “app package” (views, templates…)
└── data/                            # <— not committed; host‑side volume with media
```

Inside the running container it looks like this:

| Container path | Purpose | Mounted? |
|----------------|---------|----------|
| `/app` | Source code copied in by Dockerfile | **read‑only** |
| `/data` | All uploaded files | **read‑write volume** |

---

## 🚀  Quick start (with Docker)

```bash
git clone https://github.com/<you>/web-file-storager.git
cd web-file-storager

# Build the image from ./src
docker build -t web-file-storager ./src

# Create a host directory for persistent files
mkdir -p data

# Run the container, binding port 8000 and mounting ./data → /data
docker run --rm -it       -p 8000:8000       -v "$(pwd)/data:/data"       web-file-storager
```

Open **http://localhost:8000**  
* Upload a few `.jpg` / `.mp4` files.  
* Thumbnails appear instantly; click any item to open it in a new tab.

> **Tip:** If you only need read‑only mode (e.g. in production),
> mount the volume with `:ro`:
> `-v /mnt/media:/data:ro`

---

## ⚙️  Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | `change-me` | Override for `SECRET_KEY` |
| `DEBUG` | `false` | Set `true` for Django debug mode & `/media/` serving |
| `SQLITE_PATH` | `:memory:` | Not really used, but keeps Django happy if you want a file DB |

---

## 🔒  Security model

| Attack surface | Mitigation |
|----------------|------------|
| Path traversal (`../../app/*`) | Django’s `FileSystemStorage` + `relpath` checks in `utils.py` |
| Upload of disallowed types | Extension white‑list in settings & form validation |
| Access to source code | Container mounts source at `/app` **read‑only**; no upload or list endpoint points there |
| CSRF | Django’s default middleware and template tag `{% csrf_token %}` |
| Secrets in image | `SECRET_KEY` provided at run time via env/CI secrets |

---

## 🤖  CI/CD pipeline

1. **GitHub Actions** – `.github/workflows/build.yaml`  
   * Push to `main` → build image **from `src/`** → push to Docker Hub with tag `<sha>`.
2. **Deployment** – Pull the tagged image and run it exactly as in Quick start, mounting the same `/data` volume that your host (or Kubernetes PVC) provides.

---

## 🛠️  Local development (without Docker)

```bash
cd src
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=mysite.settings
export DEBUG=true               # enable /media/ in dev
export DJANGO_SECRET_KEY="dev"
python manage.py runserver 8000
```

Uploads will still go to `/data` – so either:

```bash
mkdir -p /data  # if you are on Linux and want a global dir
#    – or –
export MEDIA_DIR="$(pwd)/../data"   # override in shell before runserver
```

---

## ➕  Extending

* **Video previews** – swap the 🎞️ icon div for an actual `<video controls>` tag.  
* **Authentication** – add `django.contrib.auth`, flip `DEBUG = False` and protect
  upload with `@login_required`.  
* **Database models** – if you ever need metadata, create a model with `FileField(storage=…)` pointing at `/data`.

---

Happy storing! 📦
