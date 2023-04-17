# MClassifierPipeline-Const-50-offset

import os
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from DataAttacker import DataAttacker
from DataCleaner import DataCleaner
from DataGatherer import DataGatherer
from LargeDataCleaner import LargeDataCleaner
from LogLevel import LogLevel
from Logger import Logger
from MaliciousDataDetection.MDataCleaner import MDataCleaner
from EasyMLLib.CSVWriter import CSVWriter


CLASSIFIER_INSTANCES = [RandomForestClassifier(
), DecisionTreeClassifier(), KNeighborsClassifier()]

LOG_NAME = "LargeDataPipelineGathererAndCleanerWithCustomXYUserDist"

CSV_COLUMNS = ["Model", "Total_Train_Time",
               "Total_Train_Sample_Size", "Total_Test_Sample_Size", "Train_Time_Per_Sample", "Prediction_Train_Set_Time_Per_Sample", "Prediction_Test_Set_Time_Per_Sample",
               "train_accuracy", "train_precision", "train_recall", "train_f1",
               "test_accuracy", "test_precision", "test_recall", "test_f1"]

CSV_FORMAT = {CSV_COLUMNS[i]: i for i in range(len(CSV_COLUMNS))}

# will be relied on by other methods to gather large data and filter it to a small area
class LargeDataPipelineGathererAndCleanerWithCustomXYUserDist:


    def __init__(self, logger=Logger(LOG_NAME), csvWriter=CSVWriter(f"{LOG_NAME}.csv", CSV_COLUMNS, outputpath=os.path.join("data", "classifierdata", "results")), LOG_NAME=LOG_NAME):
        self.logger = logger
        self.csvWriter = csvWriter
        self.LOG_NAME = LOG_NAME

    def write_entire_row(self, dict):
        row = [" "]*len(CSV_COLUMNS)
        # Writing each variable to the row
        for d in dict:
            row[CSV_FORMAT[d]] = dict[d]

        self.csvWriter.addRow(row)
        return self

    def run(self, cleanFunc=DataCleaner.clean_data_with_OTHER_FUNC_Then_XY, otherCleanFunc=DataCleaner.clean_data_with_timestamps, filterFunction=LargeDataCleaner.within_range, max_dist=100, x_col="x_pos", y_col="y_pos", x_pos=-105.1159611, y_pos=41.0982327, lines_per_file=100000):

        # makes standard data gatherer
        self.dg = DataGatherer(filepath="data/data.csv", subsectionpath=f"data/classifierdata/sub/{self.LOG_NAME}/subsection.csv", splitfilespath=f"data/classifierdata/split/{self.LOG_NAME}/split/", logger=self.logger.newPrefix("DataGatherer"))
        # chunks data into smaller files
        self.dg.split_large_data(lines_per_file=lines_per_file)

        # cleaning the data in the split files
        self.dc = LargeDataCleaner(splitfilespath=f"data/classifierdata/split/{self.LOG_NAME}/split/", cleanedsplitfilespath=f"data/classifierdata/clean/{self.LOG_NAME}/split/", combinedcleandatapath=f"data/classifierdata/clean/{self.LOG_NAME}/combined.csv", logger=self.logger.newPrefix("LargeDataCleaner"))
        # cleans the data
        # the cleanFunc actually adds the x and y columns as a offset from a constant lat-long as specified by x_pos and y_pos
        # the otherCleanFunc actually does the cleaning part. The otherCleanFunc is called first and then
        # we convert the X and Y columns to be a const offset from the x_pos and y_pos
        self.dc.clean_data(filterFunction=filterFunction, cleanFunc=cleanFunc, otherCleanFunction=otherCleanFunc, max_dist=max_dist, x_col=x_col, y_col=y_col, x_pos=x_pos, y_pos=y_pos)
        # combining the data into combinedcleandatapath
        self.dc.combine_data()
        return self



    def getNRows(self, n):
        # read from combined data
        return self.dc.getNRows(n, dtypes=LargeDataCleaner.default_dtypes)


if __name__ == "__main__":
    mcplu = LargeDataPipelineGathererAndCleanerWithCustomXYUserDist()
    mcplu.run()
