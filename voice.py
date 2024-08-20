import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from threading import Thread

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble with the speech service.")
            return ""

def process_command(command):
    if "hello" in command:
        response = "Hello! How can I assist you today?"
    
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        response = f"The current time is {current_time}"
    
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        response = f"Today's date is {current_date}"
    
    elif "search" in command:
        speak("What would you like to search for?")
        append_text("Assistant: What would you like to search for?")
        query = listen()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            response = f"Here are the search results for {query}."
    
    elif "exit" in command or "quit" in command:
        response = "Goodbye!"
        root.quit() 
    
    else:
        response = "I'm sorry, I don't know how to do that."

    speak(response)
    append_text(f"Assistant: {response}")

def append_text(text):
    text_box.configure(state='normal')
    text_box.insert(tk.END, text + "\n")
    text_box.configure(state='disabled')
    text_box.see(tk.END)

def start_listening():
    append_text("Listening...")
    command = listen()
    if command:
        append_text(f"You: {command}")
        process_command(command)

def start_voice_assistant():
    listen_thread = Thread(target=start_listening)
    listen_thread.daemon = True  
    listen_thread.start()

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x520")
root.configure(bg='#f0f0f0')

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)

frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(pady=20)

text_box = tk.Text(frame, wrap='word', height=20, width=50, state='disabled', font=('Helvetica', 10), bg='#e6e6e6', fg='#333')
text_box.pack(padx=10, pady=10)

listen_button = ttk.Button(root, text="Speak", command=start_voice_assistant)
listen_button.pack(pady=10)

exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

root.mainloop()
