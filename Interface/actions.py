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
    Load the desired SVM classifier saved in a file
    :param size_sample: size of the sample used
    :param randomness: boolean indicating the randomness of the sample
    :param pos_eq_neg: boolean indicating if the number of positive and negative features vectors is equal
    :param kernel: name of the kernel used
    :return: SVM Predictor (SVM classifier ready to predict)
    """
    if type(size_sample) is str:
        size_sample = int("".join(size_sample.split(" tweets")[0].split()))

    return get_from_file(construct_name_file(size_sample, randomness, pos_eq_neg, kernel))


def _minimal_analysis(text, classifier, Resource, threshold, language='en'):
    """
    Analyse a simple text / tweet with the classifier and the resources provided
    :param text: string containing the text to predict the sentiment of
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: sentiment label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    list_text = clean_text(bytes(text, 'utf-8'), get_correct_stop_word(Resource, language))
    m_features = list()
    m_features.append(characteristic_vector(list_text, Resource))
    return classifier.predict(array(m_features), threshold), m_features


def analyse_text(custom_text, classifier, Resource, threshold, language='en'):
    """
    Predict the sentiment of the text
    :param custom_text: string containing the text to analyse
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: list of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    return [(custom_text, _minimal_analysis(custom_text, classifier, Resource, threshold, language))]


def analyse_file(file_content, classifier, Resource, threshold, language='en'):
    """
    Predict the sentiment for every line, representing a text / tweet, in the file
    :param file_content: list of text / tweet described by one line in the file
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: generator of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    return [(line, _minimal_analysis(line, classifier, Resource, threshold, language)) for line in file_content]


def analyse_query(query, classifier, Resource, threshold, language='en'):
    """
    Predict the sentiment of some trending tweets around the query
    :param query: '#...' to look for
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: generator of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    return [(line, _minimal_analysis(line, classifier, Resource, threshold, language)) for line in search_sample(query)]


def analyse_tweets(nb_tweets, classifier, Resource, threshold, language='en'):
    """
    Predict the sentiment of the desired number of tweets from the Twitter stream
    :param nb_tweets: number of tweets to collect from the Twitter stream
    :param classifier: SVM classifier to use to predict the sentiment
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :param language: not used, choose between french and english
        'fr' | 'en'
    :return: generator of sentiments label of the text
        'Negative' | 'Neutral' | 'Positive'
    """
    return [(line, _minimal_analysis(line, classifier, Resource, threshold, language)) for line in
            collect_tweet(nb_tweets)]


def _minimal_predict(Classifier, vector, threshold):
    """
    Analyse one feature vector and predict the sentiment of this vector
    :param Classifier: SVM classifier to use to predict the sentiment
    :param vector: array containing the features (in a vector) of a corresponding tweet / text
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :return: string containing the label of the features vector
    """
    return Classifier.predict(array([vector.tolist()]), threshold)


def _performance(Classifier, features, labels, threshold):
    """
    For an array containing multiple features vector with the supposed label, compute the score (%) of the SVM
    classifier to predict the correct label
    :param Classifier: SVM classifier to use and measure the performance
    :param features: array of multiple characteristic vectors
    :param labels: array containing the labels of each characteristic vector
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :return: float containing the score of the classifier
    """
    correct = 0
    for index, vector in enumerate(features):
        result = _minimal_predict(Classifier, vector, threshold)
        if result == "Positive" and labels[index] == 1.0 or result == "Negative" and labels[
            index] == 0.0 or result == "Neutral":
            correct += 1
    return correct / len(labels) * 100


def _prediction(features, labels, threshold, size_sample, randomised, equal_pos_neg, name_kernel):
    """
    Generic method to compute the performance score of a designated classifier
    :param features: array containing multiple features vectors
    :param labels: array containing the labels of the features
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :param size_sample: size of the sample use to build and save the SVM classifier
    :param randomised: boolean to indicate the randomised reading of the sample use to build and save the SVM classifier
    :param equal_pos_neg: boolean to indicate if the number of positive and negative tweets of the sample use to
    build and save the SVM classifier
    :param name_kernel: name of the kernel use to build and save the SVM classifier
    :return: tuple containing the general name of the classifier and the performance score of this classifier
    """
    Classifier = load_classifier(size_sample, randomised, equal_pos_neg, name_kernel)
    name_file = str(construct_name_file(size_sample, randomised, equal_pos_neg, name_kernel).split(".json")[0])
    return name_file, _performance(Classifier, features, labels, threshold)


def predict_test(nb_tweet_sample, Resource, threshold, size_sample=None, randomised=None, equal_pos_neg=None,
                 name_kernel=None,
                 language='en'):
    """
    Measure the performance score for one specific classifier or all the default profiles
    :param nb_tweet_sample: size of the sample to test against the classifier
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param threshold: From -'threshold' to +'threshold' the class label will be 'Neutral'. In the computation of the
    performance score, 'Neutral' is both considered 'Positive' and 'Negative'
    :param size_sample: size of the sample use to build and save the SVM classifier
    :param randomised: boolean to indicate the randomised reading of the sample use to build and save the SVM classifier
    :param equal_pos_neg: boolean to indicate if the number of positive and negative tweets of the sample use to
    build and save the SVM classifier
    :param name_kernel: name of the kernel use to build and save the SVM classifier
    :param language: not used, choose between english and french
        'en' | 'fr'
    :return: generator containing tuples of the name of the classifier and its performance score
    """
    m_features, m_labels = get_characteristic_label_vectors(nb_tweet_sample, randomised, equal_pos_neg, Resource, False,
                                                            language)

    result = list()
    if name_kernel is not None:
        result.append(_prediction(m_features, m_labels, threshold, size_sample, randomised, equal_pos_neg, name_kernel))
    else:
        for size_sample in [1000, 10000]:
            for randomised in [True, False]:
                for equal_pos_neg in [True, False]:
                    for name_kernel in ["linear", "poly_kernel", "gaussian", "radial_basis"]:
                        result.append(
                            _prediction(m_features, m_labels, threshold, size_sample, randomised, equal_pos_neg,
                                        name_kernel))
    return result


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
