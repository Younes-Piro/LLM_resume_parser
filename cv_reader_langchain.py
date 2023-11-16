import os
import openai
import json
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.document_loaders import PyPDFLoader
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

def read_cv_output_parser(cv):

    # load cv file
    loader = PyPDFLoader(cv)
    documents = loader.load()
    
    # prompt
    PROMPT = '''
    
        you are an experiment data extractor, you will help me to make a resume parser.
        
        following the context given, answer the questions asked \
        all the informations that you will provide me should be the exact answer and if the answer doesnt exist \
        the answer should be 'NONE'
        
        context : {context}
        
        questions : {questions}
        
        {format_instructions}
    '''

    #output parser
    response_schemas = [
    
        ResponseSchema(name="full_name", description="Describe the candidate entire name based on the context"),
        ResponseSchema(name="role", description="Describe the role of the candidate in the industry based on the context"),
        ResponseSchema(name="last_formation", description="Describe the latest academical formation of the candidate based on the context"),
        ResponseSchema(name="domaine_expertise", description="Describe the latest technologies and domaine expertise of the candidate based on the context"),
        ResponseSchema(name="ville_residance", description="Describe where the candidate is living based on the context"),
        ResponseSchema(name="email", description="Describe the email of the canditate based on the context"),
        ResponseSchema(name="experiences", description="A list of structured descriptions for all the candidate professional \
        experiences excluding academic and educational background, each in the format: \
        {'title': 'Describe from the document the title of the experience based on the information about this candidate', \
        'periode': 'Describe from the document the periode of the experience based on the information about this candidate', \
        'responsibilities': 'Describe from the document the responsibilities in the experience based on the information about this candidate', \
        'company': 'Describe from the document the company name based on the information about this candidate'}"),    
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    # prompt template
    prompt_template = PromptTemplate(
        template=PROMPT,
        input_variables=["context", "questions"],
        partial_variables={"format_instructions": format_instructions}
    )

    # load LLM
    llm_name = 'gpt-3.5-turbo'
    llm = ChatOpenAI(model_name=llm_name, temperature=0)

    # load chain
    qa_chain = LLMChain(llm=llm, prompt=prompt_template)

    # list the informations
    result = qa_chain({
        "questions": 'list all the candidate informations',
        "context": documents
    })

    return result["text"]


def read_cv(cv):

    # load cv file
    loader = PyPDFLoader(cv)
    documents = loader.load()

    # Prompt template with examples

    example_cv = '''PIRO YOUNES

        Étudiant en master Big Data 

        +212 6 94 800 614

        28 Comp AHLAN A2 IM 28, Tangier
        piroyounes148@gmail.com 

        linkedin.com/in/younes-piro

        github.com/Younes-piro

        Experience 

        Education 

        Data Scientist Intern

        PCA - Payment Center For Africa - Casablanca

        Février 2023 -
        Juillet 2023

        Création d'un modèle d'apprentissage automatique
        pour prédire l'appétence des clients envers
        l'utilisation des canaux digitaux

        Data Scientist Intern

        Juillet 2022 -
        Septembre 2022

        Full-stack dévelopeur
        intern

        Mars 2021 - Juin 2021

        CMAIS - Compagnie Méditerranéenne d'Analyse

        et d'Intelligence Stratégique - Rabat

        Assistance au développement d'une solution de
        knowledge management

        Maroc Advisor - Tanger

        Conception et Création d’une application web sous forme
        d’une solution pour les rendez-vous,  les paiements

            et facturation pour un cabinet de kinésithérapie 

        2021-2023

        2020-2021

        2017-2020

        

        Faculté des sciences et techniques de Tanger
        Master en Mobiquité et Big Data 

        Faculté des sciences et techniques de Tanger
        Licence en Génie informatique 

        Faculté des sciences et techniques de Tanger
        DEUST, MIPC (mathématique, Informatique , Physique et Chimie) 

        Certification

        IBM  - Big Data Engineer 2021 Mastery Award  Identifiant de la certification 4650-1655-9802-3105
        IBM - IOT Cloud Developer 2021 Mastery Award  Identifiant de la certification 4665-1658-1469-8442
        LinkedIn - Machine learning : Traitement du langage naturel avec Python
        365 Data Science : Power BI certification

        Academic
        Projects

        2022

        2022

        2022-2023

        Développement  d'une  plateforme  web  d'ETL  et
        de  visualisation  pour  l'analyse  des  données  des
        appartements au Maroc

        Technologies et outils: angular13 - Django - pandas - Plotly -
        BeautifulSoup -  MongoDb - Elasticsearch - kebana - graphql

        Réalisation  d'une  solution  décisionnelle  pour
        analyser les indicateurs clés de performance (KPI)
        de 
        la  Faculté  des  Sciences  et  Techniques  de
        Tanger

        Technologies et outils: Microsoft Power BI - MS-BI(SSIS - SSAS)

        Application  web  pour  consumer  un  model  deep
        learning  base  sur  une  architecture  LSTM  pour
        prédire les ventes futures

        Technologies et outils: React - FASTAPI - RNN - LSTM - TensorFlow -
        Keras 

        Skills

        Langues

        Programming Languanges

        Business Intelligence:

        DB:

        web development

        ML - DL :

        Python(Pandas, Numpy, Matplotlib,
        Seaborn)
        Microsoft Power BI/ MS-BI(SSIS-SSAS)

        SQL Server/ Mysql/ mongodb

        Django - Flask - FastApi 

        NLP - Tenserflow - Keras - Scikit learn

        Arabe

        Francais

        Anglais

        langue maternelle

        Courant

        Technique
        '''

    result_cv='''
    {
    "informations_basiques": {
        "nom": "PIRO",
        "prenom": "YOUNES",
        "email": "piroyounes148@gmail.com",
        "numero_telephone": "+212 6 94 800 614",
        "location": "28 Comp AHLAN A2 IM 28, Tangier",
        "linkedin_url": "linkedin.com/in/younes-piro",
        "nom_universite": "Faculté des sciences et techniques de Tanger",
        "niveau_education": "Master en Mobiquité et Big Data",
        "titre": "Étudiant en master Big Data"
    },
    "expérience_professionnelle": [
        {
        "poste": "Data Scientist Intern",
        "entreprise": "PCA - Payment Center For Africa",
        "durée": "Février 2023 - Juillet 2023",
        "responsabilités/réalisations": ["Création d'un modèle d'apprentissage automatique pour prédire l'appétence des clients envers l'utilisation des canaux digitaux"]
        },
        {
        "poste": "Data Scientist Intern",
        "entreprise": "CMAIS - Compagnie Méditerranéenne d'Analyse et d'Intelligence Stratégique",
        "durée": "Juillet 2022 - Septembre 2022",
        "responsabilités/réalisations": ["Assistance au développement d'une solution de knowledge management"]
        },
        {
        "poste": "Full-stack dévelopeur intern",
        "entreprise": "Maroc Advisor",
        "durée": "Mars 2021 - Juin 2021",
        "responsabilités/réalisations": ["Conception et Création d’une application web sous forme d’une solution pour les rendez-vous, les paiements et facturation pour un cabinet de kinésithérapie"]
        }
    ]
    }
    '''

    result_json=json.loads(result_cv)

    assistance_template = """ 

        Voici un exemple qui doit vous aidez pour analyser d'une maniere precise le CV:

        Input: {example_cv} \n\n
        Output: ```json {result_cv} ```

    """

    assistance_prompt = assistance_template.format(example_cv=example_cv, result_cv=result_json)

    # prompt
    PROMPT = '''
        Vous êtes un assistant d'analyse de CV
        
        Analysez le CV suivant et extrayez les informations pertinentes :\n\n {cv_text}
        
        Informations extraites en JSON avec exactement la structure suivante : "information_basique : [nom, prenom, email, numero_telephone, location, linkedin_url, nom_universite, niveau_education, titre], Expérience_professionnelle : [Poste, Entreprise, Durée, Responsabilités/Réalisations]"
    '''

    FINAL_PROMPT = PROMPT + assistance_prompt

    # prompt template
    prompt_template = PromptTemplate(
        template=FINAL_PROMPT,
        input_variables=["cv_text"]
    )

    # load LLM
    llm_name = 'gpt-3.5-turbo'
    llm = ChatOpenAI(model_name=llm_name, temperature=0)

    # load chain
    qa_chain = LLMChain(llm=llm, prompt=prompt_template)

    # list the informations
    result = qa_chain({
        "cv_text": documents
    })

    return result["text"]