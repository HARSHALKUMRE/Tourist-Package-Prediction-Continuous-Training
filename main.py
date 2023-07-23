import os, sys
import pandas as pd
import numpy as np
from tourism.constant.training_pipeline import *
from tourism.logger import logging
from tourism.exception import CustomException
from tourism.pipeline.training_pipeline import Pipeline

def main():
    try:
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")

if __name__ == "__main__":
    main() 