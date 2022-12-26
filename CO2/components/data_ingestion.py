import pandas as pd
import numpy as np
from CO2 import utils
from CO2.entity import config_entity
from CO2.entity import artifact_entity
from CO2.exception import CO2_Exception
import sys, os
from CO2.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            logging.info('================== Data Ingestion Class =========================')
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CO2_Exception(e, sys)

    def initiate_data_ingestion(self) -> artifact_entity.DataIngestionArtifact:
        try:
            # Exporting the data as pandas DataFrame
            logging.info('================== Initiate Data Ingestion =========================')

            # Converting the all the CDF4 data to a single csv file
            df_co2: pd.DataFrame = utils.convert_nc4_to_csv(complete_folder_path=self.data_ingestion_config.nc4_data_file_path)
            logging.info(f'Folder path is {self.data_ingestion_config.nc4_data_file_path}')

            # extracting the cement data
            df_cement: pd.DataFrame = utils.cement_dataset(complete_folder_path=self.data_ingestion_config.cement_data_file_path)
            df = pd.merge(df_co2,df_cement, how='outer', left_on=['lat','lon'], right_on= ['latitude','longitude'])

            # extracting the city data
            df_city: pd.DataFrame = utils.city_dataset(complete_folder_path=self.data_ingestion_config.city_data_file_path)
            df = pd.merge(df,df_city, how='outer', left_on=['lat','lon'], right_on= ['latitude','longitude'])

            # Extracting the fire data
            df_fire: pd.DataFrame = utils.fire_dataset(complete_folder_path=self.data_ingestion_config.fire_data_file_path)
            df = pd.merge(df, df_fire, how='outer', left_on=['lat','lon'], right_on= ['latitude','longitude'])

            # extracting Population data
            df_population: pd.DataFrame = utils.population_dataset(complete_folder_path= self.data_ingestion_config.population_file_path)
            df = pd.merge(df, df_population, how='outer', left_on=['lat','lon'], right_on= ['latitude','longitude'])

            # Extracting the power plant data
            df_power_plant: pd.DataFrame = utils.power_plant_dataset(complete_folder_path=self.data_ingestion_config.power_plant_file_path)
            df = pd.merge(df, df_power_plant, how='outer', left_on=['lat','lon'], right_on= ['latitude','longitude'])

            for i in df[df['Year'] < df['commissioning_year']].index:
                df.at[i, 'primary_fuel'] = np.NaN
                df.at[i, 'commissioning_year'] = np.NaN
                df.at[i, 'capacity_mw'] = np.NaN

            # Create a feature store folder
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            logging.info(f'Created folder {feature_store_dir}')

            # Save data to the feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index = False)
            logging.info(f'Data compiled and stored to {self.data_ingestion_config.feature_store_file_path} ')

            # prepare the artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                                                    feature_store_file_path=self.data_ingestion_config.feature_store_file_path)
            logging.info('============= Data Ingestion completed =========================')

            return data_ingestion_artifact

        except Exception as e:
            raise CO2_Exception(e, sys)


