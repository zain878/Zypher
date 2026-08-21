from utils import remember
from execute import execute
from speech import listenAudio, speak

from parser import (
    parser,
    normalizeSpeech,
    normalizeCalculator, 
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
        # if "zypher" not in speech and "zipher" not in speech:
        #     continue

        # # Remove the wake word
        # speech = (
        #     speech.replace("zypher", "", 1)
        #           .replace("zipher", "", 1)
        #           .strip()
        # )
        if any(word in speech for word in ["stop", "goodbye", "bye"]):
                speak("Signing off. Goodbye, Zain.")
                break
        
        elif any(word in speech for word in ["hello", "hi", "hey", "hello zypher", "hello zipher"]):
            speak("Hello, Zain. This is Zypher. How can I assist you today?")
            continue

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

        execute(action, target, argument)

        
if __name__ == "__main__":
    main()