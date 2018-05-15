import numpy as np
import numpy.linalg as la


class Kernel(object):
    """
    Implements list of kernels from http://en.wikipedia.org/wiki/Support_vector_machine
    """

    @staticmethod
    def linear():
        return lambda x, y: np.inner(x, y)

    @staticmethod
    def gaussian(sigma=5.0):
        return lambda x, y: np.exp(-np.sqrt(la.norm(x - y) ** 2 / (2 * sigma ** 2)))

    @staticmethod
    def poly_kernel(dimension=3, offset=1.0):
        return lambda x, y: (offset + np.inner(x, y)) ** dimension

    @staticmethod
    def hyperbolic_tangent(kappa=0.2, c=0):
        return lambda x, y: np.tanh(kappa * np.dot(x, y) + c)

    @staticmethod
    def radial_basis(gamma=10):
        return lambda x, y: np.exp(-gamma * la.norm(np.subtract(x, y)))
