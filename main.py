from db_connection import DB
from cv_parser import parse_cv
from utils.helpers import *
from glob import glob
from job_parser import parse_job
from dotenv import load_dotenv, find_dotenv
from matching import matching
import os
import openai

_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']

#load db connection
connection = DB()

# load location of pdfs
all_pdfs = glob('./data/*pdf')

#cv_path
cv_path = all_pdfs[0]

# parse cv
#read text from pdf
cv_text = read_pdf(cv_path)

#parse cv using openai api
result_cv = parse_cv(cv_text, openai.api_key)

#convert result to json
result_json = load_json(result_cv)

# format data 
data_cv = format_cv(result_json)

# load data to mongo
connection.add_data(data_cv)

# parse job description
job_path = glob('./data/description.pdf')
job_text = read_pdf(job_path)

# parse the job
result_job = parse_job(job_text, openai.api_key)

# move from entire json into json format
result_js = load_json(result_job)

# format data 
data_job = format_job(result_js)

score = matching(data_cv, data_job)
