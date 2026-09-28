import json

from google import genai
from google.genai import types

from ..config import settings
from ..prompts import build_outline_prompt, build_story_prompt
from ..schemas import PanelOutline, StoryPanel


class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate_outline(
        self,
        story_prompt: str,
        character_name: str,
        setting: str,
        tone: str,
        art_style: str,
    ) -> list[PanelOutline]:

        prompt = build_outline_prompt(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
            num_panels=settings.num_panels,
        )

        response = self.client.models.generate_content(
            model=settings.gemini_outline_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json",
                response_schema=list[PanelOutline],
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty outline."
            )

        data = json.loads(response.text)

        panels = [
            PanelOutline.model_validate(item)
            for item in data
        ]

        if len(panels) != settings.num_panels:
            raise RuntimeError(
                f"Expected {settings.num_panels} panels, "
                f"but Gemini returned {len(panels)}."
            )

        return panels

    def generate_story(
        self,
        story_prompt: str,
        character_name: str,
        setting: str,
        tone: str,
        outline: list[PanelOutline],
    ) -> list[StoryPanel]:

        outline_json = json.dumps(
            [
                panel.model_dump()
                for panel in outline
            ],
            ensure_ascii=False,
            indent=2,
        )

        prompt = build_story_prompt(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            outline_json=outline_json,
        )

        response = self.client.models.generate_content(
            model=settings.gemini_story_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9,
                response_mime_type="application/json",
                response_schema=list[StoryPanel],
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty story."
            )

        data = json.loads(response.text)

        panels = [
            StoryPanel.model_validate(item)
            for item in data
        ]

        if len(panels) != settings.num_panels:
            raise RuntimeError(
                f"Expected {settings.num_panels} story panels, "
                f"but Gemini returned {len(panels)}."
            )

        return panels


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
):
    service = GeminiService()

    return service.generate_outline(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style,
    )


def generate_story(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    outline: list[PanelOutline],
):
    service = GeminiService()

    return service.generate_story(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        outline=outline,
    )