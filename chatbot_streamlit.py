import openai
import streamlit as st

# Configurez votre clé API
openai.api_key = "org-xFvXuKAJeAlwaQRx18zSNe1n"

st.title("Chatbot avec Streamlit")
st.write("Posez-moi une question, et je vais essayer de répondre !")

# Interface utilisateur pour entrer la question
user_input = st.text_input("Votre question :")

# Si l'utilisateur entre une question
if user_input:
    try:
        # Utilisez ChatCompletion avec le modèle gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        # Affichez la réponse
        st.write(response['choices'][0]['message']['content'])
    
    except Exception as e:
        st.write("Une erreur s'est produite :", e)
