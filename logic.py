import speech_recognition as sr
import pyttsx3
from transformers import pipeline

# Configuração do reconhecimento de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def recognize_speech():
    with sr.Microphone() as source:
        print("Diga algo...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {text}")
            return text
        except sr.UnknownValueError:
            print("Não entendi o que você disse.")
            return ""
        except sr.RequestError as e:
            print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
            return ""

# Exemplo de uso do pipeline de geração de texto com T5 em português
text_generator = pipeline("text2text-generation", model="unicamp-dl/ptt5-base-portuguese-vocab")

def generate_text(prompt):
    generated = text_generator(prompt, max_length=50, num_return_sequences=1)
    return generated[0]['generated_text']

def speak_text(text):
    engine.say(text)
    engine.runAndWait()