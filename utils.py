from context import context

import time

def wait(seconds=1):
    time.sleep(seconds)

def remember(action, target=None, argument = None):
    context["last_target"] = target
    context["last_action"] = action
    context["last_argument"] = argument

    context["history"].append({"action": action, "target":target, "argument":argument})

    if len (context["history"]) > 20:
        context["history"].pop(0)

    