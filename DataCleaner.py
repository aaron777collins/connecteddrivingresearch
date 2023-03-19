import os

import pandas as pd
from DataConverter import DataConverter
from DataGatherer import DataGatherer
from Logger import Logger
from sklearn.model_selection import train_test_split

COLUMNS=["metadata_generatedAt", "metadata_recordType", "metadata_serialId_streamId",
            "metadata_serialId_bundleSize", "metadata_serialId_bundleId", "metadata_serialId_recordId",
            "metadata_serialId_serialNumber", "metadata_receivedAt",
            #  "metadata_rmd_elevation", "metadata_rmd_heading","metadata_rmd_latitude", "metadata_rmd_longitude", "metadata_rmd_speed",
            #  "metadata_rmd_rxSource","metadata_bsmSource",
            "coreData_id", "coreData_secMark", "coreData_position_lat", "coreData_position_long",
            "coreData_accuracy_semiMajor", "coreData_accuracy_semiMinor",
            "coreData_elevation", "coreData_accelset_accelYaw","coreData_speed", "coreData_heading", "coreData_position"]


class DataCleaner:
    def __init__(self, data=None, columns=COLUMNS, cleandatapath="data/clean/clean.csv", logger=Logger("DataCleaner")):
        self.data = data
        self.columns = columns
        self.cleandatapath=cleandatapath
        self.logger = logger
        if not isinstance(self.data, pd.DataFrame):
            self.logger.log("No data specified. Defaulting to data/raw/subsection.csv")
            self.data = DataGatherer().gather_data()

    def clean_data(self):
        os.makedirs(os.path.dirname(self.cleandatapath), exist_ok=True)
        self.cleaned_data = self.data[self.columns]
        self.cleaned_data = self.cleaned_data.dropna()
        self.cleaned_data["x_pos"] = self.cleaned_data["coreData_position"].map(lambda x: DataConverter.point_to_tuple(x)[0])
        self.cleaned_data["y_pos"] = self.cleaned_data["coreData_position"].map(lambda x: DataConverter.point_to_tuple(x)[1])
        self.cleaned_data.drop(columns=["coreData_position"], inplace=True)
        self.cleaned_data.to_csv(self.cleandatapath, index=False)
        return self

    def clean_data_with_timestamps(self):
        os.makedirs(os.path.dirname(self.cleandatapath), exist_ok=True)
        self.cleaned_data = self.data[self.columns]
        self.cleaned_data = self.cleaned_data.dropna()
        self.cleaned_data["x_pos"] = self.cleaned_data["coreData_position"].map(lambda x: DataConverter.point_to_tuple(x)[0])
        self.cleaned_data["y_pos"] = self.cleaned_data["coreData_position"].map(lambda x: DataConverter.point_to_tuple(x)[1])
        # of format "07/31/2019 12:41:59 PM"
        # convert to datetime
        self.cleaned_data["metadata_generatedAt"] = pd.to_datetime(self.cleaned_data["metadata_generatedAt"], format="%m/%d/%Y %I:%M:%S %p")
        self.cleaned_data["month"] = self.cleaned_data["metadata_generatedAt"].map(lambda x: x.month)
        self.cleaned_data["day"] = self.cleaned_data["metadata_generatedAt"].map(lambda x: x.day)
        self.cleaned_data["year"] = self.cleaned_data["metadata_generatedAt"].map(lambda x: x.year)
        self.cleaned_data["hour"] = self.cleaned_data["metadata_generatedAt"].map(lambda x: x.hour)
        self.cleaned_data["minute"] = self.cleaned_data["metadata_generatedAt"].map(lambda x: x.minute)
        self.cleaned_data["second"] = self.cleaned_data["metadata_generatedAt"].map(lambda x: x.second)
        self.cleaned_data["pm"] = self.cleaned_data["metadata_generatedAt"].map(lambda x: 0 if x.hour < 12 else 1) # 0 if am, 1 if pm

        self.cleaned_data["metadata_generatedAt"]
        self.cleaned_data.drop(columns=["coreData_position"], inplace=True)
        self.cleaned_data.to_csv(self.cleandatapath, index=False)
        return self

    def getCleanedData(self):
        return self.cleaned_data


if __name__ == "__main__":
    cleaner = DataCleaner()
    data = cleaner.clean_data()
    cleaner.logger.log(data.head(5))


