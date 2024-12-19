import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit
import tkinter as tk
from tkinter import scrolledtext

# Initialize the speech engine
engine = pyttsx3.init()

# Function to make Alexa speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize user voice command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            r.pause_threshold = 1
            status_label.config(text="Listening...", fg="lime")
            root.update()
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            status_label.config(text=f"You said: {query}", fg="white")
            root.update()
            return query.lower()
        except Exception as e:
            status_label.config(text="Sorry, I didn't catch that. Can you repeat?", fg="orange")
            root.update()
            return None

# Greet the user
def greet_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How can I assist you today?")

# Process commands
def process_command():
    while True:
        query = take_command()
        if query:
            if 'wikipedia' in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                response_box.insert(tk.END, f"User: {query}\nAssistant: {results}\n\n")
                response_box.see(tk.END)
                speak(results)

            elif 'open youtube' in query:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")
                response_box.insert(tk.END, "Assistant: Opening YouTube\n\n")

            elif 'open google' in query:
                speak("Opening Google")
                webbrowser.open("https://google.com")
                response_box.insert(tk.END, "Assistant: Opening Google\n\n")

            elif 'time' in query:
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {str_time}")
                response_box.insert(tk.END, f"Assistant: The current time is {str_time}\n\n")

            elif 'play' in query:
                song = query.replace("play", "").strip()
                speak(f"Playing {song} on YouTube")
                pywhatkit.playonyt(song)
                response_box.insert(tk.END, f"Assistant: Playing {song} on YouTube\n\n")

            elif 'stop' in query or 'exit' in query:
                speak("Goodbye! Have a great day.")
                status_label.config(text="Assistant Stopped", fg="red")
                root.update()
                break

            else:
                speak("I can search that for you!")
                webbrowser.open(f"https://www.google.com/search?q={query}")
                response_box.insert(tk.END, f"Assistant: Searching for {query}\n\n")

# Start the assistant
def start_assistant():
    greet_user()
    process_command()

# GUI Setup
root = tk.Tk()
root.title("Alexa Clone - Dark Mode")
root.geometry("800x600")
root.configure(bg="#2b2b2b")

# GUI Elements
title_label = tk.Label(root, text="Alexa Clone", font=("Helvetica", 24, "bold"), bg="#2b2b2b", fg="white")
title_label.pack(pady=10)

status_label = tk.Label(root, text="Click Start to Begin", font=("Helvetica", 14), bg="#2b2b2b", fg="white")
status_label.pack(pady=5)

response_box = scrolledtext.ScrolledText(root, width=70, height=20, bg="#1e1e1e", fg="white", font=("Helvetica", 12))
response_box.pack(pady=10)

button_frame = tk.Frame(root, bg="#2b2b2b")
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start Assistant", command=start_assistant, font=("Helvetica", 14), bg="#3cb371", fg="white")
start_button.grid(row=0, column=0, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=root.quit, font=("Helvetica", 14), bg="#d9534f", fg="white")
exit_button.grid(row=0, column=1, padx=10)

root.mainloop()
