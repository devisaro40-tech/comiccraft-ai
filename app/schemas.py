from pydantic import BaseModel


class PanelOutline(BaseModel):
    panel_number: int
    scene_description: str
    character_action: str
    dialogue: str
    visual_prompt: str


class StoryPanel(BaseModel):
    panel_number: int
    narration: str
    dialogue: str
    visual_prompt: str