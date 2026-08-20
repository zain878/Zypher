from keyboard import (
    keyPress,
    keyCombo,
    writeText
)

from speech import speak
from utils import wait

import os
import subprocess
HOME = os.path.expanduser("~")

def openApplication(appName):
    keyPress("win")
    wait(2)

    writeText(appName)

    keyPress("enter")
    wait(2)

    speak(f"{appName} opened")


def closeApplication():
    keyCombo("alt", "f4")

def closeTab():
    keyCombo("ctrl", "w")

def openWebsite(url):
    keyCombo("ctrl", "t")
    keyCombo("ctrl", "l")
    writeText(url)
    keyPress("enter")

    wait(10)
    speak("Website Opened")


def searchOnWebsite(query):
    keyPress("/")
    writeText(query)
    keyPress("enter")

    wait(3)
    speak("Your Search Results ")

def searchInBrowser(query):
    keyCombo("ctrl", "t")
    keyCombo("ctrl", "l")
    writeText(query)
    keyPress("enter")


def openTerminal():
    keyCombo("ctrl", "alt", "t")
    wait(2)
    speak("Opened Terminal")


def runCommandInTerminal(command):
    openTerminal()
    wait(2)
    writeText(command)
    keyPress("enter")

def searchInMenu(query):
    keyPress("win")
    wait(2)
    writeText(query)

def openFolder(folder):
    subprocess.Popen(["thunar", os.path.join(HOME, folder)])

def volumeUp():
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%+"])


def volumeDown():
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%-"])


def brightnessUp():
    subprocess.run(["brightnessctl", "set", "+10%"])


def brightnessDown():
    subprocess.run(["brightnessctl", "set", "10%-"])