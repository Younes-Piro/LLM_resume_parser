import openai
from dotenv import load_dotenv, find_dotenv
import os
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import json
import re
from dateutil import parser
from datetime import datetime


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
        {"role": "assistant", "content": "Informations extraites en JSON avec exactement la structure suivante : {information_basique : {nom, prenom, email, numero_telephone, location, linkedin_url, nom_universite, niveau_education, titre_professionnel}, Expérience_professionnelle : [{Poste, Entreprise, Durée(format : { 'start_date' : %m-YYYY, 'end_date' : %m-YYYY} ), Responsabilités/Réalisations}], skills : {Programming_languages}}"},
        
    ]

    # Make the API call
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    max_tokens=max_tokens, 
    temperature=0
    )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    # Print or use the assistant's reply as needed
    return assistant_reply

def load_json(text):
    result_json=json.loads(text)
    return result_json

# convert experiences duration to specific format
def convert_to_standard_format(date_str):
    # Try to parse the date using dateutil.parser
    try:
        parsed_date = parser.parse(date_str)
    except ValueError:
        return None

    # Format the parsed date into 'YYYY-MM' format
    formatted_date = datetime.strftime(parsed_date, "%Y-%m")
    return formatted_date

#extract and sum all work experiences
def extract_experience_duration(experiences):
    all_experience_duration = []
    num_exp = 0
    for exp in experiences:
        if not any(keyword in exp["Poste"].lower() for keyword in ["internship", "intern", "stage", "pfe"]): 
            # Use the convert_to_standard_format function for start_date and end_date
            start_date_str = convert_to_standard_format(exp['Durée']['start_date'])
            end_date_str = convert_to_standard_format(exp['Durée']['end_date']) if exp['Durée']['end_date'].lower() != 'present' else datetime.now().strftime("%Y-%m")
            
            # Try to parse the standardized dates
            start_date = datetime.strptime(start_date_str, "%Y-%m") if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m") if end_date_str else datetime.now()
            
            # Calculate the difference in months
            if start_date:
                months_difference = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
                all_experience_duration.append(months_difference)
           
    return ( sum(all_experience_duration) + len(all_experience_duration) - 1 )  

# extract all responsibilites from different experiences
def all_responsibilies(experiences):
    all_resp = []
    for exp in experiences:
        if not any(keyword in exp["Poste"].lower() for keyword in ["internship", "intern", "stage", "pfe"]):
            all_resp.extend(exp['Responsabilités/Réalisations'])
    
    return all_resp   

def format_data(cv_parsed):
  data = {}

  #basic information
  data['nom'] = cv_parsed['information_basique']['nom']
  data['prenom'] = cv_parsed['information_basique']['prenom']
  data['email'] = cv_parsed['information_basique']['email']
  data['phone'] = cv_parsed['information_basique']['numero_telephone']
  data['location'] = cv_parsed['information_basique']['location']
  data['titre'] = cv_parsed['information_basique']['titre_professionnel']

  # numero mois d'experience
  data['month_experiences'] = extract_experience_duration(cv_parsed['Expérience_professionnelle'])

  # responsibilites
  data['responsibilities'] = all_responsibilies(cv_parsed['Expérience_professionnelle'])

  return data


