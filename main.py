"""
Ali Nolan — Personal Website (FastAPI)
Run locally:
    pip install -r requirements.txt
    uvicorn main:app --reload
Then open http://127.0.0.1:8000  and the admin panel at http://127.0.0.1:8000/admin
"""
import copy
import json
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

BASE_DIR = Path(__file__).resolve().parent
CONTENT_FILE = BASE_DIR / "content.json"

# Change these through environment variables on the server (Render dashboard).
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "basra2026")
SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-in-production")

ALLOWED_ICONS = {"code", "cpu", "globe", "car", "github", "mail", "link", "pin", "star", "book"}

DEFAULT_CONTENT = {
    "siteTitle": "Ali Nolan — Programmer · Basra, Iraq",
    "firstName": "Ali",
    "lastName": "Nolan",
    "arabicName": "علي نولان",
    "kicker": "Personal Website",
    "bio": "Programmer and technology enthusiast based in Basra, Iraq. I enjoy building things with code and exploring how software can solve real problems. This is my small corner of the internet.",
    "aboutTitle": "A quiet corner of the internet",
    "aboutP1": "I'm Ali, a programmer from Basra, in the south of Iraq. I like making ideas work through code — from small scripts to full projects — and I'm always curious about new tools, systems, and where technology is heading next.",
    "aboutP2": "Lately I've been exploring automotive programming and ECU diagnostics — learning how cars think, one system at a time.",
    "focusTitle": "What I spend my time on",
    "factLocation": "Basra, Iraq",
    "factCraft": "Programming & technology",
    "factLearning": "Car / ECU programming",
    "contactTitle": "Let's talk",
    "contactText": "The easiest way to reach me is through GitHub — you'll find my work and projects there.",
    "footerAr": "أهلاً وسهلاً",
    "footerText": "© 2026 Ali Nolan · Basra, Iraq",
    "accent": "#9a7434",
    "cards": [
        {"icon": "code", "title": "Code", "text": "Writing software is my craft — from small scripts to full projects, I like making ideas work."},
        {"icon": "globe", "title": "Technology", "text": "Always curious about new tools, systems, and where technology is heading next."},
        {"icon": "car", "title": "Cars & ECUs", "text": "Learning how modern vehicles think: sensors, actuators, diagnostics and ECU programming."},
    ],
    "links": [
        {"icon": "github", "label": "GitHub", "url": "https://github.com/Usjdo299", "style": "solid"},
    ],
}

app = FastAPI(title="Ali Nolan — Personal Website", docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="lax", https_only=False)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'self'"
    )
    return response


# --- storage: Vercel KV (Upstash Redis REST) when configured, local file otherwise ---
KV_URL = os.environ.get("KV_REST_API_URL", "").rstrip("/")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN", "")
KV_KEY = "site_content"


def kv_enabled() -> bool:
    return bool(KV_URL and KV_TOKEN)


def kv_get():
    import urllib.request
    req = urllib.request.Request(KV_URL + "/get/" + KV_KEY, headers={"Authorization": "Bearer " + KV_TOKEN})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    result = data.get("result")
    if not result:
        return None
    try:
        return json.loads(result)
    except (json.JSONDecodeError, TypeError):
        return None


def kv_set(payload: dict) -> None:
    import urllib.request
    body = json.dumps(["SET", KV_KEY, json.dumps(payload, ensure_ascii=False)]).encode("utf-8")
    req = urllib.request.Request(KV_URL, data=body, headers={"Authorization": "Bearer " + KV_TOKEN, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=5) as resp:
        resp.read()


def merge_with_defaults(data: dict) -> dict:
    merged = copy.deepcopy(DEFAULT_CONTENT)
    for key, value in data.items():
        if key in merged and value not in (None, ""):
            merged[key] = value
    return merged


def load_content() -> dict:
    if kv_enabled():
        try:
            data = kv_get()
            if data:
                return merge_with_defaults(data)
        except Exception:
            pass
    if not CONTENT_FILE.exists():
        return copy.deepcopy(DEFAULT_CONTENT)
    try:
        data = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return copy.deepcopy(DEFAULT_CONTENT)
    return merge_with_defaults(data)


def save_content(data: dict) -> None:
    if kv_enabled():
        kv_set(data)
        return
    try:
        CONTENT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass  # read-only filesystem (e.g. serverless without KV)


def clean_content(payload: dict) -> dict:
    """Whitelist and sanitize incoming admin content."""
    out = copy.deepcopy(DEFAULT_CONTENT)
    text_keys = [k for k in DEFAULT_CONTENT if k not in ("cards", "links")]
    for key in text_keys:
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            out[key] = val.strip()[:2000]

    cards = payload.get("cards")
    if isinstance(cards, list) and cards:
        clean_cards = []
        for c in cards[:6]:
            if not isinstance(c, dict):
                continue
            title = str(c.get("title", "")).strip()[:120]
            text = str(c.get("text", "")).strip()[:600]
            icon = str(c.get("icon", "star")).strip()
            if icon not in ALLOWED_ICONS:
                icon = "star"
            if title:
                clean_cards.append({"icon": icon, "title": title, "text": text})
        if clean_cards:
            out["cards"] = clean_cards

    links = payload.get("links")
    if isinstance(links, list) and links:
        clean_links = []
        for l in links[:6]:
            if not isinstance(l, dict):
                continue
            url = str(l.get("url", "")).strip()[:400]
            label = str(l.get("label", "")).strip()[:80]
            icon = str(l.get("icon", "link")).strip()
            style = "ghost" if l.get("style") == "ghost" else "solid"
            if icon not in ALLOWED_ICONS:
                icon = "link"
            if url and (url.startswith("https://") or url.startswith("http://") or url.startswith("mailto:")):
                clean_links.append({"icon": icon, "label": label or url, "url": url, "style": style})
        if clean_links:
            out["links"] = clean_links
    return out


def is_admin(request: Request) -> bool:
    return bool(request.session.get("admin"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"c": load_content()})


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    if is_admin(request):
        return RedirectResponse("/admin", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"error": False})


@app.post("/admin/login")
async def admin_login(request: Request):
    form = await request.form()
    if form.get("password") == ADMIN_PASSWORD:
        request.session["admin"] = True
        return RedirectResponse("/admin", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"error": True}, status_code=401)


@app.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    if not is_admin(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse(request, "admin.html", {"c": load_content()})


@app.get("/admin/content")
async def admin_content(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    return load_content()


@app.post("/admin/save")
async def admin_save(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)
    if not isinstance(payload, dict):
        return JSONResponse({"error": "invalid payload"}, status_code=400)
    cleaned = clean_content(payload)
    save_content(cleaned)
    return {"ok": True, "content": cleaned}


@app.post("/admin/reset")
async def admin_reset(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    save_content(DEFAULT_CONTENT)
    return {"ok": True, "content": copy.deepcopy(DEFAULT_CONTENT)}
