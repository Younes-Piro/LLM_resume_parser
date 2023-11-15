import openai
from dotenv import load_dotenv, find_dotenv
import os
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import json

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

def read_cv(cv_path):
    # load cv file
    i_f = open(cv_path,'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr,TxtConverter)
    for page in PDFPage.get_pages(i_f):
        interpreter.process_page(page)
 
    txt = retData.getvalue()
    return txt


def parse_cv(cv_text, openai_api_key, max_tokens=500):
    openai.api_key = openai_api_key

    # Define the conversation with the CV text as a variable
    conversation = [
        {"role": "system", "content": "Vous êtes un assistant d'analyse de CV."},
        {"role": "user", "content": f"Analysez le CV suivant et extrayez les informations pertinentes :\n\n{cv_text}"},
        {"role": "assistant", "content": "Informations extraites en JSON avec exactement la structure suivante : {information_basique : {nom, prenom, email, numero_telephone, location, linkedin_url, nom_universite, niveau_education, titre}, Expérience_professionnelle : [{Poste, Entreprise, Durée, Responsabilités/Réalisations}]}"},
    ]

    # Make the API call
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    max_tokens=max_tokens
    )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    # Print or use the assistant's reply as needed
    return assistant_reply

def load_json(text):
    result_json=json.loads(text)
    return result_json




