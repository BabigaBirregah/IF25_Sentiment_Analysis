from os.path import dirname

from Data.clean_data import clean_end_line


def get_path_resource(name_resource):
    """
    Return the complete path of the desired element in the resource directory
    :param name_resource: file to get
    :return: absolute path to the file
    """
    return dirname(__file__) + '\\' + name_resource


def _load_positive_words(language='en'):
    """
    Load in a list all the positive words contained in a text file. One word per line
    :param language: Choose the language from french to english
        'fr' | 'en'
    :return: list of words
    """
    if language == 'fr':
        path = get_path_resource('positive_word_fr.txt')
    elif language == 'en':
        path = get_path_resource('positive_word_en.txt')

    with open(path, 'rb') as file_positive_word:
        positive_word = [clean_end_line(x) for x in file_positive_word.readlines()]
    return positive_word


def _load_negative_words(language='en'):
    """
        Load in a list all the negative words contained in a text file. One word per line
        :param language: Choose the language from french to english
        'fr' | 'en'
        :return: list of words
        """
    if language == 'fr':
        path = get_path_resource('negative_word_fr.txt')
    elif language == 'en':
        path = get_path_resource('negative_word_en.txt')

    with open(path, 'rb') as file_negative_word:
        negative_word = [clean_end_line(x) for x in file_negative_word.readlines()]
    return negative_word


def _load_stop_word(language='en'):
    """
    Load all the stop words for the corresponding language
    :param language: Choose the language from french to english
        'fr' | 'en'
    :return: list of stop words in the desired language
    """
    if language == 'fr':
        path = get_path_resource('stop_word_fr.txt')
    elif language == 'en':
        path = get_path_resource('stop_word_en.txt')

    with open(path, 'rb') as file_stop_word:
        stop_word = [clean_end_line(x) for x in file_stop_word.readlines()]
    return stop_word


def _load_emoticons():
    """
    Load in two separate lists the positive and negative emoticons.
    The file is composed of 'emoticons'sep'0|1' per line.
    Due to the character used in emoticons we have to read them in binary mode.
    :return: 2 lists of positive and negative emoticons
    """
    positive_emoticon_dict, negative_emoticon_dict = list(), list()
    with open(get_path_resource('EmoticonSentimentLexicon.txt'), 'rb') as emoticons_file:
        for line in emoticons_file.readlines():
            key, value = line.split(b'sep')
            if value == b'1':
                positive_emoticon_dict.append(key)
            else:
                negative_emoticon_dict.append(key)
    return positive_emoticon_dict, negative_emoticon_dict


class Resource(object):

    def __init__(self):
        self.positive_words = _load_positive_words()
        self.negative_words = _load_negative_words()
        self.positive_emoticons, self.negative_emoticons = _load_emoticons()
        self.stop_words_en = _load_stop_word('en')
        # self.stop_words_fr = _load_stop_word('fr')


def get_correct_stop_word(Resource, language='en'):
    if language == 'en':
        return Resource.stop_words_en
    else:
        return Resource.stop_words_fr
