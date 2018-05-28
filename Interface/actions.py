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
    Analyse a simple text / tweet with the classifier and the resources provided
    :param text: string containing the text to predict the sentiment of
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: sentiment label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    list_text = clean_text(bytes(text, 'utf-8'), get_correct_stop_word(Resource, language))
    m_features = list()
    m_features.append(characteristic_vector(list_text, Resource))
    return classifier.predict(array(m_features))


def analyse_text(custom_text, classifier, Resource, language='en'):
    """
    Predict the sentiment of the text
    :param custom_text: string containg the text to analyse
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: list of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    result = _minimal_analysis(custom_text, classifier, Resource, language)
    return [(custom_text, result)]


def analyse_file(file_content, classifier, Resource, language='en'):
    """
    Predict the sentiment for every line, representing a text / tweet, in the file
    :param file_content: list of text / tweet described by one line in the file
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: generator of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    for line in file_content:
        yield (line, _minimal_analysis(line, classifier, Resource, language))


def analyse_query(query, classifier, Resource, language='en'):
    """
    Predict the sentiment of some trending tweets around the query
    :param query: '#...' to look for
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: generator of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    for line in search_sample(query):
        yield (line, _minimal_analysis(line, classifier, Resource, language))


def analyse_tweets(nb_tweets, classifier, Resource, language='en'):
    """
    Predict the sentiment of the desired number of tweets from the Twitter stream
    :param nb_tweets: number of tweets to collect from the Twitter stream
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: generator of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    for line in collect_tweet(nb_tweets):
        yield (line, _minimal_analysis(line, classifier, Resource, language))


def custom_training(nb_tweet_sample, randomised, equal_pos_neg, language, name_kernel, Resource):
    """
    Create a tailored SVM classifier to further use to predict
    :param nb_tweet_sample: size of the desired characteristic vector to be used to train the classifier
    :param randomised: boolean to get tweets randomly from the data set or use pop
    :param equal_pos_neg: boolean to get the same amount of positive and negative tweets from the data set
    :param language: not yet used, choose between french and english
        'fr' | 'en'
    :param name_kernel: name of the kernel to use to create the desired SVM classifier
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :return:
    """
    m_features, m_labels = get_characteristic_label_vectors(nb_tweet_sample, randomised, equal_pos_neg, Resource, False,
                                                            language)

    kernel = Kernel.get_correct_kernel(name_kernel)
    custom_SVM = SVM(kernel)
    custom_SVM.fit(m_features, m_labels)

    return custom_SVM
