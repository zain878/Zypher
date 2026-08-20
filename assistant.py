from speech import listenAudio, speak

from parser import (
    parser,
    normalizeSpeech,
    normalizeCalculator,   # (temporarily, we'll discuss this below)
)

from actions import (
    openApplication,
    closeApplication,
    closeTab,
    openWebsite,
    searchOnWebsite,
    searchInBrowser,
    runCommandInTerminal,
    searchInMenu,
    openFolder,
    volumeUp,
    volumeDown,
    brightnessUp,
    brightnessDown,
)

from keyboard import (
    mouseClick,
    keyboardPress,
    selectAll,
    shortcuts,
    writeText,
)

from data import (
    applications,
    websites,
    folders,
    app_modes,
)

from context import context

from utils import wait

def main():
    while True:
        speech = listenAudio()

        if speech is None:
            continue

        speech = normalizeSpeech(speech)
        if "zypher" not in speech and "zipher" not in speech:
            continue

        # Remove the wake word
        speech = (
            speech.replace("zypher", "", 1)
                  .replace("zipher", "", 1)
                  .strip()
        )

        print(f"You said: '{speech}'")
        action, target, argument = parser(speech)

        # Nothing understood
        if action is None:
            speak("Sorry, I didn't understand.")
            continue

        # Resolve "it" using context
        if target == "it":
            target = context["last_target"]

        if target is None:
            speak("I don't know what 'it' refers to.")
            continue

        if any(word in speech for word in ["stop", "goodbye", "bye"]):
            speak("Signing off. Goodbye, Zain.")
            break

        elif any(word in speech for word in ["hello", "hi", "hey", "hello zypher", "hello zipher"]):
            speak("Hello, Zain. This is Zypher. How can I assist you today?")

        if action == "open":
            if not target:
                speak("What would you like me to open?")

            elif target in applications:
                openApplication(applications[target])
                context["app"] = target
                context["website"] = None
                context["last_target"] = target

            elif target in websites:
                if context["app"] != "google":
                    openApplication(applications["google"])
                    wait(2)
                    context["app"] = "google"

                openWebsite(websites[target])
                context["website"] = target
                context["last_target"] = target

            elif target in folders:
                openFolder(folders[target])
                context["app"] = "file manager"
                context["website"] = None
                context["last_target"] = "file manager"

            else:
                speak("I don't know that application.")

        elif action == "search":
            if target is None:
                target = context["website"]

            if target is None and context["app"] == "google":
                target = "google"

            if not target:
                speak("What would you like me to search")

            elif not argument:
                speak("Search " + target + " for what?")

            elif target in websites:
                if context["website"] != target:
                    openWebsite(websites[target])
                    context["website"] = target
                    context["last_target"] = target

                    wait(2)
                    searchOnWebsite(argument)

            elif target == "google":
                if context["app"] != "google":
                    openApplication(applications["google"])
                    wait(2)

                    context["app"] = "google"
                    context["last_target"] = "google"

                    searchInBrowser(argument)

                else:
                    speak("I can't search there yet.")

            elif target == "menu":
                searchInMenu(argument)

            else:
                speak("I can't search that website yet.")

        elif action == "run":
            if not argument:
                speak("What command would you like me to run?")

            else:
                runCommandInTerminal(argument)

        elif action == "find":
            if not argument:
                speak("What would you like me to find?")

            else:
                openApplication(applications["google"])
                wait(2)
                searchInBrowser(argument)

        elif action == "close":
            if not target:
                speak("What should I close?")

            elif target in applications:
                closeApplication()

            elif target in websites:
                closeTab()

            else:
                speak("I don't know how to close that.")

        elif action == "click":
            mouseClick(argument)

        elif action == "press":
            keyboardPress(argument)

        elif action in ["copy", "paste", "cut", "undo", "redo", "save"]:
            shortcuts(action)

        elif action == "select":
            selectAll()

        elif action == "type":
            mode = app_modes.get(context["app"], "text")

            if mode == "math":
                argument = normalizeCalculator(argument)

            writeText(argument)

        elif action == "volume":
            if argument == "up":
                volumeUp()

            elif argument == "down":
                volumeDown()

        elif action == "brightness":
            if argument == "up":
                brightnessUp()

            elif argument == "down":
                brightnessDown()

        else:
            speak("Sorry, I could not understand that command")

if __name__ == "__main__":
    main()