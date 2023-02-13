import os
from DataConverter import DataConverter
from DataGatherer import DataGatherer
from Logger import Logger

COLUMNS=["metadata_generatedAt", "metadata_recordType", "metadata_serialId_streamId",
         "metadata_serialId_bundleSize", "metadata_serialId_bundleId", "metadata_serialId_recordId",
         "metadata_serialId_serialNumber", "metadata_receivedAt",
        #  "metadata_rmd_elevation", "metadata_rmd_heading","metadata_rmd_latitude", "metadata_rmd_longitude", "metadata_rmd_speed",
        #  "metadata_rmd_rxSource","metadata_bsmSource",
         "coreData_id", "coreData_position_lat", "coreData_position_long",
         "coreData_elevation", "coreData_accelset_accelYaw","coreData_speed", "coreData_heading", "coreData_position"]

class DataCleaner:
    def __init__(self, data=None, columns=COLUMNS, cleandatapath="data/clean/clean.csv"):
        self.data = data
        self.columns = columns
        self.cleandatapath=cleandatapath
        self.logger = Logger("DataCleaner")
        if self.data == None:
            self.logger.log("No data specified. Defaulting to data/raw/subsection.csv")
            self.data = DataGatherer().gather_data()

    def clean_data(self):
        os.makedirs(os.path.dirname(self.cleandatapath), exist_ok=True)
        self.clean_data = self.data[self.columns]
        self.clean_data = self.clean_data.dropna()
        self.clean_data["x_pos"] = self.clean_data["coreData_position"].map(lambda x: DataConverter.point_to_tuple(x)[0])
        self.clean_data["y_pos"] = self.clean_data["coreData_position"].map(lambda x: DataConverter.point_to_tuple(x)[1])
        self.clean_data.drop(columns=["coreData_position"], inplace=True)
        self.clean_data.to_csv(self.cleandatapath, index=False)
        return self.clean_data

if __name__ == "__main__":
    print(DataCleaner().clean_data().head(5))

