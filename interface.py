import streamlit as st
from logic import recognize_speech, generate_text, speak_text, classify_text, handle_special_questions

def main():
    try:
        while True:
            user_input = recognize_speech()
            if user_input:
                special_response = handle_special_questions(user_input)
                if special_response:
                    st.write(special_response)
                    speak_text(special_response)
                else:
                    st.write("Gerando texto...")
                    generated_text = generate_text(user_input)
                    st.write(f"Texto gerado: {generated_text}")
                    speak_text(generated_text)

                    st.write("Classificando texto...")
                    classification = classify_text(generated_text)
                    st.write(f"Classificação: {classification}")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Interface do Streamlit
def interface():
    st.title("Assistente Pessoal Jubileu")
    st.write("O assistente está ativo e aguardando sua interação por voz.")

    # Botão para iniciar reconhecimento de voz
    if st.button("Falar"):
        main()

if __name__ == "__main__":
    interface()