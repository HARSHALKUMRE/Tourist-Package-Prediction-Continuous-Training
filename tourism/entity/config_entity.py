from collections import namedtuple

DataIngestionConfig=namedtuple("DataIngestionConfig",["bucket_name","object_name","local_file_name","raw_data_dir","ingested_train_dir","ingested_test_dir"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])