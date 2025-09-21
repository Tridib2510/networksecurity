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
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
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
from fastapi.templating import Jinja2Templates
# Jinja2Templates is used to render HTML templates using the 
# Jinja2 templating engine.
templates=Jinja2Templates(directory="./templates")

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

@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    # File(...) indicates that this parameter is required.
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred=network_model.predict(df)
        print(y_pred)
        df["predicted_column"]=y_pred
        print(df['predicted_column'])
        df.to_csv("prediction_output/output.csv")
        # Saves the DataFrame with predictions to a CSV file.
        # We can also update this csv to mongodb if needed
        table_html=df.to_html(classes="table table-striped")
        # Converts the DataFrame to an HTML table with Bootstrap classes for styling.
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
        # Renders the table.html template, passing the request and the generated HTML table.
    except Exception as e:
        raise NetworkSecurtiyException(e,sys)
"""
uvicorn app:app --reload
The command to run the FastAPI application using Uvicorn.
--reload flag enables auto-reloading of the server on code changes.
Uvicorn is an ASGI server that runs FastAPI applications.
app:app specifies the module (app.py) and the FastAPI instance (app) to run.
"""
