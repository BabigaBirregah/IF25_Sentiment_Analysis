from json import dumps, loads

from cvxopt import matrix
from cvxopt.solvers import qp
from numpy import (arange, diag, dot, hstack, identity, ones, outer, ravel, sign, vstack,
                   zeros)

from Classifier.Kernel import Kernel


class SVM(object):

    def __init__(self, kernel=Kernel.linear(), C=None):
        self.kernel = kernel
        self.C = C
        if self.C is not None:
            self.C = float(self.C)

    def fit(self, features, labels):
        """

        :param features:
        :param labels:
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
        solution = qp(P, q, G, h, A, b)

        # 3) Lagrange multipliers
        lagrange_multipliers = ravel(solution['x'])

        # 4) Lagrange multipliers
        support_vectors = lagrange_multipliers > 1e-5
        ind = arange(len(lagrange_multipliers))[support_vectors]
        self.lagrange_multipliers = lagrange_multipliers[support_vectors]
        self.support_vectors = features[support_vectors]
        self.support_vectors_labels = labels[support_vectors]
        print("%d support vectors out of %d points" % (len(self.lagrange_multipliers), n_samples))

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

        :param features:
        :return:
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

        :return:
        """
        dic_attribute = dict()
        dic_attribute["kernel"] = self.kernel
        dic_attribute["C"] = self.C
        dic_attribute["weights"] = self.weights
        dic_attribute["lagrange_multipliers"] = self.lagrange_multipliers
        dic_attribute["support_vectors"] = self.support_vectors
        dic_attribute["support_vectors_labels"] = self.support_vectors_labels
        dic_attribute["bias"] = self.bias
        return dic_attribute

    def save_to_file(self):
        """

        :return:
        """
        name_file = str(len(self.support_vectors)) + '_' + str(self.kernel) + '.txt'
        with open(name_file, 'w') as profile:
            profile.write(dumps(self.attributes()))

    def predict(self, features):
        """

        :param features:
        :return:
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

    :param name_file:
    :return:
    """
    with open(name_file, 'r') as profile:
        dic_attribute = loads(profile.read())
    return SVMPredictor(dic_attribute["kernel"], dic_attribute["C"], dic_attribute["weights"],
                        dic_attribute["lagrange_multipliers"], dic_attribute["support_vectors"],
                        dic_attribute["support_vectors_labels"], dic_attribute["bias"])
