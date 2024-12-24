Chatbot d'Orientation ENSAM - Langchain & Ollama
================================================

Ce projet montre comment utiliser Langchain avec les modèles linguistiques d'Ollama pour créer un chatbot d'orientation académique pour l'ENSAM de Meknès. Le chatbot utilise un système de question-réponse basé sur la récupération d'information (RetrievalQA). Le code inclut des étapes pour l'extraction de texte depuis des documents PDF, le stockage de ces documents dans une base de données vectorielle, et la récupération des informations pertinentes pour répondre aux requêtes des utilisateurs.

Explication du Code
----------------------
Les sections suivantes détaillent le code en expliquant chaque composant, son but et son utilisation.

### 1. *Importation des Bibliothèques* :

   .. code-block:: python

       import os
       import pdfplumber
       from langchain_community.vectorstores import Chroma
       from langchain_community.embeddings.ollama import OllamaEmbeddings
       from langchain.text_splitter import CharacterTextSplitter
       from langchain.schema import Document
       import streamlit as st

   - os : Permet d'interagir avec le système d'exploitation.
   - pdfplumber : Utilisé pour extraire le texte à partir de fichiers PDF.
   - Chroma : Base de données vectorielle pour stocker et interroger les embeddings.
   - OllamaEmbeddings : Génére des représentations vectorielles du texte.
   - CharacterTextSplitter : Permet de découper le texte en morceaux plus petits pour le traitement.
   - Document : Utilisé pour encapsuler le contenu des documents.

### 2. *Chargement et Lecture des Documents PDF* :

   .. code-block:: python

       def read_pdf(file_path):
           """Extraire le texte d'un fichier PDF."""
           with pdfplumber.open(file_path) as pdf:
               text = ""
               for page in pdf.pages:
                   text += page.extract_text()
           return text

   - La fonction `read_pdf` lit un fichier PDF et extrait son texte page par page.

### 3. *Chargement des Documents PDF depuis un Répertoire* :

   .. code-block:: python

       def load_documents_from_directory(directory_path):
           """Charger les documents PDF depuis un répertoire donné."""
           files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith(".pdf")]
           documents = [Document(page_content=read_pdf(file)) for file in files]
           return documents

   - La fonction `load_documents_from_directory` charge tous les fichiers PDF d'un répertoire et extrait leur texte pour les convertir en objets `Document`.

### 4. *Ingestion des Documents dans une Base de Données Vectorielle* :

   .. code-block:: python

       def ingest_into_vector_store(combined_texts):
           """Ingest les textes traités dans la base de données Chroma."""
           text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=200, chunk_overlap=200, separator=".")
           doc_splits = text_splitter.split_documents([Document(page_content=text) for text in combined_texts])
           db = Chroma(persist_directory="./TP_db", embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"), collection_name="rag-chroma")
           db.add_documents(doc_splits)
           db.persist()
           print("Données ingérées dans la base de données.")

   - Cette fonction découpe les documents en morceaux plus petits et les stocke dans une base de données Chroma après les avoir transformés en vecteurs à l'aide d'OllamaEmbeddings.

### 5. *Initialisation de la Base de Données Vectorielle pour la Récupération* :

   .. code-block:: python

       def initialize_vector_store():
           """Initialiser la base de données vectorielle Chroma pour la récupération."""
           db = Chroma(persist_directory="./TP_db", embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"), collection_name="rag-chroma")
           return db

   - La fonction `initialize_vector_store` initialise la base de données Chroma pour effectuer des recherches de similarité basées sur les vecteurs.

### 6. *Interface Streamlit pour le Chatbot* :

   .. code-block:: python

       st.title("Chatbot d'Orientation ENSAM")
       st.write("Ce chatbot peut répondre aux questions sur l'ENSAM de Meknès.")
       file = st.file_uploader("Téléchargez un fichier PDF", type=["pdf"])
       if file:
           doc = read_pdf(file)
           question = st.text_input("Posez une question")
           if st.button("Poser la question"):
               answer = retriever(doc, question)
               st.write(answer)
       else:
           question = st.text_input("Posez une question")
           if st.button("Poser la question"):
               answer = retrieve_from_db(question)
               st.write(answer)

   - L'interface utilisateur est créée avec Streamlit. Elle permet aux utilisateurs de télécharger un fichier PDF et de poser des questions sur son contenu.

### 7. *Récupération d'Information et Réponse à la Question* :

   .. code-block:: python

       def retrieve_from_db(question):
           """Récupérer la réponse à la question depuis la base de données vectorielle."""
           model = ChatOllama(model="mistral")
           db = initialize_vector_store()
           retriever = db.similarity_search(question, k=2)
           after_rag_template = """Répondez à la question en vous basant uniquement sur le contexte suivant :
           {context}
           Question : {question}
           Si aucune réponse n'est possible, répondez "Désolé, le contexte est insuffisant pour répondre à la question.""""
           after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
           after_rag_chain = (
               {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
               | after_rag_prompt
               | model
               | StrOutputParser()
           )
           return after_rag_chain.invoke({"context": retriever, "question": question})

   - La fonction `retrieve_from_db` interroge la base de données vectorielle et utilise le modèle Ollama pour générer une réponse à partir des données récupérées.

### 8. *Réponse Dynamique Basée sur le Contexte* :

   .. code-block:: python

       def retriever(doc, question):
           """Récupérer la réponse en fonction du document et de la question."""
           model_local = ChatOllama(model="mistral")
           doc = Document(page_content=doc)
           doc = [doc]
           text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=800, chunk_overlap=0)
           doc_splits = text_splitter.split_documents(doc)
           vectorstore = Chroma.from_documents(
               documents=doc_splits,
               collection_name="rag-chroma",
               embedding=OllamaEmbeddings(model="mxbai-embed-large:latest"),
           )
           retriever = vectorstore.as_retriever(k=3)
           after_rag_template = """Répondez à la question en vous basant uniquement sur le contexte suivant :
           {context}
           Question : {question}
           Si aucune réponse n'est possible, répondez "Désolé, le contexte est insuffisant pour répondre à la question.""""
           after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
           after_rag_chain = (
               {"context": retriever, "question": RunnablePassthrough()}
               | after_rag_prompt
               | model_local
               | StrOutputParser()
           )
           return after_rag_chain.invoke(question)

   - La fonction `retriever` gère la récupération des documents pertinents en fonction de la question et du texte donné, générant une réponse spécifique.

Utilisation du Projet
------------------------
Pour utiliser ce projet :
1. Remplacez le contenu du fichier PDF et la question avec vos propres documents et requêtes.
2. Assurez-vous que le serveur Ollama fonctionne à l'adresse spécifiée dans le modèle.

Structure des Fichiers
-------------------------
.. code-block::

    .
    ├── main.py                # Script principal contenant le code
    ├── .env                   # Fichier des variables d'environnement
    ├── requirements.txt       # Liste des dépendances
    ├── README.rst             # Documentation du projet
    ├── documents/             # Dossier contenant les fichiers PDF à traiter

Dépendances
-------------
Ajoutez les dépendances suivantes dans `requirements.txt` :

.. code-block:: text

    langchain
    chromadb
    streamlit
    pdfplumber
    langchain-core
    python-dotenv

Licence
-------
Ce projet est sous licence MIT.

Remerciements
---------------
Un grand merci aux équipes derrière Langchain, Ollama, et Streamlit pour leurs outils et APIs.



