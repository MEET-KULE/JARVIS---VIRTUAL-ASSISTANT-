import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()

NEWS_API_KEY = "0e6c3caef60a4b5c8ef93ff9c04b8066"

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def get_time():
    now = datetime.datetime.now()
    return now.strftime("IT'S %I:%M %p")

def get_news():
    speak("Fetching top news headlines...")
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data["articles"]
        speak("Here are the top 5 headlines:")
        for count, article in enumerate(articles[:5], 1):
            speak(f"Headline {count}: {article['title']}")
    except Exception as e:
        speak("Could not fetch the news.")
        print("Error:", e)

def processCommand(command):
    command = command.lower()
    if "stop" in command:
        speak("Goodbye!")
        exit()
    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
    elif "open calculator" in command:
        webbrowser.open("https://calculator.com")
        speak("Opening Calculator")
    elif "what time" in command:
        speak(get_time())
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")
        else:
            speak("Please tell me what to search for.")
    elif "news" in command:
        get_news()
    else:
        speak("Sorry, I didn't understand that.")

def listen_command(prompt_text="Listening...", timeout=5, phrase_time_limit=5):
    with sr.Microphone() as source:
        print(prompt_text)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.WaitTimeoutError:
            print("[DEBUG] Timeout - no speech detected.")
            return None
        except sr.UnknownValueError:
            print("[DEBUG] Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"[DEBUG] API error: {e}")
            return None

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    failure_count = 0
    max_failures = 3

    while failure_count < max_failures:
        wake_word = listen_command("Say 'Jarvis' to activate...", timeout=5)
        if wake_word and "jarvis" in wake_word.lower():
            speak("Yes?")
            command = listen_command("Listening for your command...", timeout=7, phrase_time_limit=7)
            if command:
                processCommand(command)
                failure_count = 0
            else:
                failure_count += 1
        elif wake_word and "stop" in wake_word.lower():
            speak("Goodbye!")
            break
        else:
            failure_count += 1

    if failure_count >= max_failures:
        speak("Too many failed attempts. Exiting.")
