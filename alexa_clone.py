import os

# Set a dummy DISPLAY environment variable to avoid the KeyError in a headless environment
os.environ['DISPLAY'] = ':0'

import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import datetime
import wikipedia
import webbrowser
import pywhatkit

# Initialize the speech engine
engine = pyttsx3.init()

# Set properties for the voice engine (optional, customize as needed)
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)

# Function to speak text in a separate thread
def speak(text):
    def speak_thread():
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=speak_thread)
    thread.start()

# Function to recognize user voice command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            st.write("Listening...")
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            st.write(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            st.warning("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            st.error("Could not request results; check your internet connection.")
            return None

# Greet the user
def greet_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
        st.write("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
        st.write("Good Afternoon!")
    else:
        speak("Good Evening!")
        st.write("Good Evening!")
    speak("How can I assist you today?")

# Process commands
def process_command(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            st.write(f"User: {query}")
            st.write(f"Assistant: {results}")
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            st.error("Too many results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            st.error(f"No page found for {query}.")
    
    elif 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        st.write("Assistant: Opening YouTube")
    
    elif 'open google' in query:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        st.write("Assistant: Opening Google")
    
    elif 'time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")
        st.write(f"Assistant: The current time is {str_time}")
    
    elif 'play' in query:
        song = query.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
        st.write(f"Assistant: Playing {song} on YouTube")
    
    elif 'stop' in query or 'exit' in query:
        speak("Goodbye! Have a great day.")
        st.write("Assistant Stopped")
        return False
    
    else:
        speak("I can search that for you!")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        st.write(f"Assistant: Searching for {query}")
    return True

# Streamlit App
st.title("Alexa Clone")
st.write("A simple virtual assistant powered by Streamlit")

if st.button("Start Assistant"):
    greet_user()
    while True:
        query = take_command()
        if query:
            if not process_command(query):
                break

st.warning("Click 'Start Assistant' to begin.")
