import pandas as pd
import os.path as path
import os
from Logger import Logger
from itertools import islice

class DataGatherer:
    def __init__(self, numrows=10000, filepath="data/data.csv", subsectionpath="data/sub/subsection.csv", splitfilespath="data/split/", logger=Logger("DataGatherer")):
        self.numrows = numrows
        self.filepath = filepath
        self.subsectionpath = subsectionpath
        self.splitfilespath = splitfilespath
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

    def split_large_data(self, lines_per_file=100000) -> pd.DataFrame:

        if path.isfile(self.splitfilespath + "split0.csv"):
            self.logger.log("Found split files! Skipping regeneration.")
            return self

        os.makedirs(path.dirname(self.splitfilespath), exist_ok=True)
        # loop until we have all the data
        # create new file for each 1000 lines

        with open(self.filepath, "r") as f:
            header = next(f)  # read the header from the first line of the file
            for i, line in enumerate(f):
                if i % lines_per_file == 0:
                    self.logger.log(f"Creating new file for line {i}")
                    if i != 0:
                        file.close()
                    file = open(self.splitfilespath + f"split{i}.csv", "w")
                    file.write(header)  # write the header at the beginning of the file
                file.write(line)
        file.close()

        return self


if __name__ == "__main__":
    dg = DataGatherer()
    print(dg.gather_data().head(5))
