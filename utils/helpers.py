import json
from dateutil import parser
from datetime import datetime
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

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

def format_cv(cv_parsed):
  data = {}

  #basic information
  data['nom'] = cv_parsed['information_basique']['nom']
  data['prenom'] = cv_parsed['information_basique']['prenom']
  data['email'] = cv_parsed['information_basique']['email']
  data['phone'] = cv_parsed['information_basique']['numero_telephone']
  data['location'] = cv_parsed['information_basique']['location']
  data['titre'] = cv_parsed['information_basique']['titre_professionnel']

  # numero mois d'experience
  data['months_experiences'] = extract_experience_duration(cv_parsed['Expérience_professionnelle'])

  # responsibilites
  data['responsibilities'] = all_responsibilies(cv_parsed['Expérience_professionnelle'])

  #Skills 
  data['Programming_languages'] = cv_parsed['skills']['Programming_languages']

  return data

def format_job(job_parsed):
    data = {}

    data['post'] = job_parsed['information_post']['intitule_poste']
    data['months_experiences']   = ( int((job_parsed['information_post']['année_experience'].split())[0] if ' ' in job_parsed['information_post']['année_experience'] else job_parsed['information_post']['année_experience']) * 12 ) 
    data['programming_skills'] = job_parsed['Skills']['Programming_languages']
    data['responsibilities']   = job_parsed['Skills']['responsibilities']
    data['theorical_skills']   = job_parsed['Skills']['theorical_skills']
    return data

# function to read the pdf
def read_pdf(cv_path):
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