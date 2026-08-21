from actions import *
from keyboard import *
from data import *
from context import context
from speech import speak
from parser import normalizeCalculator
from utils import wait, remember


def execute(action, target, argument):

    success = False

    if action == "open":
        if not target:
            speak("What would you like me to open?")

        elif target in applications:
            openApplication(applications[target])
            context["app"] = target
            context["website"] = None
            context["last_target"] = target
            success = True

        elif target in websites:
            if context["app"] != "google":
                openApplication(applications["google"])
                wait(2)
                context["app"] = "google"

            openWebsite(websites[target])
            context["website"] = target
            context["last_target"] = target
            success = True

        elif target in folders:
            openFolder(folders[target])
            context["app"] = "file manager"
            context["website"] = None
            context["last_target"] = "file manager"
            success = True

        else:
            speak("I don't know that application.")

    elif action == "search":
        if target is None:
            target = context["website"]

        if target is None and context["app"] == "google":
            target = "google"

        if not target:
            speak("What would you like me to search?")

        elif not argument:
            speak(f"Search {target} for what?")

        elif target in websites:
            if context["website"] != target:
                openWebsite(websites[target])
                context["website"] = target
                context["last_target"] = target
                wait(2)

            searchOnWebsite(argument)
            success = True

        elif target == "google":
            if context["app"] != "google":
                openApplication(applications["google"])
                wait(2)
                context["app"] = "google"
                context["last_target"] = "google"

            searchInBrowser(argument)
            success = True

        elif target == "menu":
            searchInMenu(argument)
            success = True

        else:
            speak("I can't search that website yet.")

    elif action == "run":
        if not argument:
            speak("What command would you like me to run?")
        else:
            runCommandInTerminal(argument)
            success = True

    elif action == "repeat":
        if not context["history"]:
            speak("There is nothing to repeat.")
            return

        last = context["history"][-1]
        execute(last["action"], last["target"], last["argument"])
        return  # Don't remember "repeat" itself

    elif action == "back":
        keyCombo("alt", "left")
        success = True

    elif action == "shutdown":
        shutdown()
        success = True

    elif action == "suspend":
        suspend()
        success = True

    elif action == "reboot":
        reboot()
        success = True

    elif action == "find":
        if not argument:
            speak("What would you like me to find?")
        else:
            openApplication(applications["google"])
            wait(2)
            searchInBrowser(argument)
            success = True

    elif action == "close":
        if not target:
            speak("What should I close?")

        elif target in applications:
            closeApplication()
            success = True

        elif target in websites:
            closeTab()
            success = True

        else:
            speak("I don't know how to close that.")

    elif action == "click":
        mouseClick(argument)
        success = True

    elif action == "press":
        keyboardPress(argument)
        success = True

    elif action in ["copy", "paste", "cut", "undo", "redo", "save"]:
        shortcuts(action)
        success = True

    elif action == "select":
        selectAll()
        success = True

    elif action == "type":
        mode = app_modes.get(context["app"], "text")

        if mode == "math":
            argument = normalizeCalculator(argument)

        writeText(argument)
        success = True

    elif action == "volume":
        if argument == "up":
            volumeUp()
            success = True
        elif argument == "down":
            volumeDown()
            success = True

    elif action == "brightness":
        if argument == "up":
            brightnessUp()
            success = True
        elif argument == "down":
            brightnessDown()
            success = True

    else:
        speak("Sorry, I could not understand that command")

    if success:
        remember(action, target, argument)
