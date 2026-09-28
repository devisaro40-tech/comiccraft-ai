from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

static_dir.mkdir(
    parents=True,
    exist_ok=True,
)

(static_dir / "panels").mkdir(
    parents=True,
    exist_ok=True,
)

(static_dir / "exports").mkdir(
    parents=True,
    exist_ok=True,
)


app = FastAPI(
    title=settings.app_name,
    description=(
        "Generative AI powered comic "
        "story creation platform."
    ),
    version="1.0.0",
    debug=settings.debug,
)


app.mount(
    "/static",
    StaticFiles(directory=str(static_dir)),
    name="static",
)


app.include_router(
    router
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": settings.app_name,
    }