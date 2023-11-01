import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging as lg
from config import IngestionConfig,TransformationConfig
from src.components.transformation import Transformation
from src.components.model_trainer import ModelTrainer

class Ingestion:
    def __init__(self):
        self.ingestion_config=IngestionConfig()

    def initiate_data_ingestion(self):

        lg.info("Entered the data ingestion method ")

        try:
            df=pd.read_csv('data\kidney_disease.csv')
            lg.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            lg.info("Train test split initiated")

            train_df,test_df=train_test_split(df,test_size=0.2,random_state=10)
            train_df.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_df.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            lg.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=Ingestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=Transformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
