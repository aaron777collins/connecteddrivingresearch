# Seperates the isAttacker column from the data (and cleans it) and returns the cleaned data and the isAttacker column
import os
from Logger import Logger

import pandas as pd
from sklearn.model_selection import train_test_split

import DataGatherer

COLUMNS=[
    # "metadata_generatedAt", "metadata_recordType", "metadata_serialId_streamId",
    #  "metadata_serialId_bundleSize", "metadata_serialId_bundleId", "metadata_serialId_recordId",
    #  "metadata_serialId_serialNumber", "metadata_receivedAt",
    #  "metadata_rmd_elevation", "metadata_rmd_heading","metadata_rmd_latitude", "metadata_rmd_longitude", "metadata_rmd_speed",
    #  "metadata_rmd_rxSource","metadata_bsmSource",
        "coreData_id", # "coreData_position_lat", "coreData_position_long",
        "coreData_elevation", "coreData_accelset_accelYaw","coreData_speed", "coreData_heading", "x_pos", "y_pos", "isAttacker"]

# COLUMNS_EXT=[
# # "metadata_generatedAt", "metadata_recordType", "metadata_serialId_streamId",
# #  "metadata_serialId_bundleSize", "metadata_serialId_bundleId", "metadata_serialId_recordId",
# #  "metadata_serialId_serialNumber", "metadata_receivedAt",
# #  "metadata_rmd_elevation", "metadata_rmd_heading","metadata_rmd_latitude", "metadata_rmd_longitude", "metadata_rmd_speed",
# #  "metadata_rmd_rxSource","metadata_bsmSource",
#     "coreData_id", "coreData_position_lat", "coreData_position_long",
#     "coreData_secMark", "accuracy_semiMajor", "accuracy_semiMinor",
#     "coreData_elevation", "coreData_accelset_accelYaw","coreData_speed", "coreData_heading", "x_pos", "y_pos", "isAttacker"]

# COLUMNS_EXT_WITH_TIMESTAMPS=[
# # "metadata_generatedAt", "metadata_recordType", "metadata_serialId_streamId",
# #  "metadata_serialId_bundleSize", "metadata_serialId_bundleId", "metadata_serialId_recordId",
# #  "metadata_serialId_serialNumber", "metadata_receivedAt",
# #  "metadata_rmd_elevation", "metadata_rmd_heading","metadata_rmd_latitude", "metadata_rmd_longitude", "metadata_rmd_speed",
# #  "metadata_rmd_rxSource","metadata_bsmSource",
#     "coreData_id", "coreData_position_lat", "coreData_position_long",
#     "coreData_secMark", "accuracy_semiMajor", "accuracy_semiMinor",
#     "month", "day", "year", "hour", "minute", "second", "pm",
#     "coreData_elevation", "coreData_accelset_accelYaw","coreData_speed", "coreData_heading", "x_pos", "y_pos", "isAttacker"]
class MDataCleaner:
    def __init__(self, data, columns=COLUMNS, cleandatapath="data/classifierdata/Mclean/clean.csv", logger=Logger("MDataCleaner")):
        self.data = data
        self.cleandatapath=cleandatapath
        self.logger = logger
        self.columns = columns

    def clean_data(self):
        os.makedirs(os.path.dirname(self.cleandatapath), exist_ok=True)

        # check if the cleaned data already exists
        if os.path.isfile(self.cleandatapath):
            self.logger.log("Cleaned data already exists. Reading from file.")
            self.cleaned_data = pd.read_csv(self.cleandatapath)
            return self

        def convert_large_hex_str_to_hex(num):
            # account for str with decimal point
            if "." in num:
                num = num.split(".")[0]
            # convert to hex
            num = int(num, 16)

            return num

        # clean the data
        self.logger.log("Cleaning data...")
        self.cleaned_data = self.data[self.columns]
        # convert the coreData_id from hexadecimal to decimal
        self.cleaned_data["coreData_id"] = self.cleaned_data["coreData_id"].map(lambda x: convert_large_hex_str_to_hex(x))
        self.cleaned_data.to_csv(self.cleandatapath, index=False)
        return self

    def get_cleaned_data(self):
        return self.cleaned_data

    # COMMENTED OUT because we don't need to split the data into train and test sets
    # I am going to split the data itself into train and test sets
    # def train_test_split(self, test_size=0.2):
    #     self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.cleaned_data.drop("isAttacker"), self.cleaned_data["isAttacker"], test_size=test_size)
    #     return self

    # def get_train_test_split(self):
    #     return self.X_train, self.X_test, self.y_train, self.y_test





