from execute import execute
from speech import listenAudio, speak
from fuzzy import correctTarget
from data import applications, websites, folders
from parser import parser, normalizeSpeech
from context import context


def process_speech(speech):
    """Process one recognized command and preserve Zypher context."""

    if not speech:
        return {"status": "I didn't hear anything.", "speech": None}

    speech = normalizeSpeech(speech)

    if any(word in speech for word in ["stop", "goodbye", "bye"]):
        speak("Signing off. Goodbye, Zain.")
        return {"status": "Signing off.", "speech": speech, "stop": True}

    if any(
        word in speech
        for word in ["hello", "hi", "hey", "hello zypher", "hello zipher"]
    ):
        reply = "Hello, Zain. This is Zypher. How can I assist you today?"
        speak(reply)
        return {"status": reply, "speech": speech}

    action, target, argument = parser(speech)
    target = correctTarget(action, target, applications, websites, folders)

    if action is None:
        speak("Sorry, I didn't understand.")
        return {"status": "Sorry, I didn't understand.", "speech": speech}

    # This is the same shared context used by every later button click.
    if target == "it":
        target = context["last_target"]

        if target is None:
            reply = "I don't know what 'it' refers to."
            speak(reply)
            return {"status": reply, "speech": speech}

    execute(action, target, argument)
    return {"status": "Ready", "speech": speech}


def run_one_command():
    """Listen once, then process exactly one Zypher command."""
    return process_speech(listenAudio())


def main():
    """Keep the original terminal-based continuous mode working."""
    while True:
        result = run_one_command()

        if result.get("stop"):
            break


if __name__ == "__main__":
    main()
