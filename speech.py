import speech_recognition as sr
import pyttsx3 as psx

r = sr.Recognizer()
engine = psx.init()

def listenAudio():

    with sr.Microphone() as source:
        print("Speak Now")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio)

        except sr.UnknownValueError:
            print("Could not hear anything")
            return None

        except sr.WaitTimeoutError:
            print("Did not spoke")
            return None

        except sr.RequestError as e:
            print("Speech recognition service error:", e)
            return None

    return text

def speak(sp):
    engine.say(sp)
    engine.runAndWait()