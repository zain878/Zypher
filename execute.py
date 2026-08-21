from actions import *
from keyboard import *
from data import *
from context import context
from speech import speak
from parser import normalizeCalculator
from utils import wait,remember

def execute(action, target, argument):

    if action == "open":
                if not target:
                    speak("What would you like me to open?")
    
                elif target in applications:
                    openApplication(applications[target])
                    remember(action, target)
                    context["app"] = target
                    context["website"] = None
                    context["last_target"] = target
    
                elif target in websites:
                    if context["app"] != "google":
                        openApplication(applications["google"])
                        wait(2)
                        context["app"] = "google"
                        remember(action,target)
    
                    openWebsite(websites[target])
                    context["website"] = target
                    context["last_target"] = target
                    remember(action,target)
    
                elif target in folders:
                    openFolder(folders[target])
                    remember(action,target)
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
                        remember(action,target)
                        context["website"] = target
                        context["last_target"] = target
    
                        wait(2)
                    searchOnWebsite(argument)
                    remember(action,target,argument)
    
                elif target == "google":
                    if context["app"] != "google":
                        openApplication(applications["google"])
                        remember(action,target)
                        wait(2)
    
                        context["app"] = "google"
                        context["last_target"] = "google"
    
                    searchInBrowser(argument)
                    remember(action,target,argument)
    
                    # else:
                    #     speak("I can't search there yet.")
    
                elif target == "menu":
                    searchInMenu(argument)
                    remember(action,target,argument)
    
                else:
                    speak("I can't search that website yet.")
    
    elif action == "run":
                if not argument:
                    speak("What command would you like me to run?")
    
                else:
                    runCommandInTerminal(argument)
                    remember(action,target,argument)
    
    elif action == "repeat":
                if not context["history"]:
                    speak("There is nothing to repeat")
                    return

                last = context["history"][-1]

                execute(
                      last["action"], last["target"], last["argument"]
                )

    elif action == "back":
                keyCombo("alt" , "left")

    elif action == "shutdown":
                shutdown()
    elif action == "suspend":
                suspend()
    elif action == "reboot":
                reboot()
    
    elif action == "find":
                if not argument:
                    speak("What would you like me to find?")
    
                else:
                    openApplication(applications["google"])
                    remember(action,target)
                    wait(2)
                    searchInBrowser(argument)
                    remember(action,target,argument)
    
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
                remember(action,target,argument)
    
    elif action in ["copy", "paste", "cut", "undo", "redo", "save"]:
                shortcuts(action)
    
    elif action == "select":
                selectAll()
    
    elif action == "type":
                mode = app_modes.get(context["app"], "text")
    
                if mode == "math":
                    argument = normalizeCalculator(argument)
    
                writeText(argument)
                remember(action,target,argument)
    
    
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
    