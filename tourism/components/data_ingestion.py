import os, sys
from tourism.entity.config_entity import DataIngestionConfig
from tourism.entity.artifact_entity import DataIngestionArtifact
from tourism.logger import logging
from tourism.exception import CustomException
import numpy as np
import pandas as pd
from six.moves import urllib
from sklearn.model_selection import train_test_split
from tourism.utils.s3_operation import download_from_s3
from tourism.constant.training_pipeline import SCHEMA_FILE_PATH
from tourism.utils.main_utils import read_yaml_file


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):

        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys) from e 

    def download_tourism_data(self) -> str:
        try:
            #extraction remote url to download dataset
            bucket_name = self.data_ingestion_config.bucket_name
            object_name = self.data_ingestion_config.object_name
            local_file_name = self.data_ingestion_config.local_file_name
            
            #folder location to download file
            download_dir = self.data_ingestion_config.raw_data_dir
            
            os.makedirs(download_dir,exist_ok=True)

            raw_data_dir = os.path.join(download_dir, local_file_name)
            
            download_from_s3(bucket_name=bucket_name, 
                             object_name= object_name, 
                             filename=raw_data_dir)
        
            logging.info(f"File :[{raw_data_dir}] has been downloaded successfully.")
            return raw_data_dir

        except Exception as e:
            raise CustomException(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            data_file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file: [{data_file_path}]")
            data_frame = pd.read_csv(data_file_path, index_col=False)
            data_frame.drop(self._schema_config["Drop_columns"], axis=1, inplace=True)

            logging.info(f"Splitting data into train and test")
            train_set = None
            test_set = None

            train_set, test_set = train_test_split(data_frame, test_size=0.2, random_state=42)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                train_set.to_csv(train_file_path,index=False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                test_set.to_csv(test_file_path,index=False)
            
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys) from e


    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            raw_data_dir =  self.download_tourism_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise CustomException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")