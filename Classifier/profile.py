from Classifier.Kernel import Kernel
from Classifier.SVM import SVM
from Data.dataset import get_characteristic_label_vectors


def construct_name_file(size_sample, randomness, pos_equal_neg, kernel):
    """
    Build the name of the file to save the SVM classifier attributes to create a SVM classifier later
    :param size_sample: number of tweets / characteristic vectors used
    :param randomness: if the collection was randomised from data set
    :param pos_equal_neg: if there was the same amount of positive and negative tweets / characteristic vectors
    :param kernel: name of the kernel used
    :return: string name of the file
    """
    if randomness:
        randomness = "rand"
    else:
        randomness = "nrand"

    if pos_equal_neg:
        pos_equal_neg = "pos-neg-eq"
    else:
        pos_equal_neg = "pos-neg-neq"

    return "Profile/{}_{}_{}_{}.json".format(size_sample, randomness, pos_equal_neg, kernel)


def create_SVM_profile(size_sample, randomness, pos_equal_neg, kernel, m_features=None,
                       m_labels=None, language='English'):
    """
    With the desired parameters, create a SVM classifier and save it to a file
    :param size_sample: number of tweets / characteristic vectors to use
    :param randomness: if the collection should be randomised from data set
    :param pos_equal_neg: if the same amount of positive and negative tweets / characteristic vectors should be used
    :param kernel: name of the kernel to use
    :param m_features:
        (optional) array of already constructed features vector
        (default) will construct an array of features vector
    :param m_labels:
        (optional) array of already constructed labels vector
        (default) will construct an array of labels vector
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :return:
    """
    if m_features is None and m_labels is None:
        m_features, m_labels = get_characteristic_label_vectors(size_sample, randomness, pos_equal_neg)

    Classifier = SVM(kernel)
    Classifier.fit(m_features, m_labels)

    name_file = construct_name_file(size_sample, randomness, pos_equal_neg, str(kernel).split('.')[1])

    Classifier.save_to_file(name_file)


def generate_profiles(kernel=None, l_size=[1000, 10000], l_random=[True, False], l_pos_eq_neg=[True, False]):
    """
    Generate multiple profiles for one or more kernels
    :param kernel:
        (optional) name of the kernel to use
        'default) will construct profiles for every kernel (linear, poly_kernel, gaussian)
    :param l_size: list of the desired size of characteristic vectors
    :param l_random: list of situation of randomness
    :param l_pos_eq_neg: list of situation of positives equal negatives
    :return:
    """
    if kernel == "linear":
        kernel = Kernel.linear()
    elif kernel == "poly_kernel":
        kernel = Kernel.poly_kernel()
    elif kernel == "gaussian":
        kernel = Kernel.gaussian()

    for size_sample in l_size:
        for randomness in l_random:
            for pos_eq_neg in l_pos_eq_neg:
                m_features, m_labels = get_characteristic_label_vectors(size_sample, randomness, pos_eq_neg)
                if kernel is not None:
                    try:
                        create_SVM_profile(size_sample, randomness, pos_eq_neg, kernel, m_features, m_labels)
                    except:
                        print("fail : " + construct_name_file(size_sample, randomness, pos_eq_neg,
                                                              str(kernel).split('.')[1]))
                else:
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, Kernel.linear(), m_features, m_labels)
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, Kernel.poly_kernel(), m_features, m_labels)
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, Kernel.gaussian(), m_features, m_labels)
