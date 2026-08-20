# Zypher

A modular offline voice assistant built with Python for Linux Mint XFCE.

Zypher can understand voice commands and perform common desktop automation tasks such as opening applications,
searching websites, controlling system settings, and interacting with the keyboard and mouse.

---

## Features

- 🎙️ Voice command recognition
- 💬 Text-to-speech responses
- 🖥️ Open desktop applications
- 🌐 Open and search websites
- 📂 Open common folders
- ⌨️ Keyboard shortcuts
- 🖱️ Mouse automation
- 🔊 Volume control
- 💡 Brightness control
- 🧮 Calculator-aware typing
- 🧠 Context memory for follow-up commands

---

## Project Structure


Zypher/
│
├── run.py
├── assistant.py
├── parser.py
├── actions.py
├── speech.py
├── keyboard.py
├── utils.py
├── data.py
├── context.py


---

## Technologies Used

- Python 3
- SpeechRecognition
- PyAutoGUI
- pyttsx3
- subprocess
- Linux Mint XFCE

---

## Current Status

This project is actively being developed.

Current version includes:

- Modular architecture
- Voice command parsing
- Desktop automation
- Context-aware commands

Planned features include:

- RapidFuzz command matching
- OpenCV screen recognition
- Plugin system
- Local AI integration
- Better natural language understanding

---

## Installation

Clone the repository:

  bash
git clone https://github.com/zain878/Zypher.git

Install the required packages:

  bash
pip install -r requirements.txt


Run the assistant:

  bash
python run.py

---

  ## Author

  ## Zain Ali

Software Engineering Student at University of Central Punjab

Built as a personal learning project to explore Python automation, Linux desktop scripting, and AI assistants.
