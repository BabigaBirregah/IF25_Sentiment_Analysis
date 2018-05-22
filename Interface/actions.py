from numpy import array

from Classifier.Kernel import Kernel
from Classifier.SVM import SVM, get_from_file
from Classifier.features import characteristic_vector
from Classifier.profile import construct_name_file
from Data.clean_data import clean_text
from Data.dataset import get_characteristic_label_vectors
from Data.twitter_collect import collect_tweet, search_sample


def load_classifier(size_sample, randomness, pos_eq_neg, kernel):
    size_sample = int("".join(size_sample.split(" tweets")[0].split()))

    return get_from_file(construct_name_file(size_sample, randomness, pos_eq_neg, kernel))


def analyse_text(text, classifier, Resource, language='en'):
    list_text = clean_text(bytes(text, 'utf-8'))
    m_features = list()
    m_features.append(characteristic_vector(list_text, Resource))
    result = classifier.predict(array(m_features))
    # TODO: create the viewer part for the result


def analyse_file(file_content, classifier, Resource, language='en'):
    pass


def analyse_query(query, classifier, Resource, language='en'):
    twitter_sample = search_sample(query)
    pass


def analyse_tweets(nb_tweets, classifier, Resource, language='en'):
    twitter_sample = collect_tweet(nb_tweets)
    pass


def custom_training(nb_tweet_sample, randomised, equal_pos_neg, language, name_kernel, Resource):
    m_features, m_labels = get_characteristic_label_vectors(nb_tweet_sample, randomised, equal_pos_neg, Resource, True)

    kernel = Kernel.get_correct_kernel(name_kernel)
    custom_SVM = SVM(kernel)
    custom_SVM.fit(m_features, m_labels)

    return custom_SVM
