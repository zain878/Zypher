from pathlib import Path

import cv2
import numpy as np
import pyautogui as pag


PROJECT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = PROJECT_DIR / "templates"


def findTemplate(template_path):
    template_path = Path(template_path)

    if not template_path.is_file():
        print(f"Template file not found: {template_path}")
        return None

    screen = pag.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    template = cv2.imread(str(template_path))

    if template is None:
        print(f"Could not read template image: {template_path}")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, maxVal, _, maxLoc = cv2.minMaxLoc(result)

    print("Match confidence:", maxVal)

    if maxVal < 0.75:
        return None

    height, width = template.shape[:2]
    x, y = maxLoc

    return x + width // 2, y + height // 2


search_templates = {
    "youtube": TEMPLATES_DIR / "yt_search.png",
    "google": TEMPLATES_DIR / "google_search.png",
    "github": TEMPLATES_DIR / "git_search.png",
    "gmail": TEMPLATES_DIR / "gmail_search.png",
    "facebook": TEMPLATES_DIR / "fb_search.png",
}