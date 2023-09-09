import speech_recognition as sr
import openai
import pyttsx3
from secret import SECRET_KEY

#set openai key
openai.api_key = SECRET_KEY

#initialize the text-to-speech engine
engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
    try:      
            return recognizer.recognize_google(audio)
        
    except:
        print("Somenthing its wrong")
    
    

def generate_response(prompt):
    #Do request to OpenAI's API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response['choices'][0]['text']

#Say the anwser
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
def main():
    while True:
        print("Say 'Logan' to start to speek")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
        try:      
                transcription = recognizer.recognize_google(audio, language='en-US')
                if transcription.lower() == 'logan':
                    #record audio
                    filename = "input.wav"
                    print("Speak... ")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    #Trascribe audio to text
                    
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        
                        #Genarate response using GPT
                        response = generate_response(text)
                        print(f"GPT reply: {text}")
                        
                        #Read Response using Text_to_Speech
                        speak_text(response)             
            
        except Exception as e:
            print("Somenthing its wrong: {}".format(e))

if __name__ == "__main__":
    main()