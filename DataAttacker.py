import os
import random
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from DataCleaner import DataCleaner
from Logger import Logger
from MathHelper import MathHelper



class DataAttacker:
    def __init__(self, data, modified_data_path="data/modified/modified.csv", SEED=42, logger=Logger("DataAttacker"), isXYCoords=False, pos_lat_col = "y_pos", pos_long_col = "x_pos", x_col = "x_pos", y_col = "y_pos"):
        self.data = data
        self.modified_data_path = modified_data_path
        self.SEED = SEED
        self.logger = logger
        self.isXYCoords = isXYCoords
        self.pos_lat_col = pos_lat_col
        self.pos_long_col = pos_long_col
        self.x_col = x_col
        self.y_col = y_col

    # Must be run after the data is clean to get a proper result.
    # This function returns the list of unique IDs from the coreData_id column
    def getUniqueIDsFromCleanData(self):
        return self.data.coreData_id.unique()

    # returns the data with the new attackers
    # It requires having the modified_data_path exist and the uniqueIDs column
    def add_attackers(self, attack_ratio=0.05):

        os.makedirs(os.path.dirname(self.modified_data_path), exist_ok=True)

        uniqueIDs = self.getUniqueIDsFromCleanData()

        # Splits the data into the regular cars and the new chosen attackers (5% attackers)
        regular, attackers = train_test_split(uniqueIDs, test_size=attack_ratio, random_state=self.SEED)

        # Adds a column called isAttacker with 0 if they are regular and 1 if they are in the attackers list
        self.data["isAttacker"] = self.data.coreData_id.apply(lambda x: 1 if x in attackers else 0)

        # ensure that the path exists
        os.makedirs(os.path.dirname(self.modified_data_path), exist_ok=True)

        # saving the data
        self.data.to_csv(self.modified_data_path, index=False)

        return self

    # returns the data with the new attackers
    # It requires having the modified_data_path exist and the uniqueIDs column
    # this one is random and doesn't specify the attackers by ID
    def add_rand_attackers(self, attack_ratio=0.05):

        # Adds a column called isAttacker with 0 if they are regular and 1 if they are an attacker
        # attackers are randomly chosen for each row by the attack_ratio
        self.data["isAttacker"] = self.data.coreData_id.apply(lambda x: 1 if random.random() <= attack_ratio else 0)

        # ensure that the path exists
        os.makedirs(os.path.dirname(self.modified_data_path), exist_ok=True)

        # saving the data
        self.data.to_csv(self.modified_data_path, index=False)

        return self

    # adds a constant positional offset attack to the core data
    # Affected columns: coreData_position_lat,coreData_position_long
    # direction_angle is north at 0 (- is to the west, + is to the east)
    def add_attacks_positional_offset_const(self, direction_angle=45, distance_meters=50):
        # Applying the attack to the data when the isAttacker column is 1

        # Checking if the row is an attacker
        # applying the attack function to each row
        self.data = self.data.apply(lambda row: self.positional_offset_const_attack(row, direction_angle, distance_meters), axis=1)

        return self

    def positional_offset_const_attack(self, row, direction_angle, distance_meters):
        # Checking if the row is not an attacker
        if row["isAttacker"] == 0:
            return row # if not an attacker, return the row as is


        # checking if the coordinates are in XY format
        if self.isXYCoords:
            # add attack with XY coordinates
            # calculating positional offset based on direction angle and distance
            newX, newY = MathHelper.direction_and_dist_to_XY(row[self.x_col], row[self.y_col], direction_angle, distance_meters)

            row[self.x_col] = newX
            row[self.y_col] = newY
        else:
            # calculating positional offset based on direction angle and distance
            newLat, newLong = MathHelper.direction_and_dist_to_lat_long_offset(row[self.pos_lat_col], row[self.pos_long_col], direction_angle, distance_meters)
            # self.logger.log("Before:", row[self.pos_lat_col], row[self.pos_long_col])
            row[self.pos_lat_col] = newLat
            row[self.pos_long_col] = newLong
            # self.logger.log("After:", row[self.pos_lat_col], row[self.pos_long_col])
        return row

    def add_attacks_positional_offset_rand(self, min_dist=25, max_dist = 250):
        # similar to the const attack, but the distance and direction is random

        self.data = self.data.apply(lambda row: self.positional_offset_rand_attack(row, min_dist, max_dist), axis=1)

        return self

    def positional_offset_rand_attack(self, row, min_dist, max_dist):
        # checking if the row is not an attacker
        if row["isAttacker"] == 0:
            return row # if not an attacker, return the row as is

        if self.isXYCoords:
            # add attack with XY coordinates
            # calculating the positional offset based on a random direction and distance
            newX, newY = MathHelper.direction_and_dist_to_XY(row[self.x_col], row[self.y_col], random.randint(0, 360), random.randint(min_dist, max_dist))

            row[self.x_col] = newX
            row[self.y_col] = newY

        else:

            # calculating the positional offset based on a random direction and distance
            newLat, newLong = MathHelper.direction_and_dist_to_lat_long_offset(row[self.pos_lat_col], row[self.pos_long_col], random.randint(0, 360), random.randint(min_dist, max_dist))

            row[self.pos_lat_col] = newLat
            row[self.pos_long_col] = newLong

        return row


    def getData(self):
        return self.data

if __name__ == "__main__":
    cleanData = DataCleaner().clean_data().getCleanedData()
    da = DataAttacker(cleanData)
    modified_data = da.add_attackers().add_attacks_positional_offset_const().getData()
    da.logger.log(modified_data.head(5))

