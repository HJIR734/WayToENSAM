import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# 1. Chargement du modèle avec st.cache pour l'optimiser
@st.cache(allow_output_mutation=True)
def load_model_once():
    return load_model('cnn_model_5_classes.h5')

model = load_model_once()

# 2. Définir les classes
classes = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

# 3. Prétraitement de l'image
def preprocess_image(image):
    image = image.resize((150, 150))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

# 4. CSS intégré pour personnaliser le style de la page
st.markdown("""
    <style>
    /* Fond noir pour toute la page */
    body {
        background-color: #0d1117;
        color: white;
    }

    /* Style du titre principal */
    h1 {
        font-family: 'Arial', sans-serif;
        color: #ffffff;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
    }

    /* Style pour les sous-titres */
    h2 {
        font-family: 'Arial', sans-serif;
        color: #00ff00; /* Vert pour les résultats */
        text-align: center;
    }

    /* Centrer les éléments Streamlit */
    .stFileUploader, .stButton, .stImage {
        margin-left: auto;
        margin-right: auto;
    }

    /* Style des boutons */
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-size: 20px;
        border-radius: 12px;
        padding: 10px 20px;
        cursor: pointer;
        border: none;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #ff7979;
    }
    </style>
""", unsafe_allow_html=True)

# 5. Interface de l'application Streamlit
st.markdown("<h1>🌸 Modèle de Classification des Fleurs 🌸</h1>", unsafe_allow_html=True)

# Téléchargement de fichier
uploaded_file = st.file_uploader("Choisissez une image à classer", type=["jpg", "png", "jpeg"])

# Si l'utilisateur a téléchargé une image
if uploaded_file is not None:
    # Afficher l'image téléchargée
    image = Image.open(uploaded_file)
    st.image(image, caption='Image chargée avec succès.', use_column_width=True)

    # Bouton de prédiction
    if st.button('Prédire'):
        with st.spinner('Prédiction en cours...'):
            # Prétraitement de l'image
            processed_image = preprocess_image(image)
            
            # Faire la prédiction
            prediction = model.predict(processed_image)
            predicted_class_index = np.argmax(prediction, axis=1)[0]  # Obtenir l'index de la classe prédite

            # Nom de la classe prédite
            predicted_class_name = classes[predicted_class_index]
            
            # Afficher le résultat de la prédiction
            st.markdown(f"<h2>Classe prédite : {predicted_class_name}</h2>", unsafe_allow_html=True)

            # Afficher les probabilités pour chaque classe
            probabilities = {classes[i]: float(prediction[0][i]) for i in range(len(classes))}
            st.write("Probabilités pour chaque classe :")
            st.write(probabilities)

 