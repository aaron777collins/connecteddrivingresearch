# prepares the data, trains the pipelines and classifies the data based on the classifiers

from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from DataAttacker import DataAttacker
from DataCleaner import DataCleaner
from DataGatherer import DataGatherer
from MaliciousDataDetection.MDataClassifier import MDataClassifier
from MaliciousDataDetection.MDataCleaner import MDataCleaner

CLASSIFIER_INSTANCES = [RandomForestClassifier(
), DecisionTreeClassifier(), KNeighborsClassifier()]


class MClassifierPipeline:
    def __init__(self, train_X, train_Y, test_X, test_Y, classifier_instances=CLASSIFIER_INSTANCES):

        # create MDataClassifier instances for each classifier
        self.classifiers = []
        for classifier_instance in classifier_instances:
            self.classifiers.append(
                MDataClassifier(classifier_instance, train_X, train_Y, test_X, test_Y))

    def train(self, data):
        for mClassifier in self.classifiers:
            mClassifier.train()

    def test(self, data):
        for mClassifier in self.classifiers:
            mClassifier.classify()

    # gets accuracy, precision, recall and f1 score for each classifier and associates it with the classifier
    def calc_classifier_results(self):
        self.results = []

        for mClassifier in self.classifiers:
            self.results.append((mClassifier, mClassifier.get_results()))

        return self

    def get_classifier_results(self):
        return self.results


if __name__ == "__main__":
    # Getting the first 20000 rows of data and splitting it into train and test sets (10000 rows each)
    dg = DataGatherer(numrows=20000, filepath="data/data.csv", subsectionpath="data/classifierdata/sub/subsection.csv")

    # getting the data (as dataframe)
    data: DataFrame = dg.gather_data()

    # splitting into train and test sets
    train = data.iloc[:10000].copy()
    test = data.iloc[10000:20000].copy()

    # cleaning/adding attackers to the data
    train = DataAttacker(DataCleaner(train, cleandatapath="data/classifierdata/clean/clean_train.csv").clean_data().getCleanedData(),
                         modified_data_path="data/classifierdata/modified/modified_train.csv", SEED=24).add_attackers().add_attacks_positional_offset_const().getData()
    test = DataAttacker(DataCleaner(test, cleandatapath="data/classifierdata/clean/clean_test.csv").clean_data().getCleanedData(),
                        modified_data_path="data/classifierdata/modified/modified_test.csv", SEED=48).add_attackers().add_attacks_positional_offset_const().getData()

    # Cleaning it for the malicious data detection
    mdcleaner_train = MDataCleaner(train, cleandatapath="data/classifierdata/Mclean/clean_train.csv")
    mdcleaner_test = MDataCleaner(test, cleandatapath="data/classifierdata/Mclean/clean_test.csv")
    m_train = mdcleaner_train.clean_data().get_cleaned_data()
    m_test = mdcleaner_test.clean_data().get_cleaned_data()

    # splitting into X and Y
    attacker_col_name = "isAttacker"
    train_X = m_train.drop(columns=[attacker_col_name], axis=1)
    train_Y = m_train[attacker_col_name]
    test_X = m_test.drop(columns=[attacker_col_name], axis=1)
    test_Y = m_test[attacker_col_name]

    # training the classifiers
    mcp = MClassifierPipeline(train_X, train_Y, test_X, test_Y)

    mcp.train(train)
    mcp.test(test)

    # getting the results
    results = mcp.calc_classifier_results().get_classifier_results()

    # printing the results
    for mclassifier, result in results:
        print(mclassifier)
        print("Accuracy: ", result[0])
        print("Precision: ", result[1])
        print("Recall: ", result[2])
        print("F1: ", result[3])
        # printing the elapsed training and prediction time
        print("Elapsed Training Time: ", mclassifier.elapsed_train_time)
        print("Elapsed Prediction Time: ", mclassifier.elapsed_prediction_time)
