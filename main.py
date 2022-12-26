import pandas as pd

from CO2.exception import CO2_Exception
import sys,os
from CO2 import utils
from CO2.logger import logging
from CO2.entity import config_entity
from CO2.components.data_validation import DataValidation
from CO2.components.data_ingestion import DataIngestion


if __name__ == "__main__":
    training_pipeline_config = config_entity.TrainingPipelineConfig()
    data_ingestion = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
    a = utils.convert_nc4_to_csv(complete_folder_path=data_ingestion.nc4_data_file_path)
    b = utils.power_plant_dataset(complete_folder_path=data_ingestion.power_plant_file_path)
    c = utils.city_dataset(complete_folder_path=data_ingestion.city_data_file_path)
    d = utils.fire_dataset(complete_folder_path= data_ingestion.fire_data_file_path)
    e = utils.cement_dataset(complete_folder_path=data_ingestion.cement_data_file_path)
    f = utils.population_dataset(complete_folder_path=data_ingestion.population_file_path)

    df = pd.merge(a,b, how='left',
                  left_on=['lat', 'lon'],
                  right_on=['latitude','longitude'])
    df.drop(columns=['latitude','longitude'], inplace=True)
    df.to_csv(r"C:\Users\preet\Desktop\merge1.csv", index=False)

    df = pd.merge(df,c, how='left',
                  left_on=['lat', 'lon'],
                  right_on=['latitude','longitude'])
    df.drop(columns=['latitude','longitude','capital'], inplace=True)
    df.to_csv(r"C:\Users\preet\Desktop\merge2.csv", index=False)

    df = pd.merge(df,d, how='left',
                  left_on=['lat', 'lon', 'Year', 'Month'],
                  right_on=['latitude','longitude', 'year', 'month'])
    df.drop(columns=['latitude','longitude','year', 'month'], inplace=True)
    df.to_csv(r"C:\Users\preet\Desktop\merge3.csv", index=False)

    df = pd.merge(df,e, how='left',
                  left_on=['lat', 'lon'],
                  right_on=['latitude','longitude'])
    df.drop(columns=['latitude','longitude'], inplace=True)
    df.to_csv(r"C:\Users\preet\Desktop\merge4.csv", index=False)

    df = pd.merge(df,f, how='left',
                  left_on=['lat', 'lon', 'Year'],
                  right_on=['latitude','longitude', 'year'])
    df.drop(columns=['latitude','longitude', 'year', 'city', 'state'], inplace=True)
    df.to_csv(r"C:\Users\preet\Desktop\merge5.csv", index=False)


# merge1 = pd.read_csv(r"C:\Users\preet\Desktop\merge1.csv")
# merge2 = pd.read_csv(r"C:\Users\preet\Desktop\merge2.csv")
# merge3 = pd.read_csv(r"C:\Users\preet\Desktop\merge3.csv")
# merge4 = pd.read_csv(r"C:\Users\preet\Desktop\merge4.csv")
# merge5 = pd.read_csv(r"C:\Users\preet\Desktop\merge5.csv")
#
# print(merge1[merge1.duplicated()])
# print('========================================')
# print(merge2[merge2.duplicated()])
# print('========================================')
# print(merge3[merge3.duplicated()])
# print('========================================')
# print(merge4[merge4.duplicated()])
# print('========================================')
# print(merge5[merge5.duplicated()])

