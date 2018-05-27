from numpy import exp, inner, sqrt, subtract
from numpy.linalg import norm


class Kernel(object):
    @staticmethod
    def linear():
        return lambda x, y: inner(x, y)

    @staticmethod
    def gaussian(sigma=5.0):
        return lambda x, y: exp(-sqrt(norm(x - y) ** 2 / (2 * sigma ** 2)))

    @staticmethod
    def poly_kernel(dimension=3, offset=1.0):
        return lambda x, y: (offset + inner(x, y)) ** dimension

    @staticmethod
    def radial_basis(gamma=10):
        return lambda x, y: exp(-gamma * norm(subtract(x, y)))

    @staticmethod
    def get_correct_kernel(name):
        if name == "linear":
            return Kernel.linear()
        elif name == "poly_kernel":
            return Kernel.poly_kernel()
        elif name == "gaussian":
            return Kernel.gaussian()
        elif name == "radial_basis":
            return Kernel.radial_basis()
