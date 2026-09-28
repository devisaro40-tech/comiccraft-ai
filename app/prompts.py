def build_outline_prompt(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style,
    num_panels,
):
    return f"""
Create a {num_panels}-panel comic outline.

Story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

For each panel provide:
- panel_number
- scene_description
- character_action
- dialogue
- visual_prompt

Return only valid JSON.
"""


def build_story_prompt(
    story_prompt,
    character_name,
    setting,
    tone,
    outline_json,
):
    return f"""
Create the final comic story using the outline below.

Story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Outline:
{outline_json}

For every panel provide:
- panel_number
- narration
- dialogue
- visual_prompt

Return only valid JSON.
"""