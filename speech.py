import speech_recognition as sr
import pyttsx3 as psx
from ctypes import *
import contextlib

# Suppress non-fatal ALSA/JACK warnings emitted by PortAudio
# during Microphone initialization on Linux.
# This keeps the terminal clean while preserving portability
# across different microphone devices.
import os
import sys
import contextlib

@contextlib.contextmanager
def suppress_stderr():
    stderr_fd = sys.stderr.fileno()

    # Save original stderr
    saved_stderr = os.dup(stderr_fd)

    with open(os.devnull, "w") as devnull:
        # Redirect stderr to /dev/null
        os.dup2(devnull.fileno(), stderr_fd)

        try:
            yield
        finally:
            # Restore stderr
            os.dup2(saved_stderr, stderr_fd)
            os.close(saved_stderr)

r = sr.Recognizer()
engine = psx.init()

def listenAudio():

    with suppress_stderr():
        with sr.Microphone() as source:

            print("🎤 Listening...")

            r.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

                text = r.recognize_google(audio)

                return text.strip()

            except sr.WaitTimeoutError:
                print("⌛ No speech detected.")
                return None

            except sr.UnknownValueError:
                print("❓ Couldn't understand.")
                return None

            except sr.RequestError:
                print("🌐 Speech service unavailable.")
                return None
            
def speak(sp):
    engine.say(sp)
    engine.runAndWait()