import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv
#from openai import ChatCompletion
import openai

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

r = sr.Recognizer()

def record_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def send_to_ChatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = [{"role": "user", "content": "Please act like Jarvis from Iron man."}]
while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_ChatGPT(messages)
    SpeakText(response)
    print(response)
