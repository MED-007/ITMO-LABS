import sys
import os
import json
import requests
import sounddevice as sd
import pyttsx3
import webbrowser
from vosk import Model, KaldiRecognizer

# CONFIGURATION
MODEL_PATH = "model" 
FILE_NAME = "dictionary.txt"

class Speaker:
    def __init__(self):
        try:
            # Force Windows SAPI5 driver for stability
            self.engine = pyttsx3.init(driverName='sapi5')
        except:
            # Fallback for Mac/Linux
            self.engine = pyttsx3.init()
            
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def say(self, text):
        print(f"[ASSISTANT] {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass # Ignore TTS errors if audio is busy

class DictionaryAPI:
    def __init__(self):
        self.current_word = None
        self.data = None

    def find_word(self, word):
        self.current_word = word
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.data = response.json()[0]
                return f"Found {word}."
            elif response.status_code == 404:
                self.data = None
                return f"Sorry, I couldn't find {word}."
            else:
                return "Dictionary API Error."
        except Exception:
            return "Connection failed."

    def get_meaning(self):
        if not self.data: return "Please find a word first."
        try:
            defin = self.data['meanings'][0]['definitions'][0]['definition']
            return defin
        except:
            return "No definition found."

    def get_example(self):
        if not self.data: return "Please find a word first."
        try:
            ex = self.data['meanings'][0]['definitions'][0].get('example')
            return ex if ex else "No example available."
        except:
            return "No example found."

    def open_link(self):
        if not self.data: return "Please find a word first."
        try:
            link = self.data.get('sourceUrls', [None])[0]
            if link:
                webbrowser.open(link)
                return "Opening browser."
            return "No link found."
        except:
            return "Could not open link."

    def save_entry(self):
        if not self.data: return "Please find a word first."
        meaning = self.get_meaning()
        entry = f"{self.current_word}: {meaning}\n"
        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(entry)
        return "Saved to file."

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Folder '{MODEL_PATH}' not found. Please download Vosk model.")
        sys.exit(1)

    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, 16000)
    
    # Open mic
    p = sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, dtype='int16', channels=1)
    p.start()

    speaker = Speaker()
    api = DictionaryAPI()
    
    print("=== Additional Task: Dictionary Assistant ===")
    print("Commands: 'find [word]', 'meaning', 'example', 'link', 'save', 'exit'")
    speaker.say("Dictionary ready.")

    while True:
        data = p.read(4000)[0]
        if len(data) == 0: break
            
        if rec.AcceptWaveform(bytes(data)):
            result = json.loads(rec.Result())
            text = result.get('text', '')
            
            if not text: continue
            print(f"[YOU]: {text}")
            
            # COMMANDS 
            if "find" in text:
                words = text.split()
                try:
                    idx = words.index("find")
                    # Check words after 'find'
                    if idx + 1 < len(words):
                        # Filter out 'the', 'a'
                        candidates = [w for w in words[idx+1:] if w not in ['the', 'a', 'an']]
                        if candidates:
                            target = candidates[0]
                            msg = api.find_word(target)
                            speaker.say(msg)
                        else:
                            speaker.say("Find what?")
                except:
                    pass

            elif "meaning" in text:
                speaker.say(api.get_meaning())

            elif "example" in text:
                speaker.say(api.get_example())

            elif "link" in text:
                msg = api.open_link()
                speaker.say(msg)

            elif "save" in text:
                msg = api.save_entry()
                speaker.say(msg)

            elif "exit" in text or "stop" in text:
                speaker.say("Goodbye.")
                break

if __name__ == "__main__":
    main()
