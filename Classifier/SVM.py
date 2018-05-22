from json import dumps, loads

from cvxopt import matrix
from cvxopt.solvers import qp
from numpy import (arange, array, diag, dot, hstack, identity, ones, outer, ravel, sign, vstack, zeros)

from Classifier.Kernel import Kernel


class SVM(object):

    def __init__(self, kernel=Kernel.linear(), C=None):
        self.kernel = kernel
        self.C = C
        if self.C is not None:
            self.C = float(self.C)

    def fit(self, features, labels, iters=16):
        """
        Compute the parameters of the SVM classifier regarding the features and the associated labels.
        :param features: array of features vectors
        :param labels: array of labels vectors corresponding to the features
        :param iters: number of iteration to solve the quadratic problem
        :return:
        """
        n_samples, n_features = features.shape

        # 1) Gram matrix
        K = zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i, j] = self.kernel(features[i], features[j])

        P = matrix(outer(labels, labels) * K)
        q = matrix(ones(n_samples) * -1)
        A = matrix(labels, (1, n_samples))
        b = matrix(0.0)

        if self.C is None:
            G = matrix(diag(ones(n_samples) * -1))
            h = matrix(zeros(n_samples))
        else:
            tmp1 = diag(ones(n_samples) * -1)
            tmp2 = identity(n_samples)
            G = matrix(vstack((tmp1, tmp2)))
            tmp1 = zeros(n_samples)
            tmp2 = ones(n_samples) * self.C
            h = matrix(hstack((tmp1, tmp2)))

        # 2) Resolve QP problem
        options = dict()
        options['maxiters'] = iters
        # options['show_progress'] = False
        solution = qp(P, q, G, h, A, b, options=options)['x']

        # 3) Lagrange multipliers
        lagrange_multipliers = ravel(solution)

        # 4) Lagrange multipliers
        support_vectors = lagrange_multipliers > 1e-5
        ind = arange(len(lagrange_multipliers))[support_vectors]
        self.lagrange_multipliers = lagrange_multipliers[support_vectors]
        self.support_vectors = features[support_vectors]
        self.support_vectors_labels = labels[support_vectors]

        # 5) Bias
        self.bias = 0
        for n in range(len(self.lagrange_multipliers)):
            self.bias += self.support_vectors_labels[n]
            self.bias -= sum(self.lagrange_multipliers * self.support_vectors_labels * K[ind[n], support_vectors])
        self.bias /= len(self.lagrange_multipliers)

        # 6) Weight vector
        if self.kernel == Kernel.linear():
            self.weights = zeros(n_features)
            for n in range(len(self.lagrange_multipliers)):
                self.weights += self.lagrange_multipliers[n] * self.support_vectors_labels[n] * self.support_vectors[n]
        else:
            self.weights = None

    def _project(self, features):
        """
        Compute the score of the features
        :param features: array of features vectors
        :return: score prediction of the features (real number)
        """
        if self.weights is not None:
            return dot(features, self.weights) + self.bias
        else:
            y_predict = zeros(len(features))
            for i in range(len(features)):
                s = 0
                for lagrange_multipliers, support_vectors_labels, support_vectors in zip(self.lagrange_multipliers,
                                                                                         self.support_vectors_labels,
                                                                                         self.support_vectors):
                    s += lagrange_multipliers * support_vectors_labels * self.kernel(features[i], support_vectors)
                y_predict[i] = s
            return y_predict + self.bias

    def attributes(self):
        """
        Create a dictionary (that is writable to a file) of the different attributes of the SVM classifier
        :return: dictionary containing the different attributes of the SVM classifier
        """
        dic_attribute = dict()
        dic_attribute["kernel"] = str(self.kernel).split('.')[1]
        dic_attribute["C"] = self.C
        if self.weights:
            dic_attribute["weights"] = self.weights.tolist()
        else:
            dic_attribute["weights"] = self.weights
        dic_attribute["lagrange_multipliers"] = self.lagrange_multipliers.tolist()
        dic_attribute["support_vectors"] = self.support_vectors.tolist()
        dic_attribute["support_vectors_labels"] = self.support_vectors_labels.tolist()
        dic_attribute["bias"] = self.bias
        return dic_attribute

    def save_to_file(self, name_file):
        """
        Save to a file the SVM classifier to initiate a SVMPredictor
        :param name_file: name of the file to save all the attributes of the SVM classifier to a file
        :return:
        """
        with open(name_file, 'w') as profile:
            profile.write(dumps(self.attributes()))

    def predict(self, features):
        """
        Given an array of features, predict the label of each vector
        :param features: array of features vectors
        :return: array of corresponding labels (0.0 or 1.0)
        """
        return sign(self._project(features))


class SVMPredictor(SVM):

    def __init__(self, kernel, C, weights, lagrange_multipliers, support_vectors, support_vectors_labels, bias):
        self.kernel = kernel
        self.C = C
        self.weights = weights
        self.lagrange_multipliers = lagrange_multipliers
        self.support_vectors = support_vectors
        self.support_vectors_labels = support_vectors_labels
        self.bias = bias


def get_from_file(name_file):
    """
    Create a SVM classifier already initiated with the information contained in the corresponding file
    :param name_file: name of the file containing the information to initiate the SVM classifier
    :return: SVM classifier already initiated (ready to predict)
    """
    with open(name_file, 'r') as profile:
        dic_attribute = loads(profile.read())

    if dic_attribute["kernel"] == "linear":
        kernel = Kernel.linear()
    elif dic_attribute["kernel"] == "gaussian":
        kernel = Kernel.gaussian()
    elif dic_attribute["kernel"] == "poly_kernel":
        kernel = Kernel.poly_kernel()
    elif dic_attribute["kernel"] == "hyperbolic_tangent":
        kernel = Kernel.hyperbolic_tangent()
    else:
        kernel = Kernel.radial_basis()

    if dic_attribute["weights"]:
        dic_attribute["weights"] = array(dic_attribute["weights"])

    return SVMPredictor(kernel, dic_attribute["C"], dic_attribute["weights"],
                        array(dic_attribute["lagrange_multipliers"]), array(dic_attribute["support_vectors"]),
                        array(dic_attribute["support_vectors_labels"]), dic_attribute["bias"])
