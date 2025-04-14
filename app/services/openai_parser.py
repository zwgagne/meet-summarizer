import re

def parse_openai_summary(raw_text):
    title = None
    key_points = []
    action_items = []

    lines = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]
    section = None

    for line in lines:
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
            section = None
        elif "key point" in line.lower():
            section = "key_points"
        elif "action" in line.lower():
            section = "action_items"
        elif line.startswith("-") or line.startswith("*"):
            content = line[1:].strip()
            if section == "key_points":
                key_points.append(content)
            elif section == "action_items":
                action_items.append(content)

    return {
        "title": title,
        "key_points": key_points,
        "action_items": action_items
    }