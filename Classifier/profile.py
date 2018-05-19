from Classifier.Kernel import Kernel
from Classifier.SVM import SVM
from Data.dataset import get_characteristic_label_vectors


def create_SVM_profile(size_sample, randomness, pos_equal_neg, kernel, language='English'):
    m_features, m_labels = get_characteristic_label_vectors(size_sample, randomness, pos_equal_neg)

    Classifier = SVM(kernel)
    Classifier.fit(m_features, m_labels)

    if randomness:
        random = "rand"
    else:
        random = "nrand"

    if pos_equal_neg:
        pos_neg_eq = "pos-neg-eq"
    else:
        pos_neg_eq = "pos-neg-neq"

    name_file = "Profile/{}_{}_{}_{}.txt".format(str(size_sample), random, pos_neg_eq, str(kernel).split('.')[1])

    Classifier.save_to_file(name_file)


def generate_profiles():
    create_SVM_profile(1000, True, True, Kernel.gaussian())
    create_SVM_profile(1000, True, False, Kernel.gaussian())
    create_SVM_profile(1000, False, True, Kernel.gaussian())
    create_SVM_profile(1000, False, False, Kernel.gaussian())

    create_SVM_profile(1000, True, True, Kernel.linear())
    create_SVM_profile(1000, True, False, Kernel.linear())
    create_SVM_profile(1000, False, True, Kernel.linear())
    create_SVM_profile(1000, False, False, Kernel.linear())

    create_SVM_profile(1000, True, True, Kernel.poly_kernel())
    create_SVM_profile(1000, True, False, Kernel.poly_kernel())
    create_SVM_profile(1000, False, True, Kernel.poly_kernel())
    create_SVM_profile(1000, False, False, Kernel.poly_kernel())

    create_SVM_profile(10000, True, True, Kernel.gaussian())
    create_SVM_profile(10000, True, False, Kernel.gaussian())
    create_SVM_profile(10000, False, True, Kernel.gaussian())
    create_SVM_profile(10000, False, False, Kernel.gaussian())

    create_SVM_profile(10000, True, True, Kernel.linear())
    create_SVM_profile(10000, True, False, Kernel.linear())
    create_SVM_profile(10000, False, True, Kernel.linear())
    create_SVM_profile(10000, False, False, Kernel.linear())

    create_SVM_profile(10000, True, True, Kernel.poly_kernel())
    create_SVM_profile(10000, True, False, Kernel.poly_kernel())
    create_SVM_profile(10000, False, True, Kernel.poly_kernel())
    create_SVM_profile(10000, False, False, Kernel.poly_kernel())


generate_profiles()
