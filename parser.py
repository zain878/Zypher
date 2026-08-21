from data import numbers, operators,actions,aliases

def parser(speech):
    action = None
    target = None
    argument = None

    for stop in ["please", "can", "could", "you", "would", "kindly", "for me"]:
        if stop in speech:
            speech.replace(stop, "")

    for ac in actions:
        if ac in speech:
            action = ac
            break

    if action is None:
        return None, None, None

    if "command" in speech:
        target = "terminal"
        parts = speech.split("command")
        argument = parts[1].strip()

    # elif "shutdown" in speech:
    #     action = "shutdown"

    # elif "suspend" in speech:
    #     action = "suspend"

    # elif "reboot" in speech:
    #     action = "reboot"

    elif action == "find":
        parts = speech.split("find")
        argument = parts[1].strip()

    elif action == "run":
        target = "terminal"
        parts = speech.split("run")
        argument = parts[1].strip()

    elif action == "repeat":
        pass

    elif action == "back":
        pass

    elif action == "search":
        if speech.startswith("search for"):
            target = None
            argument = speech.split("search for")[1].strip()
        else:
            target = speech.split(action)[1].split(" for")[0].strip()
            argument = speech.split("for")[1].strip()

        parts = speech.split("for")
        argument = parts[1].strip()

    elif action == "close":
        if "it" in speech:
            action = "close"
            target = "it"
            argument = None
        parts = speech.split(action)
        target = parts[1].strip()

    elif action == "click":
        parts = speech.split(action)
        argument = parts[1].strip()

    elif action in ["go back" , "back", "repeat"]:
        action = "back"

    elif action == "press":
        parts = speech.split(action)
        argument = parts[1].strip()

    elif action in ["copy", "paste", "undo", "redo", "cut"]:
        argument = action

    elif action == "select":
        target = "all"

    elif action == "type":
        parts = speech.split(action)
        argument = parts[1].strip()

    elif action == "volume":
        if "up" in speech:
            argument = "up"

        elif "down" in speech:
            argument = "down"

    elif action == "brightness":
        if "up" in speech:
            argument = "up"

        elif "down" in speech:
            argument = "down"

    elif action == "save":
        argument = action
    else:
        parts = speech.split(action)
        target = parts[1].strip()

    return action, target, argument


def normalizeSpeech(speech):

    speech = speech.lower().strip()

    for old, new in aliases.items():
        speech = speech.replace(old, new)

    return speech


def normalizeCalculator(speech):
    for word, symbol in operators.items():
        speech = speech.replace(word, symbol)
    for word, digit in numbers.items():
        speech = speech.replace(word, digit)
    return speech
