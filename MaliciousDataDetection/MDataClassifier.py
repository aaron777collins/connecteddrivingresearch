import time

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os

from Logger import Logger

# Creates uses the data to classify whether or not a vehicle is an attacker
# Takes in a sklearn classifier and the data to classify
class MDataClassifier:
    def __init__(self, classifier, train_X, train_Y, test_X, test_Y, logger=Logger("MDataClassifier")):
        self.classifier = classifier
        self.train_X = train_X
        self.train_Y = train_Y
        self.test_X = test_X
        self.test_Y = test_Y
        self.elapsed_train_time = -1
        self.elapsed_prediction_time = -1
        self.elapsed_prediction_train_time = -1
        self.results = None
        self.logger = logger

    # training the classifier and tracking the time it takes
    def train(self):

        # start time
        start_time = time.time()

        self.classifier.fit(self.train_X, self.train_Y)

        # elapsed time in seconds
        self.elapsed_train_time = time.time() - start_time

        return self

    # classifying the data and tracking the time it takes
    def classify(self):

        # start time
        start_time = time.time()

        self.predicted_results = self.classifier.predict(self.test_X)

        # elapsed time in seconds
        self.elapsed_prediction_time = time.time() - start_time

        return self

    def classify_train(self):

        # start time
        start_time = time.time()

        self.predicted_train_results = self.classifier.predict(self.train_X)

        # elapsed time in seconds
        self.elapsed_prediction_train_time = time.time() - start_time

        return self

    # returns the accuracy, precision, recall, and f1 score of the classifier
    def get_results(self):
        # calculate the accuracy, precision, recall, and f1 score
        accuracy = accuracy_score(self.test_Y, self.predicted_results)
        precision = precision_score(self.test_Y, self.predicted_results)
        recall = recall_score(self.test_Y, self.predicted_results)
        f1 = f1_score(self.test_Y, self.predicted_results)
        return accuracy, precision, recall, f1

    def get_train_results(self):
        # calculate the accuracy, precision, recall, and f1 score
        accuracy = accuracy_score(self.train_Y, self.predicted_train_results)
        precision = precision_score(self.train_Y, self.predicted_train_results)
        recall = recall_score(self.train_Y, self.predicted_train_results)
        f1 = f1_score(self.train_Y, self.predicted_train_results)
        return accuracy, precision, recall, f1

    def get_confusion_matrix(self) -> list[list[float]]:
        return confusion_matrix(self.test_Y, self.predicted_results, normalize='all')

    # plots confusion matrix using ConfusionMatrixDisplay
    def plot_confusion_matrix(self, confusion_matrix, path, labels=["Regular", "Malicious"]):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.logger.log("Plotting confusion matrix to " + path)
        disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=labels)
        disp.plot()
        plt.savefig(path)
        return self

    # string representation of the classifier classname as MDataClassifier[classifier_name]
    def __str__(self):
        return "MDataClassifier[" + self.classifier.__class__.__name__ + "]"
