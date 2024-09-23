from urllib.request import urlopen
from googletrans import Translator
from random import choice
import speech_recognition as sr
import pyttsx3 as ttx
import subprocess
import wolframalpha
import webbrowser
import wikipedia
import datetime
import pywhatkit

listner = sr.Recognizer()
engine = ttx.init()
voice = engine.getProperty("voices")
engine.setProperty("voice", 'french')


def Parler(text):
    engine.say(text)
    engine.runAndWait()


def Ecoute():
    command = ""  # Initialisation de la variable command
    try:
        with sr.Microphone() as source:
            print("Parler........")
            voix = listner.listen(source)
            command = listner.recognize_google(voix, language="fr-FR")
    except:
        pass
    return command


def assistantVocale():
    command = Ecoute()
    print(command)
    if 'salut' in command:
        Parler("Salut comment ça va ?")
    elif 'Bonjour' in command:
        Parler("Bonjour comment vous allez ?")
    elif "oui ça va et toi" in command:
        Parler("Je vais bien merci, comment je peux vous aider ?")


while True:
    assistantVocale()
