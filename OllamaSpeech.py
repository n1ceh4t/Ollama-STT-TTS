import requests
import json
import speech_recognition as sr
import pyttsx3 
import misc
from random import randrange
import subprocess
# Define the library to use here
LIBRARY = "wizardlm2:7b" 

# Go-word.
GOWORD = 'okay'
# Stop phrase
STOPPHRASE = 'thank you'

# Initialize voice recognition
r = sr.Recognizer() 
r.energy_threshold = 400
# Text-to-Speech

def runCommands(cmd, text):
    if (cmd == "exit"):
        exit(0)
    elif (cmd == "play"):
        title = text.replace("play","")
        SpeakText("Playing " + title)
        proc = subprocess.Popen("yt /" + title + ",d,1", shell=True)
    elif (cmd == "stop"):
        proc.kill()

def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    # Say the words :)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command) 
    engine.runAndWait()
   
def listening():
    while(1):
        try:
            with sr.Microphone() as source2:
                
                # Adjust for background noise 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                    
                # Listen for the user's input 
                audio2 = r.listen(source2)
                    
                # Uses google to recognize audio
                MyText = r.recognize_vosk(audio2)
                MyText = json.loads(MyText.lower())["text"]
                print(MyText)

                for i in misc.commands:
                    if (i in MyText):
                        runCommands(i, MyText)
                        MyText = ""
                    else:
                        continue

                if (STOPPHRASE in MyText):
                    SpeakText(misc.part[randrange(0,len(misc.part)-1)])
                    break
                elif (MyText == ""):
                    break
                
                # Unsure if this is needed. Init a dict
                HISTORY = {}
                # Load chat history from file
                with open('history.json') as f:
                    HISTORY = json.load(f)
                # print("History: " + str(HISTORY["history"]))
                # print("MyText: " + MyText)
                # print("Appending MyText to history...")
                new_entry = {"role": "user", "content": MyText}
                HISTORY["history"].append(new_entry)
                # Endpoint for OLLAMA
                url = 'http://127.0.0.1:11434/api/chat'

                # Initialize JSON object
                myobj = {
                "model": LIBRARY,
                "messages": HISTORY["history"],
                "stream": False,
                }
                # print(str(myobj))

                # Perform post request
                x = requests.post(url, json = myobj)
                # Print the response
                #print(x.text)
                RESPONSE = json.loads(x.text)["message"]
                new_entry = RESPONSE
                print(RESPONSE)
                HISTORY["history"].append(new_entry)

                # Open and append or create log file
                f = open("log.txt", "a+")
                f.write('Prompt: \n' + MyText + '\n Response: \n' + x.text + '\n')
                f.close()

                with open('history.json', 'w', encoding='utf-8') as f:
                    json.dump(HISTORY, f, ensure_ascii=False, indent=4)

                # Use text-to-speech to speak the response

                SpeakText(RESPONSE["content"])
                # Clear response variables

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred (Timed out waiting for input.)")

def main():
    # Loop infinitely 
    # SpeakText("Hello, how may I assist you today?")
    while(1):    
        try:
            # use the default microphone as source for input.
            with sr.Microphone() as source2:
                
                # Adjust for background noise 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                # Listen for the user's input 
                audio2 = r.listen(source2)
                
                # Uses google to recognize audio
                MyText = r.recognize_vosk(audio2)
                MyText = json.loads(MyText.lower())["text"]
                print(MyText)

                if (MyText == GOWORD):
                    SpeakText(misc.ack[randrange(0,len(misc.ack)-1)])
                    listening()

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred (Timed out waiting for input.)")

main()