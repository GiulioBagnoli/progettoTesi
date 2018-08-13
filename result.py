from svmutil_prova import *
import pickle


class result:

    def __init__(self, classificazione, kernel, scalati, dimensioni, features, prob, x, y,):
        self.classificazione = classificazione
        self.kernel = kernel
        self.scalati = scalati
        self.features = features  # indica le features utilizzate per l'addestramento della rete
        self.dimensioni = dimensioni  # indica le dimensioni del train e del set in percentuale

        options = self.classificazione + self.kernel + ' -q'
        m = svm_train(prob, options)
        auxResult = svm_predict(y, x, m)

        self.accuracy = auxResult[1][0]
        self.meanSquareError = auxResult[1][1]
        self.squaredCorrelationCoefficent = auxResult[1][2]
        self.predictedLabels = auxResult[0]
        self.decisionValues = auxResult[2]

