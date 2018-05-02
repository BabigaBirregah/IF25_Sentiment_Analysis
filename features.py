# http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip : labelled tweets data set
# https://www.w3.org/community/sentiment/wiki/Datasets : emoticon Lexicon dictionary among others
# https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107 : english positive and negative words
# http://positivewordsresearch.com/liste-des-mots-positifs/ : french positive words
# http://richesse-et-finance.com/liste-mots-cles-negatifs/ : french negative words

import threading
from os import getcwd
from re import match

from clean_data import clean_end_line


def load_positive_words(language='en'):
    """
    Load in a list all the positive words contained in a text file. One word per line
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :return: list of words
    """
    if language == 'fr':
        path = getcwd() + '/Ressources/positive_word_fr.txt'
    elif language == 'en':
        path = getcwd() + '/Ressources/positive_word_en.txt'

    with open(path, 'rb') as file_positive_word:
        positive_word = [clean_end_line(x) for x in file_positive_word.readlines()]
    return positive_word


def load_negative_words(language='en'):
    """
        Load in a list all the negative words contained in a text file. One word per line
        :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
        :return: list of words
        """
    if language == 'fr':
        path = getcwd() + '/Ressources/negative_word_fr.txt'
    elif language == 'en':
        path = getcwd() + '/Ressources/negative_word_en.txt'

    with open(path, 'rb') as file_negative_word:
        negative_word = [clean_end_line(x) for x in file_negative_word.readlines()]
    return negative_word


def load_emoticons():
    """
    Load in two separate lists the positive and negative emoticons.
    The file is composed of 'emoticons'sep'0|1' per line.
    Due to the character used in emoticons we have to read them in binary mode.
    :return: 2 lists of positive and negative emoticons
    """
    positive_emoticon_dict, negative_emoticon_dict = list(), list()
    with open(getcwd() + '/Ressources/EmoticonSentimentLexicon.txt', 'rb') as emoticons_file:
        print(emoticons_file.readline().split(b'sep'))
        for line in emoticons_file.readlines():
            key, value = line.split(b'sep')
            if value:
                positive_emoticon_dict.append(key)
            else:
                negative_emoticon_dict.append(key)
    return positive_emoticon_dict, negative_emoticon_dict


def count_generic(list_element, list_words, struct, weight=1):
    """
    Generic function to count the number of element from list_element in list_words.
    Since we are going to call this function in thread we use a struct -> dict to store the result of the counting.
    We can also apply a weight on the counting (emoticons have somehow bigger impact on the sentiment).
    :param list_element: list of elements we need to confront to list_words
    :param list_words: list of words that we are trying to count in list_element
    :param struct: dict in which we store the result of the counting
    :param weight: importance coefficient to use
    :return: None, this function will be used in a thread (hence the dict)
    """
    count = 0
    for element in list_element:
        if element in list_words:
            count += 1
    struct['count'] = count


def negation_presence(list_element, language, struct):
    """
    Method to be called within a thread to detect whether there is a negation or not among the elements of the tweets
    contained in the list of elements.
    :param list_element: list of relevant element in the tweet
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :param struct: dict in which we store the result of the counting
    :return: None, this function will be used in a thread (hence the dict)
    """
    if language == 'fr':
        for element in list_element:
            if match(r'ne|n\'.*', element):
                struct['bool'] = 1
                break
    elif language == 'en':
        for element in list_element:
            if match(r'.*n\'t', element) or match(r'neither|not', element):
                struct['bool'] = 1
                break


def characteristic_vector(list_element_tweet, language):
    """
    Creation of the characteristic vector to further use in a classifier.
    The characteristics to be counted :
        - Number of positive words
        - Number of negative words
        - Number of positive emoticons
        - Number of negative emoticons
        - Presence of negation
    :param list_element_tweet: list of key elements of a tweet
    :param language: language used to write the tweet
        'fr' | 'en'
    :return: list / vector
    """
    positive_words = load_positive_words(language)
    negative_words = load_negative_words(language)
    positive_emoticons, negative_emoticons = load_emoticons()
    count_positive_words, count_negative_words, count_positive_emoticons, count_negative_emoticons, presence_negation \
        = dict(), dict(), \
          dict(), dict(), dict()

    count_positive_words['count'] = 0
    count_negative_words['count'] = 0
    count_positive_emoticons['count'] = 0
    count_negative_emoticons['count'] = 0
    presence_negation['bool'] = 0

    thread_pw = threading.Thread(target=count_generic, args=(list_element_tweet, positive_words, count_positive_words))
    thread_nw = threading.Thread(target=count_generic, args=(list_element_tweet, negative_words, count_negative_words))
    thread_pe = threading.Thread(target=count_generic,
                                 args=(list_element_tweet, positive_emoticons, count_positive_emoticons))
    thread_ne = threading.Thread(target=count_generic,
                                 args=(list_element_tweet, negative_emoticons, count_negative_emoticons))
    thread_np = threading.Thread(target=negation_presence, args=(list_element_tweet, language, presence_negation))

    thread_pw.start()
    thread_nw.start()
    thread_pe.start()
    thread_ne.start()
    thread_np.start()

    thread_pw.join()
    thread_nw.join()
    thread_pe.join()
    thread_ne.join()
    thread_np.join()

    return [count_positive_words['count'], count_negative_words['count'], count_positive_emoticons['count'],
            count_negative_emoticons['count'], presence_negation['bool']]
