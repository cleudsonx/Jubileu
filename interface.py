import streamlit as st
from speech import recognize_speech
from logic import generate_text, speak_text, classify_text, handle_special_questions, learn_knowledge, get_knowledge

def main():
    try:
        user_input = recognize_speech()
        if user_input:
            special_response = handle_special_questions(user_input)
            if special_response:
                st.write(special_response)
                speak_text(special_response)
            else:
                # Verificar se o assistente já conhece a resposta
                known_answer = get_knowledge(user_input)
                if known_answer:
                    st.write(f"Resposta conhecida: {known_answer}")
                    speak_text(known_answer)
                else:
                    st.write("Gerando texto...")
                    generated_text = generate_text(user_input)
                    st.write(f"Texto gerado: {generated_text}")
                    speak_text(generated_text)

                    st.write("Classificando texto...")
                    classification = classify_text(generated_text)
                    st.write(f"Classificação: {classification}")

                    # Perguntar ao usuário se a resposta gerada está correta
                    if st.button("A resposta está correta?"):
                        learn_knowledge(user_input, generated_text)
                        st.write("Conhecimento armazenado.")
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