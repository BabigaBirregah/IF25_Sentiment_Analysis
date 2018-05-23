from numpy import array

from Classifier.Kernel import Kernel
from Classifier.SVM import SVM, get_from_file
from Classifier.features import characteristic_vector
from Classifier.profile import construct_name_file
from Data.clean_data import clean_text
from Data.dataset import get_characteristic_label_vectors
from Data.twitter_collect import collect_tweet, search_sample
from Ressources.resource import get_correct_stop_word


def load_classifier(size_sample, randomness, pos_eq_neg, kernel):
    """
    Load th desired SVM classifier saved in a file
    :param size_sample: size of the sample used
    :param randomness: boolean indicating the randomness of the sample
    :param pos_eq_neg: boolean indicating if the number of positive and negative features vectors is equal
    :param kernel: name of the kernel used
    :return: SVM Predictor (SVM classifier ready to predict)
    """
    size_sample = int("".join(size_sample.split(" tweets")[0].split()))

    return get_from_file(construct_name_file(size_sample, randomness, pos_eq_neg, kernel))


def _minimal_analysis(text, classifier, Resource, language='en'):
    """

    :param text:
    :param classifier:
    :param Resource:
    :param language:
    :return:
    """
    list_text = clean_text(bytes(text, 'utf-8'), get_correct_stop_word(Resource, language))
    m_features = list()
    m_features.append(characteristic_vector(list_text, Resource))
    return classifier.predict(array(m_features))


def analyse_text(custom_text, classifier, Resource, language='en'):
    """

    :param custom_text:
    :param classifier:
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language:
    :return:
    """
    result = _minimal_analysis(custom_text, classifier, Resource, language)
    return [result]


def analyse_file(file_content, classifier, Resource, language='en'):
    """

    :param file_content:
    :param classifier:
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language:
    :return:
    """
    for line in file_content:
        yield _minimal_analysis(line, classifier, Resource, language)


def analyse_query(query, classifier, Resource, language='en'):
    """

    :param query:
    :param classifier:
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language:
    :return:
    """
    for line in search_sample(query):
        yield _minimal_analysis(line, classifier, Resource, language)


def analyse_tweets(nb_tweets, classifier, Resource, language='en'):
    """

    :param nb_tweets:
    :param classifier:
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language:
    :return:
    """
    for line in collect_tweet(nb_tweets):
        yield _minimal_analysis(line, classifier, Resource, language)


def custom_training(nb_tweet_sample, randomised, equal_pos_neg, language, name_kernel, Resource):
    """

    :param nb_tweet_sample:
    :param randomised:
    :param equal_pos_neg:
    :param language:
    :param name_kernel:
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :return:
    """
    m_features, m_labels = get_characteristic_label_vectors(nb_tweet_sample, randomised, equal_pos_neg, Resource, True,
                                                            language)

    kernel = Kernel.get_correct_kernel(name_kernel)
    custom_SVM = SVM(kernel)
    custom_SVM.fit(m_features, m_labels)

    return custom_SVM
