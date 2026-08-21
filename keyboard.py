import pyautogui as pag

shortcut_keys = {
    "copy": ("ctrl", "c"),
    "paste": ("ctrl", "v"),
    "cut": ("ctrl", "x"),
    "undo": ("ctrl", "z"),
    "redo": ("ctrl", "y"),
    "save": ("ctrl", "s"),
}

def keyPress(key):
    pag.press(key)


def keyCombo(*keys):
    pag.hotkey(*keys)

def writeText(text):
    pag.write(text, interval=0.07)

def mouseClick(click):
    if click == "right":
        pag.rightClick()
    elif click == "left":
        pag.leftClick()
    elif click == "double":
        pag.doubleClick()

def keyboardPress(key):
    if key == "esc":
        keyPress("esc")
    elif key == "enter":
        keyPress("enter")
    elif key == "tab":
        keyPress("tab")
    elif key == "backspace":
        keyPress("backspace")


def selectAll():
    keyCombo("ctrl", "a")


def shortcuts(name):
    keyCombo(*shortcut_keys[name])
