import requests
import json
import speech_recognition as sr
import pyttsx3 

# Default prompt used on first run to set context.
PROMPT = 'You are a helpful assistant.'
#Empty array to be appended with the LLM's response (Casted into RESPONSE)
RESPONSE_ARRAY = [] 
# Empty string to store the response
RESPONSE = '' 
# Define the library to use here
LIBRARY = "llama3" 
# Define the endpoint URL hosting Ollama
URL = 'http://127.0.0.1:11434/api/generate'
 
# Initialize the voice recognizer 
r = sr.Recognizer() 
 
# Text-to-Speech
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    # Say the words :)
    engine.say(command) 
    engine.runAndWait()
   

count = 0 # Counter to identify first run in loop 
     
# Loop infinitely 
SpeakText("Hello, how may I assist you today?")
while(1):    
     
    try:
       
         
        # use the default microphone as source for input.
        with sr.Microphone() as source2:
             
            # Adjust for background noise 
            r.adjust_for_ambient_noise(source2, duration=0.2)
             
            # Listen for the user's input 
            audio2 = r.listen(source2)
             
            # Uses google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
        
            if count == 0:
                # Appends spoken text to default prompt defined above 
                pass 
            else:
                # Assumes you are continuing conversation from previous response
                PROMPT = ''
          
            # Initialize JSON object
            myobj = {
            "model": LIBRARY,
            "prompt": PROMPT + MyText
            }
          
            # Perform post request
            x = requests.post(URL, json = myobj)
            
            # Response is sent one word at a time. The following lines extract the response and add them to a list for printing.
            # If you are looking for speed statistics/metrics, this can be modified.
            answer = x.text.split("\n")

            # Iterate through each element and append the one-word response to RESPONSE_ARRAY for processing
            for i in answer:
                if json.loads(i)['response']:
                    RESPONSE_ARRAY.append(json.loads(i)['response'])
                else:
                    break

            # Convert RESPONSE_ARRAY to string
            RESPONSE.join(RESPONSE_ARRAY)

            # Print the response
            print(RESPONSE)

            # Open and append or create log file
            f = open("log.txt", "a+")
            f.write('Prompt: \n' + PROMPT + '\n Response: \n' + RESPONSE + '\n')
            f.close()

            # Use text-to-speech to speak the response

            SpeakText(RESPONSE)
            # Clear response variables
            RESPONSE_ARRAY.clear()
            RESPONSE = ''

            # Bypass original prompt
            count += 1

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("unknown error occurred (Timed out waiting for input.)")
