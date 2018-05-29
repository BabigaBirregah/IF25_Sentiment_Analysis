from Classifier.Kernel import Kernel
from Classifier.SVM import SVM
from Data.dataset import get_characteristic_label_vectors


def readable_name_classifier(name_file):
    """

    :param name_file:
    :return:
    """
    try:
        size, randomness, pos_equal_neg, kernel = name_file.split('_')
    except:
        size, randomness, pos_equal_neg, kernel, poly = name_file.split('_')
        kernel = kernel + '-' + poly
    classifier_name = str(size) + " characteristic vectors ; "
    if randomness == "rand":
        classifier_name += "sample read randomly ; "
    else:
        classifier_name += "sample read non-randomly ; "

    if pos_equal_neg == "pos-neg-eq":
        classifier_name += "number positive = number negative ; "
    else:
        classifier_name += "number positive != number negative ; "

    return classifier_name + kernel + " kernel"

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

    return "{}_{}_{}_{}.json".format(size_sample, randomness, pos_equal_neg, kernel)


def create_SVM_profile(size_sample, randomness, pos_equal_neg, kernel, Resource, m_features=None,
                       m_labels=None, language='en'):
    """
    With the desired parameters, create a SVM classifier and save it to a file
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
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
    :param language: Choose the language from french to english
        'fr' | 'en'
    :return:
    """
    if m_features is None and m_labels is None:
        m_features, m_labels = get_characteristic_label_vectors(size_sample, randomness, pos_equal_neg, Resource, False,
                                                                language)

    Classifier = SVM(kernel)
    Classifier.fit(m_features, m_labels)

    name_file = construct_name_file(size_sample, randomness, pos_equal_neg, str(kernel).split('.')[1])

    Classifier.save_to_file(name_file)


def generate_profiles(Resource, name_kernel=None, l_size=None, l_random=None, l_pos_eq_neg=None, language='en'):
    """
    Generate multiple profiles for one or more kernels
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param name_kernel:
        (optional) name of the kernel to use
        (default) will construct profiles for every kernel (linear, poly_kernel, gaussian)
    :param l_size: list of the desired size of characteristic vectors
    :param l_random: list of situation of randomness
    :param l_pos_eq_neg: list of situation of positives equal negatives
    :param language: Choose the language from french to english
        'fr' | 'en'
    :return:
    """
    if l_random is None:
        l_random = [True, False]
    if l_pos_eq_neg is None:
        l_pos_eq_neg = [True, False]
    if l_size is None:
        l_size = [1000, 10000]

    for size_sample in l_size:
        for randomness in l_random:
            for pos_eq_neg in l_pos_eq_neg:
                m_features, m_labels = get_characteristic_label_vectors(size_sample, randomness, pos_eq_neg, Resource,
                                                                        False, language)
                if type(name_kernel) is str:
                    kernel = Kernel.get_correct_kernel(name_kernel)
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, kernel, Resource, m_features, m_labels)
                elif type(name_kernel) is list:
                    for name in name_kernel:
                        kernel = Kernel.get_correct_kernel(name)
                        create_SVM_profile(size_sample, randomness, pos_eq_neg, kernel, Resource, m_features, m_labels)
                else:
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, Kernel.linear(), Resource, m_features,
                                       m_labels)
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, Kernel.poly_kernel(), Resource, m_features,
                                       m_labels)
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, Kernel.gaussian(), Resource, m_features,
                                       m_labels)
                    create_SVM_profile(size_sample, randomness, pos_eq_neg, Kernel.radial_basis(), Resource, m_features,
                                       m_labels)