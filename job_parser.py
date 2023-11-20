import openai
import os
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io


# Set your GPT-3 API key
openai.api_key = os.environ['OPENAI_API_KEY']

def read_pdf(pdf):
    # load cv file
    i_f = open(pdf,'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr,TxtConverter)
    for page in PDFPage.get_pages(i_f):
        interpreter.process_page(page)
 
    txt = retData.getvalue()
    return txt


def parse_job(description_de_poste, openai_api_key, max_tokens):

    openai.api_key = openai_api_key

    # Définissez la conversation avec la description de poste comme variable
    conversation = [
        {"role": "system", "content": "Vous êtes un analyseur de descriptions de poste."},
        {"role": "user", "content": f"Analysez la description de poste suivante et extrayez les informations pertinentes :\n\n{description_de_poste}"},
        {"role": "assistant", "content": "Informations extraites en JSON avec exactement la structure suivante : {information_post : {intitule_poste, année_experience}, Skills : {Programming_languages, responsibilities, theorical_skills}}" }

    ]

    # Effectuez l'appel à l'API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=max_tokens
    )

    # Extrayez la réponse de l'assistant
    assistant_reply = response['choices'][0]['message']['content']

    # Affichez ou utilisez la réponse de l'assistant selon vos besoins
    print(assistant_reply)