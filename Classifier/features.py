# http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip : labelled tweets data set
# https://www.w3.org/community/sentiment/wiki/Datasets : emoticon Lexicon dictionary among others
# https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107 : english positive and negative words
# http://positivewordsresearch.com/liste-des-mots-positifs/ : french positive words
# http://richesse-et-finance.com/liste-mots-cles-negatifs/ : french negative words

from re import match


def _count_generic(list_element, list_words, weight=1):
    """
    Generic function to count the number of element from list_element in list_words.
    Since we are going to call this function in thread we use a struct -> dict to store the result of the counting.
    We can also apply a weight on the counting (emoticons have somehow bigger impact on the sentiment).
    :param list_element: list of elements we need to confront to list_words
    :param list_words: list of words that we are trying to count in list_element
    :param weight: importance coefficient to use
    :return: None, this function will be used in a thread (hence the dict)
    """
    count = 0
    for element in list_element:
        if element in list_words:
            count += 1 * weight
    return count


def _negation_presence(list_element, language='en'):
    """
    Method to be called within a thread to detect whether there is a negation or not among the elements of the tweets
    contained in the list of elements.
    :param list_element: list of relevant element in the tweet
    :param language: Choose the language from french to english
        'fr' | 'en'
    :return: None, this function will be used in a thread (hence the dict)
    """
    if language == 'fr':
        for element in list_element:
            if match(rb'ne|n\'.*', element):
                return 1
    elif language == 'en':
        for element in list_element:
            if match(rb'.*n\'t', element) or match(rb'neither|not|nor', element):
                return 1
    return 0


def characteristic_vector(list_element_tweet, Resource):
    """
    Creation of the characteristic vector to further use in a classifier.
    The characteristics to be counted :
        - Number of positive words
        - Number of negative words
        - Number of positive emoticons
        - Number of negative emoticons
        - Presence of negation
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param list_element_tweet: list of key elements of a tweet
    :return: list / vector
    """

    return [_count_generic(list_element_tweet, Resource.positive_words),
            _count_generic(list_element_tweet, Resource.negative_words),
            _count_generic(list_element_tweet, Resource.positive_emoticons, 2),
            _count_generic(list_element_tweet, Resource.negative_emoticons, 2), _negation_presence(list_element_tweet)]
