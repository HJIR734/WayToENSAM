import streamlit as st
import spacy

# Charger le modèle de langue
nlp = spacy.load("en_core_web_sm")

# Titre de l'application
st.title("Chatbot avec Streamlit et spaCy")

# Champ de saisie pour l'utilisateur
user_input = st.text_input("Vous : ")

# Fonction de réponse du chatbot
def get_bot_response(user_input):
    doc = nlp(user_input)
    # Simple logique de réponse basée sur l'entrée de l'utilisateur
    if "hello" in user_input.lower():
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    elif "how are you" in user_input.lower():
        return "Je suis juste un programme, mais je vais bien, merci !"
    else:
        return "Désolé, je n'ai pas compris. Pouvez-vous reformuler ?"

# Afficher la réponse du chatbot
if user_input:
    bot_response = get_bot_response(user_input)
    st.text_area("Bot : ", value=bot_response, height=150)
