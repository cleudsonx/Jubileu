import streamlit as st
import speech_recognition as sr
import pyttsx3
import cv2
from transformers import pipeline
import os

st.title("Assistente Pessoal para Windows 11")

# Configuração do reconhecimento de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def recognize_speech():
    with sr.Microphone() as source:
        st.write("Diga algo...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
            st.write(f"Você disse: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Não entendi o que você disse.")
        except sr.RequestError as e:
            st.write(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")

if st.button("Falar"):
    recognize_speech()

# Carregar modelo de RAG
rag_pipeline = pipeline("rag-token", model="facebook/rag-token-base")

def get_response(query):
    response = rag_pipeline(query)
    return response[0]['generated_text']

if st.button("Perguntar"):
    query = recognize_speech()
    if query:
        response = get_response(query)
        st.write(response)

# Listar arquivos de um diretório
def list_files(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

directory = st.text_input("Digite o diretório para listar arquivos:")
if directory:
    files = list_files(directory)
    st.write(files)

# Capturar vídeo da câmera
def capture_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if st.button("Iniciar Câmera"):
    capture_video()

