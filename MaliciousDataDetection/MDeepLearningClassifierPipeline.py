# Deep Learning Pipelin extends MClassifierPipeline
from Logger import Logger
from MaliciousDataDetection.MClassifierPipeline import MClassifierPipeline
from MaliciousDataDetection.MDeepLearningDataClassifier import MDeepLearningDataClassifier
from MaliciousDataDetection.Models.LSTMModel import LSTMModel

DEEP_LEARNING_CLASSIFIER_INSTANCES = [
    LSTMModel.getCompiledModel(LSTMModel.getUncompiledModel(24, 1, memoryunits=128, activation="sigmoid", embedding=True, embeddingInputDim=1000, embeddingOutputDim=32), loss="binary_crossentropy", optimizer="adam", metrics=["accuracy", "mse", "mae"])
]

class MDeepLearningClassifierPipeline(MClassifierPipeline):
    def __init__(self, train_X, train_Y, test_X, test_Y, classifier_instances=DEEP_LEARNING_CLASSIFIER_INSTANCES, logger=Logger("MDeepLearningClassifierPipeline")):
        self.classifier_instances = classifier_instances
        super().__init__(train_X, train_Y, test_X, test_Y, classifier_instances=classifier_instances, logger=logger)
        self.classifiers_and_confusion_matrices: list[tuple[MDeepLearningDataClassifier, list[list[float]]]] = []

        # create MDeepLearningDataClassifier instances for each classifier
        self.classifiers: list[MDeepLearningDataClassifier] = []
        for classifier_instance in classifier_instances:
            self.classifiers.append(
                MDeepLearningDataClassifier(classifier_instance, train_X, train_Y, test_X, test_Y, logger=self.logger.newPrefix("MDeepLearningDataClassifier-"+classifier_instance.__class__.__name__)))
