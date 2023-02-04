# Create a class Logger to log the info of the program with an elevation level, prefix and message.
import os
from LogLevel import LogLevel
from datetime import datetime

class Logger:

    def __init__(self, prefix, elevation = LogLevel.INFO, logpath = None):
        self.logpath = logpath
        if self.logpath == None:
            self.logpath = f"data/log/{prefix}-{elevation}.txt"
        self.elevation = elevation
        self.prefix = prefix

    def log(self, message):
        # print to console and append to file
        string = f"{self.elevation} {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} {self.prefix}: {str(message)}"
        print(string)
        os.makedirs(os.path.dirname(self.logpath), exist_ok=True)
        with open(self.logpath, "a") as f:
            f.write(string + "\n")

