import cv2
import pyautogui as pag
import time
import numpy as np


def findTemplate(template_path):

    screen = pag.screenshot()

    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    template = cv2.imread(template_path)

    if template is None:
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

    print("Match confidence:", maxVal)

    if maxVal < 0.75:
        return None

    height, width = template.shape[:2]

    x, y = maxLoc

    center_x = x + width // 2
    center_y = y + height // 2

    return center_x, center_y


search_templates = {
    "youtube": "templates/yt_search.png",
    "google": "templates/google_search.png",
    "github": "templates/git_search.png",
    "gmail": "templates/gmail_search.png",
    "facebook": "templates/fb_search.png",
}
