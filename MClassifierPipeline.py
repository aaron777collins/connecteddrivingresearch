# prepares the data, trains the pipelines and classifies the data based on the classifiers

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from Logger import Logger
from MaliciousDataDetection.MDataClassifier import MDataClassifier

CLASSIFIER_INSTANCES = [RandomForestClassifier(
), DecisionTreeClassifier(), KNeighborsClassifier()]


class MClassifierPipeline:
    def __init__(self, train_X, train_Y, test_X, test_Y, classifier_instances=CLASSIFIER_INSTANCES, logger=Logger("MClassifierPipeline")):

        self.logger = logger
        self.classifiers_and_confusion_matrices: list[tuple[MDataClassifier, list[list[float]]]] = []

        # create MDataClassifier instances for each classifier
        self.classifiers: list[MDataClassifier] = []
        for classifier_instance in classifier_instances:
            self.classifiers.append(
                MDataClassifier(classifier_instance, train_X, train_Y, test_X, test_Y, logger=self.logger.newPrefix("MDataClassifier-"+classifier_instance.__class__.__name__)))


    def train(self):
        for mClassifier in self.classifiers:
            mClassifier.train()

    def test(self):
        for mClassifier in self.classifiers:
            mClassifier.classify_train()
            mClassifier.classify()

    # gets accuracy, precision, recall and f1 score for each classifier and associates it with the classifier
    def calc_classifier_results(self):
        self.results = []

        for mClassifier in self.classifiers:
            self.results.append((mClassifier, mClassifier.get_train_results(), mClassifier.get_results()))

        return self

    def get_classifier_results(self):
        return self.results

    def calculate_classifiers_and_confusion_matrices(self):
        self.classifiers_and_confusion_matrices: list[tuple[MDataClassifier, list[list[float]]]] = []

        for mClassifier in self.classifiers:
            self.classifiers_and_confusion_matrices.append((mClassifier, mClassifier.get_confusion_matrix()))

        return self

    def get_classifiers_and_confusion_matrices(self):
        return self.classifiers_and_confusion_matrices

    # path should be the path to store the plot (ending without a slash)
    # i.e. f"data/classifierdata/results/plots/{LOG_NAME}/confusion_matrices"
    def plot_confusion_matrices(self, path, labels=["Regular", "Malicious"]):
        for mClassifier, confusion_matrix in self.classifiers_and_confusion_matrices:
            mClassifier.plot_confusion_matrix(confusion_matrix, path + "/" + mClassifier.classifier.__class__.__name__ + ".png", labels=labels)
