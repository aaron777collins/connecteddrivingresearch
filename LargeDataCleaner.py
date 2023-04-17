# reads each file from the split folder and cleans them and then saves them in the cleaned split folder
from ast import Dict
import os

import numpy as np
from DataCleaner import DataCleaner
from Logger import Logger
import pandas as pd
import os.path as path
import glob as glob

from MathHelper import MathHelper

class LargeDataCleaner:
    def __init__(self, splitfilespath="data/split/", cleanedsplitfilespath="data/cleaned/split/", combinedcleandatapath="data/cleaned/combined.csv", logger=Logger("LargeDataCleaner")):
        self.splitfilespath = splitfilespath
        self.cleanedfilespath = cleanedsplitfilespath
        self.combinedcleandatapath = combinedcleandatapath
        self.logger = logger

    def clean_data(self, filterFunction=None, cleanFunc=DataCleaner.clean_data_with_timestamps, **kwargs):
        # reads each file from the split folder and cleans them and then saves them in the cleaned split folder
        glob.glob(self.splitfilespath + "*.csv")

        # create the cleaned split folder if it doesn't exist
        os.makedirs(path.dirname(self.cleanedfilespath), exist_ok=True)

        # check if there is already a cleaned file for this model type
        if len(glob.glob(self.cleanedfilespath + "*.csv")) > 0:
            self.logger.log("Found cleaned files! Skipping regeneration.")
            return self

        for file in glob.glob(self.splitfilespath + "*.csv"):
            self.logger.log(f"Cleaning file {file}")
            df = pd.read_csv(file)
            dc = DataCleaner(data=df, logger=self.logger.newPrefix("DataCleaner"))
            newDf = cleanFunc(dc, **kwargs).getCleanedData()
            if (filterFunction != None):
                newDf = filterFunction(newDf, **kwargs)

            # only write file if there are rows in newDf
            if len(newDf) > 0:
                newDf.to_csv(self.cleanedfilespath + path.basename(file), index=False)
            else:
                self.logger.log(f"Skipping writing file {file} because it has no rows.")

        return self

    @staticmethod
    def within_range(df, x_col="x_pos", y_col="y_pos", x_pos=0, y_pos=0, max_dist=10000, **kwargs):
        # calculate the distance between each point and (x_pos, y_pos)
        df = df.copy()
        df['distance'] = df.apply(lambda row: MathHelper.dist_between_two_points(row[x_col], row[y_col], x_pos, y_pos), axis=1)
        # filter out points that are outside the max distance
        df = df[df['distance'] <= max_dist]
        # drop the 'distance' column
        df.drop('distance', axis=1, inplace=True)
        return df

    @staticmethod
    def within_rangeXY(df, x_col="x_pos", y_col="y_pos", max_dist=10000, **kwargs):
        # assume (0, 0) is the center of the map
        x_pos = 0
        y_pos = 0
        # calculate the distance between each point and (x_pos, y_pos)
        df = df.copy()
        df['distance'] = df.apply(lambda row: MathHelper.dist_between_two_pointsXY(row[x_col], row[y_col], x_pos, y_pos), axis=1)
        # filter out points that are outside the max distance
        df = df[df['distance'] <= max_dist]
        # drop the 'distance' column
        df.drop('distance', axis=1, inplace=True)
        return df

    def combine_data(self):
        # search the cleaned split folder for all csv files
        # combine them into one csv file

        # make sure the combined data folder exists
        os.makedirs(path.dirname(self.combinedcleandatapath), exist_ok=True)

        # check if the combined data file already exists
        if(path.exists(self.combinedcleandatapath)):
            self.logger.log("Found combined data file! Skipping regeneration.")
            return self

        first_file = True
        with open(self.combinedcleandatapath, 'w') as outfile:
            for file in glob.glob(self.cleanedfilespath + "*.csv"):
                self.logger.log(f"Combining file {file}")
                with open(file) as infile:
                    if first_file:
                        # Write the header row for the first file
                        outfile.write(infile.readline())
                        first_file = False
                    else:
                        # Skip the header row for subsequent files
                        infile.readline()

                    outfile.write(infile.read())


    default_dtypes = {
        # metadata_generatedAt,metadata_recordType,metadata_serialId_streamId,metadata_serialId_bundleSize,metadata_serialId_bundleId,metadata_serialId_recordId,metadata_serialId_serialNumber,metadata_receivedAt,coreData_id,coreData_secMark,coreData_position_lat,coreData_position_long,coreData_accuracy_semiMajor,coreData_accuracy_semiMinor,coreData_elevation,coreData_accelset_accelYaw,coreData_speed,coreData_heading,x_pos,y_pos,month,day,year,hour,minute,second,pm
        # 2019-04-24 13:04:14,rxMsg,4acfcee9-59da-45bb-aaca-c1f548b9540a,960,1793,247,800342,06/26/2019 09:00:43 PM,54420000,14500,41.0980636,-105.1133162,6.8,9.65,2153.9,-0.27,30.0,280.4125,-105.1133162,41.0980636,4,24,2019,13,4,14,1
        # 2019-04-24 13:04:14,rxMsg,4acfcee9-59da-45bb-aaca-c1f548b9540a,960,1793,252,800347,06/26/2019 09:00:43 PM,54420000,15000,41.098088,-105.1134922,6.8,9.65,2154.4,0.0,30.06,280.3375,-105.1134922,41.098088,4,24,2019,13,4,14,1
        "metadata_generatedAt": "str",
        "metadata_recordType": "str",
        "metadata_serialId_streamId": "str",
        "metadata_serialId_bundleSize": "str",
        "metadata_serialId_bundleId": "str",
        "metadata_serialId_recordId": "str",
        "metadata_serialId_serialNumber": "str",
        "metadata_receivedAt": "str",
        "coreData_id": "str",
        "coreData_secMark": "int64",
        "coreData_position_lat": "float64",
        "coreData_position_long": "float64",
        "coreData_accuracy_semiMajor": "float64",
        "coreData_accuracy_semiMinor": "float64",
        "coreData_elevation": "float64",
        "coreData_accelset_accelYaw": "float64",
        "coreData_speed": "float64",
        "coreData_heading": "float64",
        "x_pos": "float64",
        "y_pos": "float64",
        "month": "int64",
        "day": "int64",
        "year": "int64",
        "hour": "int64",
        "minute": "int64",
        "second": "int64",
        "pm": "int64"
    }

    def getNRows(self, n, dtypes=default_dtypes):
        # returns n rowsfrom the data from the combined file. ONLY reads n rows
        #  reads n lines of a file and saves it again as [filename]-[n].csv

        # checking if the file already exists
        if path.exists(self.combinedcleandatapath + "-" + str(n) + ".csv"):
            self.logger.log(f"Found file {self.combinedcleandatapath + '-' + str(n) + '.csv'}! Skipping regeneration.")
            return pd.read_csv(self.combinedcleandatapath + "-" + str(n) + ".csv", dtype=dtypes)

        # reading n lines of the file and saving it again
        df = pd.read_csv(self.combinedcleandatapath, nrows=n, dtype=dtypes)
        df.to_csv(self.combinedcleandatapath + "-" + str(n) + ".csv", index=False)


        df = pd.read_csv(self.combinedcleandatapath + "-" + str(n) + ".csv", dtype=dtypes)
        return df

