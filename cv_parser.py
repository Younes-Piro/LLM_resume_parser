import openai
from dotenv import load_dotenv, find_dotenv
import os
from langchain.document_loaders import PyPDFLoader

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

def read_cv(cv_path):
    # load cv file
    loader = PyPDFLoader(cv_path)
    documents = loader.load()

    result = ""
    if len(documents) > 1:
        for doc in documents:
           result = f"{result} {doc.page_content}" 
    else:
        result = f"{result} {documents[0].page_content}"

    return result


def parse_cv(cv_text, openai_api_key):
    openai.api_key = openai_api_key

    # Define the conversation with the CV text as a variable
    conversation = [
        {"role": "system", "content": "You are a CV parsing assistant."},
        {"role": "user", "content": f"Parse the following CV and extract relevant information:\n\n{cv_text}"},
        {"role": "assistant", "content": "---\nExtracted Information:\n1. Personal Information:\n   - Full Name:\n   - Contact Information:\n\n2. Education:\n   - Degree:\n   - Major:\n   - School/University:\n   - Graduation Year:\n\n3. Work Experience:\n   - Position:\n   - Company:\n   - Duration:\n   - Responsibilities/Accomplishments:\n\n   - Position:\n   - Company:\n   - Duration:\n   - Responsibilities/Accomplishments:\n\n4. Skills:\n   - List of skills mentioned in the CV.\n\n5. Additional Information:\n   - Any additional noteworthy details.\n\n---\nClarifications/Questions:\n- If any information is unclear or missing, ask for clarification or request additional details."}
    ]

    # Make the API call
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    max_tokens=400
    )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    # Print or use the assistant's reply as needed
    return assistant_reply






