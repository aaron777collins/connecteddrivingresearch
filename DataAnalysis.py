# finding out how many unique IDs there are for the "coreData_id" column (using Dataframes)
from DataCleaner import DataCleaner


class DataAnalysis:
    def __init__(self, data):
        self.data = data

    def getUniqueIDs(self):
        return self.data.coreData_id.unique()

    def getUniqueIDsCount(self):
        return len(self.getUniqueIDs())

if __name__ == "__main__":
    data = DataCleaner().clean_data()
    analyzer  = DataAnalysis(data)
    print(f"Num Unique IDs: {analyzer.getUniqueIDsCount()}")
    # Result: Num Unique IDs: 32
    # I guess there isn't a ton of cars in the first 3 hours lol
