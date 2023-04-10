# reads each file from the split folder and cleans them and then saves them in the cleaned split folder
import os
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
            newDf = cleanFunc(dc).getCleanedData()
            if (filterFunction != None):
                newDf = filterFunction(newDf, **kwargs)

            # only write file if there are rows in newDf
            if len(newDf) > 0:
                newDf.to_csv(self.cleanedfilespath + path.basename(file), index=False)
            else:
                self.logger.log(f"Skipping writing file {file} because it has no rows.")

        return self

    def within_range(self, df, x_col="x_pos", y_col="y_pos", x_pos=0, y_pos=0, max_dist=10000):
        # calculate the distance between each point and (x_pos, y_pos)
        df = df.copy()
        df['distance'] = df.apply(lambda row: MathHelper.dist_between_two_points(row[x_col], row[y_col], x_pos, y_pos), axis=1)
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

        with open(self.combinedcleandatapath, 'w') as outfile:
            for file in glob.glob(self.cleanedfilespath + "*.csv"):
                self.logger.log(f"Combining file {file}")
                with open(file) as infile:
                    outfile.write(infile.read())
