import time

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from Logger import Logger
from MaliciousDataDetection.MDataClassifier import MDataClassifier
import numpy as np

# extends MDataClassifier
class MDeepLearningDataClassifier(MDataClassifier):

    @staticmethod
    def round_0_or_1(number) -> float:
        if (number < 0.5):
            return 0.0
        else:
            return 1.0

    def __init__(self, classifier, train_X, train_Y, test_X, test_Y, logger=Logger("MDataDeepLearningClassifier")):
        super().__init__(classifier, train_X, train_Y, test_X, test_Y, logger=logger)

    # add batch_size and epochs to train (with features, answers) and call fit
    def train(self, batch_size=32, epochs=10):
        # start time
        start_time = time.time()

        # train
        self.classifier.fit(self.train_X, self.train_Y, batch_size=batch_size, epochs=epochs)

        # elapsed time in seconds
        self.elapsed_train_time = time.time() - start_time

        return self

    def transpose_pred_round_0_or_1(self):
        self.predicted_results = list(map(MDeepLearningDataClassifier.round_0_or_1, np.transpose(self.predicted_results)[0]))
        return self

    def transpose_pred_train_round_0_or_1(self):
        self.predicted_train_results = list(map(MDeepLearningDataClassifier.round_0_or_1, np.transpose(self.predicted_train_results)[0]))
        return self

    def pred_round_0_or_1(self):
        self.predicted_results = list(map(MDeepLearningDataClassifier.round_0_or_1, self.predicted_results))
        return self

    def pred_train_round_0_or_1(self):
        self.predicted_train_results = list(map(MDeepLearningDataClassifier.round_0_or_1, self.predicted_train_results))

    # classifying the data and tracking the time it takes
    def classify(self):

        # start time
        start_time = time.time()

        self.predicted_results = self.classifier.predict(self.test_X)

        # self.transpose_pred_round_0_or_1()
        self.pred_round_0_or_1()

        # elapsed time in seconds
        self.elapsed_prediction_time = time.time() - start_time

        return self

    def classify_train(self):

        # start time
        start_time = time.time()

        self.predicted_train_results = self.classifier.predict(self.train_X)

        # self.transpose_pred_train_round_0_or_1()
        self.pred_train_round_0_or_1()

        # elapsed time in seconds
        self.elapsed_prediction_train_time = time.time() - start_time

        return self

    # string representation of the classifier classname as MDataClassifier[classifier_name]
    def __str__(self):
        return "MDeepLearningDataClassifier[" + self.classifier.__class__.__name__ + "]"
