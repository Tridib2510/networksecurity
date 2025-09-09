from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurtiyException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=='__main__':
   try:
    #   Initiate Data ingestion
    trainingpipelineconfig=TrainingPipelineConfig()
    dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
    data_ingestion=DataIngestion(dataingestionconfig)
    logging.info("Initiate the data ingestion")
    dataIngestionArtifact=data_ingestion.initiate_data_ingestion()
    print(dataIngestionArtifact)


   except Exception as e:
      raise NetworkSecurtiyException(e,sys)