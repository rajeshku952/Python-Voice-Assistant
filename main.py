import speech_recognition as sr
import pyttsx3
import random
import string
import nltk
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from datetime import datetime
import os
import webbrowser
import wikipedia # type: ignore
import nltk
nltk.download('punkt')
nltk.download('stopwords')


recognizer = sr.Recognizer()
engine = pyttsx3.init()


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to preprocess user input
def preprocess_input(user_input):
    # Tokenize and remove punctuation
    user_input = user_input.lower()
    user_input = user_input.translate(str.maketrans("", "", string.punctuation))
    words = word_tokenize(user_input)
    
    # Remove stop words
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

# Function to handle custom commands (like opening applications, websites, etc.)
def handle_custom_commands(user_input):
    if 'time' in user_input:
        current_time = datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
        return True
    elif 'open browser' in user_input or 'google' in user_input:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
        return True
    elif 'youtube' in user_input:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return True
    elif 'wikipedia' in user_input:
        speak("Opening Wikipedia.")
        webbrowser.open("https://www.wikipedia.org")
        return True
    elif 'file' in user_input:
        speak("Opening your file explorer.")
        os.system("explorer")
        return True
    elif 'joke' in user_input:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you get when you cross a snowman and a vampire? Frostbite."
        ]
                  
    elif 'just open youtube' in query: # type: ignore
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            url = "https://www.youtube.com"
            if os.path.exists(chrome_path):  
                subprocess.Popen([chrome_path, url])
            else:
                speak("I couldn't find Google Chrome. Please check the installation.")
        
    elif 'open youtube' in user_input:
            speak("What should I search?")
            search_query = takeCommand()  
            if search_query:
                speak(f"Searching for {search_query} on YouTube...")
                wk.playonyt(search_query)
                speak("Enjoy the video, Boss!")  
                
                time.sleep(180)
                speak("It's been 3 minutes, Sir. Do you need anything else?")
                next_query = takeCommand()  
    else:
        return False
    
# Set the padding token to the EOS token (since DialoGPT doesn't have a separate pad token)
tokenizer.pad_token_id = tokenizer.eos_token_id

# Function to get a more advanced response using DialoGPT
def get_response(user_input):
    user_input = preprocess_input(user_input)
       
    # First, check for custom commands
    if handle_custom_commands(user_input):
        return None
    
    # Tokenize the input and create an attention mask
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # Generate the response with the attention mask
    attention_mask = inputs.ne(tokenizer.pad_token_id).long()  # Create the attention mask
    response_ids = model.generate(
        inputs, 
        max_length=1000, 
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=attention_mask  # Pass attention mask
    )
    
    response = tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    
    return response

# Function to listen for voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Could not request results from the speech recognition service.")
            return None

# Main chatbot loop
def chatbot():
    speak("Hello Boss! How can I assist you today?  Say 'exit' to stop.")
    
    while True:
        user_input = listen()
        if user_input:
            if 'exit' in user_input or 'quit' in user_input:
                speak("Good bye Boss!")
                break
            
            response = get_response(user_input)
            if response:
                speak(response)

if __name__ == "__main__":
    chatbot()
  
