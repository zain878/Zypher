import tkinter as tk
import threading

from assistant import listenAudio
from parser import parser
from fuzzy import correctTarget
from execute import execute
from data import *

# ---------------- GUI COLORS ----------------

BG_COLOR = "#111827"
CARD_COLOR = "#1F2937"
ACCENT_COLOR = "#6366F1"
ACCENT_HOVER = "#818CF8"
TEXT_COLOR = "#F9FAFB"
SECONDARY_TEXT = "#9CA3AF"
SUCCESS_COLOR = "#34D399"


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Zypher")
window_width = 500
window_height = 550

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")


root.resizable(False, False)
root.configure(bg=BG_COLOR,)


# ---------------- TITLE ----------------

title = tk.Label(
    root, text="ZYPHER", font=("Orbitron", 28, "bold"), fg=TEXT_COLOR, bg=BG_COLOR
)

title.pack(pady=(50, 5))


subtitle = tk.Label(
    root,
    text="Your voice-powered desktop assistant",
    font=("Share Tech Mono", 13),
    fg=SECONDARY_TEXT,
    bg=BG_COLOR,
)

subtitle.pack()


# ---------------- STATUS ----------------

status = tk.Label(root, text="Ready", font=("Share Tech Mono", 12), fg=SUCCESS_COLOR, bg=BG_COLOR)

status.pack(pady=(35, 20))


# ---------------- MICROPHONE BUTTON ----------------

mic_button = tk.Button(
    root,
    text="🎤",
    font=("Share Tech Mono", 40),
    width=4,
    height=2,
    bg=ACCENT_COLOR,
    fg="white",
    activebackground=ACCENT_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
)

mic_button.pack(pady=20)


# ---------------- COMMAND DISPLAY ----------------

command_label = tk.Label(
    root,
    text="Click the microphone and speak",
    font=("Share Tech Mono", 12),
    fg=SECONDARY_TEXT,
    bg=BG_COLOR,
    wraplength=400,
)

command_label.pack(pady=30)


# ---------------- LISTENING FUNCTION ----------------


def startListening():

    status.config(text="Listening...", fg=ACCENT_HOVER)

    command_label.config(text="I'm listening...")

    mic_button.config(state="disabled")

    # Run microphone in background
    threading.Thread(target=processCommand, daemon=True).start()


def processCommand():

    speech = listenAudio()

    if not speech:
        root.after(0, lambda: resetGUI("I didn't hear anything."))
        return

    root.after(0, lambda: command_label.config(text=f'You said: "{speech}"'))

    # Existing Zypher pipeline
    action, target, argument = parser(speech)

    # Your existing fuzzy correction
    target = correctTarget(action, target, applications, websites, folders)

    # Existing executor
    execute(action, target, argument)

    root.after(0, lambda: resetGUI("Ready"))


def resetGUI(message):

    status.config(text=message, fg=SUCCESS_COLOR)

    mic_button.config(state="normal")


# ---------------- BUTTON ACTION ----------------

mic_button.config(command=startListening)


# ---------------- START GUI ----------------

root.mainloop()
