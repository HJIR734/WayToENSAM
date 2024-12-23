import streamlit as st
import json 
# Charger les données du fichier JSON complet
with open("way_to_ensam_chatbot_data_full.json", "r", encoding="utf-8") as file:
    chatbot_data = json.load(file)

# Titre de l'application
st.title("Way to ENSAM - Chatbot d'Orientation Académique")

# Menu latéral
st.sidebar.title("Options")
menu = st.sidebar.selectbox("Menu", ["Posez une Question", "À propos"])

# Section principale
if menu == "Posez une Question":
    st.header("Entrez votre question :")
    question = st.text_input("")

    if st.button("Envoyer"):
        if "filières" in question.lower():
            st.write("Voici les filières disponibles à l'ENSAM Meknès :")
            for filiere in chatbot_data["filières"].keys():
                st.write(f"- {filiere}")
        elif any(filiere.lower() in question.lower() for filiere in chatbot_data["filières"].keys()):
            for filiere in chatbot_data["filières"]:
                if filiere.lower() in question.lower():
                    st.write(f"Informations pour la filière {filiere} :")
                    if "objectifs" in question.lower():
                        st.write("**Objectifs :**")
                        for objectif in chatbot_data["filières"][filiere]["objectifs"]:
                            st.write(f"- {objectif}")
                    elif "modules" in question.lower():
                        st.write("**Modules par semestre :**")
                        for semestre, modules in chatbot_data["filières"][filiere]["modules_par_semestre"].items():
                            st.write(f"{semestre} :")
                            for module in modules:
                                st.write(f"- {module}")
                    elif "débouchés" in question.lower():
                        st.write("**Débouchés :**")
                        for debouche in chatbot_data["filières"][filiere]["débouchés"]:
                            st.write(f"- {debouche}")
                    break
        else:
            st.write("Je ne comprends pas votre question. Essayez d'être plus précis.")
elif menu == "À propos":
    st.header("À propos")
    st.write(chatbot_data["introduction"])

