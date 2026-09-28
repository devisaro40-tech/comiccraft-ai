from pathlib import Path

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from .ai.gemini_flash import generate_outline, generate_story


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": "ComicCraft",
            "form": None,
            "error": None,
        },
    )


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        outline = generate_outline(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        story = generate_story(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            outline=outline,
        )

        return {
            "message": "Comic story generated successfully!",
            "story": [
                panel.model_dump()
                for panel in story
            ],
        }

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "app_name": "ComicCraft",
                "form": {
                    "story_prompt": story_prompt,
                    "character_name": character_name,
                    "setting": setting,
                    "tone": tone,
                    "art_style": art_style,
                },
                "error": str(exc),
            },
        )