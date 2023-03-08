# finding out how many unique IDs there are for the "coreData_id" column (using Dataframes)
from DataCleaner import DataCleaner
from Logger import Logger


class DataAnalysis:
    def __init__(self, data, logger=Logger("DataAnalysis")):
        self.data = data
        self.logger = logger

    def getUniqueIDs(self):
        return self.data.coreData_id.unique()

    def getUniqueIDsCount(self):
        return len(self.getUniqueIDs())

if __name__ == "__main__":
    dc = DataCleaner()
    data = dc.clean_data()
    analyzer  = DataAnalysis(data)
    dc.logger.log(f"Num Unique IDs: {analyzer.getUniqueIDsCount()}")
    # Result: Num Unique IDs: 32
    # I guess there isn't a ton of cars in the first 3 hours lol
