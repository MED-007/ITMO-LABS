import sys
import os
import json
import queue
import time
import requests
import sounddevice as sd
import pyttsx3
from vosk import Model, KaldiRecognizer

# CONFIGURATION

MODEL_PATH = "model" #English model
FILE_NAME = "facts.txt"

# 1. TTS (Text-to-Speech)
class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150) # Slower speed for clarity

    def say(self, text):
        print(f"[ASSISTANT] {text}")
        self.engine.say(text)
        self.engine.runAndWait()

# 2. API Interaction (Variant 10)
class MathFactAPI:
    def __init__(self):
        self.current_fact = None

    def get_fact(self):
        try:
            # Get a random math fact
            response = requests.get("https://numbersapi.com/random/math")
            if response.status_code == 200:
                self.current_fact = response.text
                return self.current_fact
            else:
                return "Error connecting to API."
        except Exception as e:
            return f"Network error: {e}"

    def save_fact(self):
        if not self.current_fact:
            return "No fact to save. Ask for a fact first."
        
        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(self.current_fact + "\n")
        return "Fact saved to file."

    def delete_last(self):
        if not os.path.exists(FILE_NAME):
            return "File is empty."
        
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if not lines:
            return "File is already empty."
        
        # Remove last line
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.writelines(lines[:-1])
        
        return "Last fact deleted."

# 3. Voice Recognition
def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{MODEL_PATH}' folder.")
        sys.exit(1)

    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, 16000)
    
    p = sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, dtype='int16', channels=1)
    p.start()

    speaker = Speaker()
    api = MathFactAPI()
    
    print("=== Voice Assistant (Variant 10: Math Facts) ===")
    print("Commands: 'fact', 'next', 'read', 'append' (save), 'delete', 'exit'")
    
    speaker.say("I am ready. Ask me for a math fact.")

    while True:
        data = p.read(4000)[0]
        if len(data) == 0:
            break
            
        if rec.AcceptWaveform(bytes(data)):
            result = json.loads(rec.Result())
            text = result.get('text', '')
            
            if not text:
                continue
                
            print(f"[YOU]: {text}")
            
            # COMMAND HANDLING 
            if "fact" in text or "next" in text:
                fact = api.get_fact()
                speaker.say(fact)
                
            elif "read" in text:
                if api.current_fact:
                    speaker.say(f"Repeating: {api.current_fact}")
                else:
                    speaker.say("I haven't fetched a fact yet.")

            elif "append" in text or "save" in text:
                msg = api.save_fact()
                speaker.say(msg)

            elif "delete" in text:
                msg = api.delete_last()
                speaker.say(msg)

            elif "exit" in text or "stop" in text:
                speaker.say("Goodbye.")
                break

if __name__ == "__main__":
    main()
