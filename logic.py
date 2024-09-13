import speech_recognition as sr
import pyttsx3
from transformers import pipeline
import platform

# Configuração do reconhecimento de voz
recognizer = sr.Recognizer()

# Inicializar o pyttsx3 com o driver apropriado
try:
    if platform.system() == 'Windows':
        engine = pyttsx3.init(driverName='sapi5')
    elif platform.system() == 'Darwin':
        engine = pyttsx3.init(driverName='nsss')
    else:
        engine = pyttsx3.init()
except Exception as e:
    engine = None
    print(f"Erro ao inicializar o pyttsx3: {e}")

# Dicionário para armazenar conhecimentos
knowledge_base = {}

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
    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print("Engine de fala não está disponível.")

# Pipeline de classificação de texto
classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

def classify_text(text):
    classification = classifier(text)
    return classification

def handle_special_questions(text):
    if "qual o seu nome" in text.lower():
        return "Jubileu, você não sabe, nem eu!"
    return None

def learn_knowledge(question, answer):
    knowledge_base[question.lower()] = answer

def get_knowledge(question):
    return knowledge_base.get(question.lower(), None)