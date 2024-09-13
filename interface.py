import streamlit as st
from logic import recognize_speech, generate_text, speak_text

def main():
    user_input = recognize_speech()
    if user_input:
        st.write("Gerando texto...")
        generated_text = generate_text(user_input)
        st.write(f"Texto gerado: {generated_text}")
        speak_text(generated_text)

# Interface do Streamlit
def interface():
    st.title("Assistente Pessoal Jubileu")
    st.write("O assistente está ativo e aguardando sua interação por voz.")

    # Botão para iniciar reconhecimento de voz
    if st.button("Falar"):
        main()

if __name__ == "__main__":
    interface()