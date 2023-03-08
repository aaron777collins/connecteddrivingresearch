import pandas as pd
import os.path as path
import os
from Logger import Logger

class DataGatherer:
    def __init__(self, numrows=10000, filepath="data/data.csv", subsectionpath="data/sub/subsection.csv", logger=Logger("DataGatherer")):
        self.numrows = numrows
        self.filepath = filepath
        self.subsectionpath = subsectionpath
        self.logger = logger

    def gather_data(self) -> pd.DataFrame:

        os.makedirs(path.dirname(self.subsectionpath), exist_ok=True)
        if path.isfile(self.subsectionpath):
            self.logger.log("Found file! Reading from subsection.")
            self.data = pd.read_csv(self.subsectionpath)
            return self.data
        else:
            self.logger.log("Didn't find file. Reading from full dataset.")
            self.data = pd.read_csv(self.filepath, nrows=self.numrows)
            self.data.to_csv(self.subsectionpath, index=False)
            return self.data

if __name__ == "__main__":
    dg = DataGatherer()
    print(dg.gather_data().head(5))
