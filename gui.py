import tkinter as tk
import threading

from assistant import run_one_command

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
root.configure(
    bg=BG_COLOR,
)


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

status = tk.Label(
    root, text="Ready", font=("Share Tech Mono", 12), fg=SUCCESS_COLOR, bg=BG_COLOR
)

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


# ---------------- CONTINUOUS LISTENING ----------------

listening_event = threading.Event()
listener_thread = None


def update_listening_ui(is_listening, message=None):
    if is_listening:
        status.config(
            text=message or "Listening continuously...",
            fg=ACCENT_HOVER,
        )
        command_label.config(
            text="Speak a command, or press the button again to pause."
        )
        mic_button.config(text="■", bg="#EF4444")
    else:
        status.config(text=message or "Paused", fg=SUCCESS_COLOR)
        mic_button.config(text="🎤", bg=ACCENT_COLOR)


def continuous_listening_loop():
    while listening_event.is_set():
        try:
            result = run_one_command()
        except Exception as error:
            listening_event.clear()
            root.after(
                0,
                lambda error=error: update_listening_ui(
                    False,
                    f"Error: {error}",
                ),
            )
            return

        speech = result.get("speech")
        message = result.get("status", "Listening continuously...")

        if speech:
            root.after(
                0,
                lambda speech=speech: command_label.config(
                    text=f'You said: "{speech}"'
                ),
            )

        # "stop", "bye", and "goodbye" also stop continuous mode.
        if result.get("stop"):
            listening_event.clear()
            root.after(
                0,
                lambda message=message: update_listening_ui(False, message),
            )
            return

        if listening_event.is_set():
            root.after(
                0,
                lambda: status.config(
                    text="Listening continuously...",
                    fg=ACCENT_HOVER,
                ),
            )


def toggle_listening():
    global listener_thread

    # Second click: request that the loop pauses.
    if listening_event.is_set():
        listening_event.clear()
        update_listening_ui(False, "Pausing after this command...")
        return

    # First click: start the persistent command loop.
    listening_event.set()
    update_listening_ui(True)

    if listener_thread is None or not listener_thread.is_alive():
        listener_thread = threading.Thread(
            target=continuous_listening_loop,
            daemon=True,
        )
        listener_thread.start()


# ---------------- BUTTON ACTION ----------------

mic_button.config(command=toggle_listening)


# ---------------- START GUI ----------------

root.mainloop()
