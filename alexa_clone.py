import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit  # For playing YouTube videos

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
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query.lower()
        except Exception as e:
            print("Sorry, I didn't catch that. Can you repeat?")
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

# Main function for voice commands
def main():
    greet_user()
    while True:
        query = take_command()
        
        if query:
            # Respond to commands
            if 'wikipedia' in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                print(results)
                speak(results)
            
            elif 'open youtube' in query:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")
            
            elif 'open google' in query:
                speak("Opening Google")
                webbrowser.open("https://google.com")
            
            elif 'time' in query:
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {str_time}")
            
            elif 'play' in query:  # Play the song on YouTube
                song = query.replace("play", "").strip()
                speak(f"Playing {song} on YouTube")
                pywhatkit.playonyt(song)
            
            elif 'stop' in query or 'exit' in query:
                speak("Goodbye! Have a great day.")
                break
            
            else:
                speak("I can search that for you!")
                webbrowser.open(f"https://www.google.com/search?q={query}")

if __name__ == "__main__":
    main()

