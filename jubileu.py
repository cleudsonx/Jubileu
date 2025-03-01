import streamlit as st
import speech_recognition as sr
import pyttsx3
import cv2
from transformers import pipeline
import os

st.title("Assistente Pessoal Jubileu")

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
            return ""
        except sr.RequestError as e:
            st.write(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
            return ""

# Exemplo de uso do pipeline de geração de texto com gpt-neo
text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

def generate_text(prompt):
    generated = text_generator(prompt, max_length=50, num_return_sequences=1)
    return generated[0]['generated_text']

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Exemplo de uso do OpenCV para capturar uma imagem da webcam
def capture_image():
    st.write("Capturando imagem da webcam...")
    cap = cv2.VideoCapture(0)
    try:
        if not cap.isOpened():
            st.write("Erro ao abrir a câmera.")
            return
        ret, frame = cap.read()
        if not ret:
            st.write("Falha ao capturar imagem.")
            return
        cv2.imwrite("captured_image.jpg", frame)
        st.image("captured_image.jpg", caption="Imagem Capturada")
    except Exception as e:
        st.write(f"Ocorreu um erro: {e}")
    finally:
        cap.release()

# Interface do Streamlit
st.write("O assistente está ativo e aguardando sua interação por voz.")

# Botão para iniciar reconhecimento de voz
if st.button("Falar"):
    user_input = recognize_speech()
    if user_input:
        if "capturar imagem" in user_input.lower():
            capture_image()
        else:
            st.write("Gerando texto...")
            generated_text = generate_text(user_input)
            st.write(f"Texto gerado: {generated_text}")
            speak_text(generated_text)