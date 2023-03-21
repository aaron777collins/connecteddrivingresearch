import time
from Logger import Logger
from MDataClassifier import MDataClassifier

# extends MDataClassifier
class MDataDeepLearningClassifier(MDataClassifier):

    def __init__(self, classifier, train_X, train_Y, test_X, test_Y, logger=Logger("MDataDeepLearningClassifier")):
        super().__init__(classifier, train_X, train_Y, test_X, test_Y, logger)

    # add batch_size and epochs to train (with features, answers) and call fit
    def train(self, features, answers, batch_size=32, epochs=10):
        # start time
        start_time = time.time()

        # train
        self.classifier.fit(features, answers, batch_size=batch_size, epochs=epochs)

        # elapsed time in seconds
        self.elapsed_train_time = time.time() - start_time

        return self
