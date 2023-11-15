import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.document_loaders import PyPDFLoader
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

def read_cv(cv):

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
