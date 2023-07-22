import os
import sys
from typing import Union

import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from tourism.entity.config_entity import DataTransformationConfig
from tourism.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from tourism.components.data_ingestion import DataIngestion
from tourism.constant.training_pipeline import *
from tourism.exception import CustomException
from tourism.logger import logging
from tourism.utils.main_utils import read_yaml_file, save_object, save_numpy_array_data, load_data

class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e


    def get_data_transformer_object(self) -> ColumnTransformer:
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )
        try:
            logging.info(
                "Got numerical, categorical, transformation columns from schema config"
            )
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]
            discrete_columns = dataset_schema[DISCRETE_COLUMN_KEY]
            continuous_columns = dataset_schema[CONTINUOUS_COLUMN_KEY]
            transformation_columns = dataset_schema[TRANSFORMATION_COLUMN_KEY]

            logging.info("Initialized Data Transformer pipeline.")

            discrete_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("scaler", StandardScaler()),
                ]
            )

            continuous_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("scaler", StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            transform_pipe = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("transformer", PowerTransformer(standardize=True)),
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ("Discrete_Pipeline", discrete_pipeline, discrete_columns),
                    ("Continuous_Pipeline", continuous_pipeline, continuous_columns),
                    ("Categorical_Pipeline", cat_pipeline, categorical_columns),
                    ("Power_Transformation", transform_pipe, transformation_columns),
                ]
            )

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info(f"Obtaining training and test file path.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            logging.info(
                f"Loading training and test data as pandas dataframe.")
            train_df = load_data(file_path=train_file_path,
                                 schema_file_path=schema_file_path)

            test_df = load_data(file_path=test_file_path,
                                schema_file_path=schema_file_path)

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]
            
            logging.info(
                f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(
                columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[[target_column_name]]

            input_feature_test_df = test_df.drop(
                columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[[target_column_name]]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df)

            logging.info(
                    "Used the preprocessor object to fit transform the train features"
                )
            input_feature_test_arr = preprocessing_obj.transform(
                input_feature_test_df)
            logging.info("Used the preprocessor object to transform the test features")

            logging.info(
                    "Used the preprocessor object to transform the test features"
                )
            
            logging.info("Applying SMOTEENN on Training dataset")

            smt = SMOTEENN(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )

            logging.info("Applied SMOTEENN on training dataset")

            logging.info("Applying SMOTEENN on testing dataset")

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )

            logging.info("Applied SMOTEENN on testing dataset")

            logging.info("Created train array and test array")

            train_arr = np.c_[
                    input_feature_train_final, np.array(target_feature_train_final)
                ]

            test_arr = np.c_[
                    input_feature_test_final, np.array(target_feature_test_final)
                ]
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(
                train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(
                test_file_path).replace(".csv", ".npz")
            
            transformed_train_file_path = os.path.join(
                transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(
                transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")

            save_numpy_array_data(
                file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(
                file_path=transformed_test_file_path, array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,
                        obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
                                                                      message="Data transformation successfull.",
                                                                      transformed_train_file_path=transformed_train_file_path,
                                                                      transformed_test_file_path=transformed_test_file_path,
                                                                      preprocessed_object_file_path=preprocessing_obj_file_path
                                                                      )
            logging.info(
                f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e

    def __del__(self):
        logging.info(
            f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")