from cvxopt import matrix
from cvxopt.solvers import qp
from numpy import diag, mean, ones, outer, ravel, shape, sign, vstack, zeros

MIN_SUPPORT_VECTOR_MULTIPLIER = 1e-5


class SVMTrainer(object):
    def __init__(self, kernel, c):
        self._kernel = kernel
        self._c = c

    def train(self, features_vector, labels_vector):
        """
        Given the training features with labels, returns a SVM predictor representing the trained SVM
        :param features_vector:
        :param labels_vector:
        :return:
        """
        lagrange_multipliers = self._compute_multipliers(features_vector, labels_vector)
        return self._construct_predictor(features_vector, labels_vector, lagrange_multipliers)

    def _gram_matrix(self, features_vector):
        n_samples, n_features = shape(features_vector)
        K = zeros((n_samples, n_samples))
        for i, x_i in enumerate(features_vector):
            for j, x_j in enumerate(features_vector):
                K[i, j] = self._kernel(x_i, x_j)
        return K

    def _construct_predictor(self, features_vector, labels_vector, lagrange_multipliers):
        support_vector_indices = lagrange_multipliers > MIN_SUPPORT_VECTOR_MULTIPLIER

        support_multipliers = lagrange_multipliers[support_vector_indices]
        support_vectors = features_vector[support_vector_indices]
        support_vector_labels = labels_vector[support_vector_indices]

        bias = mean([y_k - SVMPredictor(kernel=self._kernel, bias=0.0, weights=support_multipliers,
                                        support_vectors=support_vectors,
                                        support_vector_labels=support_vector_labels).predict(x_k) for (y_k, x_k) in
                     zip(support_vector_labels, support_vectors)])
        return SVMPredictor(kernel=self._kernel, bias=bias, weights=support_multipliers,
                            support_vectors=support_vectors, support_vector_labels=support_vector_labels)

    def _compute_multipliers(self, features_vector, labels_vector):
        n_samples, n_features = shape(features_vector)

        K = self._gram_matrix(features_vector)

        P = matrix(outer(labels_vector, labels_vector) * K)
        q = matrix(-1 * ones(n_samples))

        G_std = matrix(diag(ones(n_samples) * -1))
        h_std = matrix(zeros(n_samples))

        G_slack = matrix(diag(ones(n_samples)))
        h_slack = matrix(ones(n_samples) * self._c)

        G = matrix(vstack((G_std, G_slack)))
        h = matrix(vstack((h_std, h_slack)))

        A = matrix(labels_vector, (1, n_samples))
        b = matrix(0.0)

        solution = qp(P, q, G, h, A, b)

        return ravel(solution['x'])


class SVMPredictor(object):
    def __init__(self, kernel, bias, weights, support_vectors, support_vector_labels):
        """

        :param kernel:
        :param bias:
        :param weights:
        :param support_vectors:
        :param support_vector_labels:
        """
        self._kernel = kernel
        self._bias = bias
        self._weights = weights
        self._support_vectors = support_vectors
        self._support_vector_labels = support_vector_labels

    def predict(self, features_given):
        """
        Computes the SVM prediction on the given features
        :param features_given:
        :return:
        """
        result = self._bias
        for z_i, x_i, y_i in zip(self._weights, self._support_vectors, self._support_vector_labels):
            result += z_i * y_i * self._kernel(x_i, features_given)
        return sign(result).item()
