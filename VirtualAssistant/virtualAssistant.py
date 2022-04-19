import speech_recognition as sr ## for mic input
import pyttsx3 ## for va to talk back
from googlesearch import search
import datetime
import wikipedia
import pyjokes
import webbrowser
import sys
import os

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[17].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def boot_up():
    time = datetime.datetime.now().strftime('%-H %p')
    time = time.split()

    if "AM" in time and (5 <= int(time[0]) <= 12):
        current = datetime.datetime.now().strftime('%I:%M %p')
        greeting = "Good morning, it is currently " + current + ",how may I help you?"
        talk(greeting)
    if "PM" in time and (12 < int(time[0]) <= 17):
        current = datetime.datetime.now().strftime('%I:%M %p')
        greeting = "Good afternoon, it is currently " + current + ",how may I help you?"
        talk(greeting)
    elif "PM" in time and (17 < int(time[0]) <= 21):
        current = datetime.datetime.now().strftime('%I:%M %p')
        greeting = "Good evening, it is currently " + current + ",how may I help you?"
        talk(greeting)


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source) ## using mic to take input
            command = listener.recognize_google(voice) ## speech to text
    except:
        pass

    return command

def run_alexa():
    command = take_command()
    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk("It's " + time)
    elif 'who is' in command:
        person = command.replace("who is", '')
        info = wikipedia.summary(person,3)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif "launch Spotify" in command:
        app = command.replace("launch","")
        path = "/Applications/" + app.strip() + ".app"
        talk("opening " + app)
        os.system("open " + path)
    elif "launch Google" in command:
        app = "\ Chrome"
        path = "/Applications/Google" + app + ".app"
        app = "Google Chrome"
        os.system("open " + path)
        talk("opening " + app)
    elif 'Google search' in command:
        talk("What would you like to search?")
        query = take_command()
        talk("searching for, " + query)
        for j in search(query,tld="com",num=1,stop=1,pause=2):
            webbrowser.open(j)
    elif 'goodbye' or 'i"m done' or 'nothing' in command:
        talk("goodbye")
        sys.exit()
    else:
        talk("I didn't quite catch that")

boot_up()
while True:
    run_alexa()