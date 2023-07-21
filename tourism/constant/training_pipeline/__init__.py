import os
from datetime import datetime

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


ROOT_DIR = os.getcwd()
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
SCHEMA_FILE_NAME = "schema.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, SCHEMA_FILE_NAME)

CURRENT_TIME_STAMP = get_current_time_stamp()

# Training pipeline realted variables
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

# Data Ingestion realted variables or constant
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
S3_BUCKET_NAME_KEY = "bucket_name"
S3_OBJECT_NAME_KEY = "object_name"
LOCAL_FILE_NAME_KEY = "local_file_name"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY = "ingested_test_dir"

# Data Validation related variables or constant
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR_NAME = "data_validation"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name" 

DATASET_SCHEMA_COLUMNS_KEY =  "ColumnNames"
NUMERICAL_COLUMN_KEY = "Numerical_columns"
CATEGORICAL_COLUMN_KEY = "Categorical_columns"
ONEHOT_COLUMNS_KEY = "onehot_columns"
BINARY_COLUMNS_KEY = "binary_columns"


TARGET_COLUMN_KEY="target_column"

