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

LOG_NAME = "LargeDataPipelineGathererAndCleanerUser100MDist"

CSV_COLUMNS = ["Model", "Total_Train_Time",
               "Total_Train_Sample_Size", "Total_Test_Sample_Size", "Train_Time_Per_Sample", "Prediction_Train_Set_Time_Per_Sample", "Prediction_Test_Set_Time_Per_Sample",
               "train_accuracy", "train_precision", "train_recall", "train_f1",
               "test_accuracy", "test_precision", "test_recall", "test_f1"]

CSV_FORMAT = {CSV_COLUMNS[i]: i for i in range(len(CSV_COLUMNS))}

# will be relied on by other methods to gather large data and filter it to a small area
class LargeDataPipelineGathererAndCleanerUser100MDist:


    def __init__(self, logger=Logger(LOG_NAME), csvWriter=CSVWriter(f"{LOG_NAME}.csv", CSV_COLUMNS, outputpath=os.path.join("data", "classifierdata", "results"))):
        self.logger = logger
        self.csvWriter = csvWriter

    def write_entire_row(self, dict):
        row = [" "]*len(CSV_COLUMNS)
        # Writing each variable to the row
        for d in dict:
            row[CSV_FORMAT[d]] = dict[d]

        self.csvWriter.addRow(row)

    def run(self):

        dg = DataGatherer(filepath="data/data.csv", subsectionpath=f"data/classifierdata/sub/{LOG_NAME}/subsection.csv", splitfilespath=f"data/classifierdata/split/{LOG_NAME}/split/", logger=self.logger.newPrefix("DataGatherer"))
        dg.split_large_data(lines_per_file=100000)

        dc = LargeDataCleaner(splitfilespath=f"data/classifierdata/split/{LOG_NAME}/split/", cleanedsplitfilespath=f"data/classifierdata/clean/{LOG_NAME}/split/", combinedcleandatapath=f"data/classifierdata/clean/{LOG_NAME}/combined.csv", logger=self.logger.newPrefix("LargeDataCleaner"))
        dc.clean_data(filterFunction=dc.within_range, cleanFunc=DataCleaner.clean_data_with_timestamps, max_dist=100, x_col="x_pos", y_col="y_pos", x_pos=-105.1159611, y_pos=41.0982327)
        dc.combine_data()


if __name__ == "__main__":
    mcplu = LargeDataPipelineGathererAndCleanerUser100MDist()
    mcplu.run()
