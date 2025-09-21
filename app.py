# Used to trigger the entire pipeline

import sys
import os
import certifi
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurtiyException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

"""
FastAPI is a modern, fast (high-performance) web framework for 
building APIs with Python.
"""


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
"""
FastAPI -->The main class used to create the API app
CORSMiddleware --> To handle Cross-Origin Resource Sharing (CORS) issues
File, UploadFile --> To handle file uploads
Request --> To handle incoming HTTP requests
"""
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["authentication"])
# It groups this endpoint under the tag Authentication in the API docs.
async def index():
    return RedirectResponse(url="/docs")
# When someone hits the / endpoint, instead of showing something, it redirects them to /docs.

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!!")
    except Exception as e:
        raise NetworkSecurtiyException(e,sys)
    
if __name__=="__main__":
    app.run(app,host="localhost",port=8000)

"""
uvicorn app:app --reload
The command to run the FastAPI application using Uvicorn.
--reload flag enables auto-reloading of the server on code changes.
Uvicorn is an ASGI server that runs FastAPI applications.
app:app specifies the module (app.py) and the FastAPI instance (app) to run.
"""