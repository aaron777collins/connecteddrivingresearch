# MClassifierPipeline-Const-50-offset

import os
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from DataAttacker import DataAttacker
from DataCleaner import DataCleaner
from DataGatherer import DataGatherer
from LogLevel import LogLevel
from Logger import Logger
from MaliciousDataDetection.MClassifierPipeline import MClassifierPipeline
from MaliciousDataDetection.MDataCleaner import MDataCleaner
from EasyMLLib.CSVWriter import CSVWriter


CLASSIFIER_INSTANCES = [RandomForestClassifier(
), DecisionTreeClassifier(), KNeighborsClassifier()]

LOG_NAME = "MClassifierPipelineUserRandOffset20To250"

CSV_COLUMNS = ["Model", "Total_Train_Time",
               "Total_Train_Sample_Size", "Total_Test_Sample_Size", "Train_Time_Per_Sample", "Prediction_Train_Set_Time_Per_Sample", "Prediction_Test_Set_Time_Per_Sample",
               "train_accuracy", "train_precision", "train_recall", "train_f1",
               "test_accuracy", "test_precision", "test_recall", "test_f1"]

CSV_FORMAT = {CSV_COLUMNS[i]: i for i in range(len(CSV_COLUMNS))}

class MClassifierPipelineUserRandOffset20To250:


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
        # main method
        # Getting the first 20000 rows of data and splitting it into train and test sets (10000 rows each)
        dg = DataGatherer(numrows=20000, filepath="data/data.csv", subsectionpath=f"data/classifierdata/sub/{LOG_NAME}/subsection.csv", logger=self.logger.newPrefix("DataGatherer"))

        # getting the data (as dataframe)
        data: DataFrame = dg.gather_data()

        # splitting into train and test sets
        train = data.iloc[:10000].copy()
        test = data.iloc[10000:20000].copy()

        # cleaning/adding attackers to the data
        train = DataAttacker(DataCleaner(train, cleandatapath=f"data/classifierdata/clean/{LOG_NAME}/clean_train.csv", logger=self.logger.newPrefix("DataCleaner")).clean_data().getCleanedData(),
                            modified_data_path=f"data/classifierdata/modified/{LOG_NAME}/modified_train.csv", SEED=24, logger=self.logger.newPrefix("DataAttacker")).add_attackers().add_attacks_positional_offset_rand().getData()
        test = DataAttacker(DataCleaner(test, cleandatapath=f"data/classifierdata/clean/{LOG_NAME}/clean_test.csv", logger=self.logger.newPrefix("DataCleaner")).clean_data().getCleanedData(),
                            modified_data_path=f"data/classifierdata/modified/{LOG_NAME}/modified_test.csv", SEED=48, logger=self.logger.newPrefix("DataAttacker")).add_attackers().add_attacks_positional_offset_rand().getData()

        # Cleaning it for the malicious data detection
        mdcleaner_train = MDataCleaner(train, cleandatapath=f"data/classifierdata/Mclean/{LOG_NAME}/clean_train.csv", logger=self.logger.newPrefix("MDataCleaner"))
        mdcleaner_test = MDataCleaner(test, cleandatapath=f"data/classifierdata/Mclean/{LOG_NAME}/clean_test.csv", logger=self.logger.newPrefix("MDataCleaner"))
        m_train = mdcleaner_train.clean_data().get_cleaned_data()
        m_test = mdcleaner_test.clean_data().get_cleaned_data()

        # splitting into X and Y
        attacker_col_name = "isAttacker"
        train_X = m_train.drop(columns=[attacker_col_name], axis=1)
        train_Y = m_train[attacker_col_name]
        test_X = m_test.drop(columns=[attacker_col_name], axis=1)
        test_Y = m_test[attacker_col_name]

        # training the classifiers
        mcp = MClassifierPipeline(train_X, train_Y, test_X, test_Y, classifier_instances=CLASSIFIER_INSTANCES, logger=self.logger.newPrefix("MClassifierPipeline"))

        mcp.train()
        mcp.test()

        # getting the results
        results = mcp.calc_classifier_results().get_classifier_results()

        # printing the results
        for mclassifier, train_result, result in results:
            mcp.logger.log(mclassifier)
            mcp.logger.log("Train Set Results:")
            mcp.logger.log("Accuracy: ", train_result[0])
            mcp.logger.log("Precision: ", train_result[1])
            mcp.logger.log("Recall: ", train_result[2])
            mcp.logger.log("F1: ", train_result[3])
            mcp.logger.log("Test Set Results:")
            mcp.logger.log("Accuracy: ", result[0])
            mcp.logger.log("Precision: ", result[1])
            mcp.logger.log("Recall: ", result[2])
            mcp.logger.log("F1: ", result[3])
            # printing the elapsed training and prediction time
            mcp.logger.log("Elapsed Training Time: ", mclassifier.elapsed_train_time)
            mcp.logger.log("Elapsed Prediction Time: ", mclassifier.elapsed_prediction_time)

            mcp.logger.log("Writing to CSV...")

            # writing entire row to csv
            # columns: "Model", "Total_Train_Time",
            #    "Total_Train_Sample_Size", "Total_Test_Sample_Size", "Train_Time_Per_Sample", "Prediction_Train_Set_Time_Per_Sample", "Prediction_Test_Set_Time_Per_Sample",
            #    "train_accuracy", "train_precision", "train_recall", "train_f1",
            #    "test_accuracy", "test_precision", "test_recall", "test_f1"

            csvrowdata = {
                "Model": mclassifier.classifier.__class__.__name__,
                "Total_Train_Time": mclassifier.elapsed_train_time,
                "Total_Train_Sample_Size": len(train_X), # train and test have the same number of samples
                "Total_Test_Sample_Size": len(test_X), # train and test have the same number of samples
                "Train_Time_Per_Sample": mclassifier.elapsed_train_time/len(train_X),
                "Prediction_Train_Set_Time_Per_Sample": mclassifier.elapsed_prediction_train_time/len(train_X),
                "Prediction_Test_Set_Time_Per_Sample": mclassifier.elapsed_prediction_time/len(test_X),
                "train_accuracy": train_result[0],
                "train_precision": train_result[1],
                "train_recall": train_result[2],
                "train_f1": train_result[3],
                "test_accuracy": result[0],
                "test_precision": result[1],
                "test_recall": result[2],
                "test_f1": result[3]}
            self.write_entire_row(csvrowdata)
        # calculating confusion matrices and storing them
        mcp.logger.log("Calculating confusion matrices and storing...")
        # path to store the confusion matrices
        plotpath = f"data/classifierdata/results/plots/{LOG_NAME}/confusion_matrices"
        mcp.calculate_classifiers_and_confusion_matrices().plot_confusion_matrices(plotpath)


if __name__ == "__main__":
    mcplu = MClassifierPipelineUserRandOffset20To250()
    mcplu.run()
