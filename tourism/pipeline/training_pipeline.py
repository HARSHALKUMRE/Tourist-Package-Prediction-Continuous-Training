import os, sys
import pandas as pd
import numpy as np
from tourism.constant.training_pipeline import *
from tourism.logger import logging
from tourism.entity.config_entity import DataIngestionConfig
from tourism.entity.artifact_entity import DataIngestionArtifact
from tourism.exception import CustomException
from datetime import date
from collections import namedtuple
from tourism.configuration.configuration_file import Configuration
from tourism.components.data_ingestion import DataIngestion

class TrainingPipeline():
    def __init__(self, config: Configuration = Configuration())->None:
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e,sys) from e  
        
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config = self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e  
        
    
        
    def run_pipeline(self):
        try:
            # Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e  