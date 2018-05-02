# http://www.lextek.com/manuals/onix/stopwords1.html : english stop words
# https://www.ranks.nl/stopwords/french : french stop words
# http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip : labelled tweets data set
# https://www.w3.org/community/sentiment/wiki/Datasets : emoticon Lexicon dictionary among others
# https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107 : english positive and negative words

from os import getcwd
from re import escape, match, sub


def load_stop_word(language='fr'):
    """
    Load all the stop words for the corresponding language
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :return: list of stop words in the desired language
    """
    if language == 'fr':
        path = getcwd() + '/Ressources/stop_word_fr.txt'
    elif language == 'en':
        path = getcwd() + '/Ressources/stop_word_en.txt'

    with open(path, 'r') as file_stop_word:
        stop_word = file_stop_word.readlines()
    return stop_word


def clean_element(element, language='fr'):
    """
    Remove all the undesired stuff from the element in the desired language
    :param element: string representing an element between whitespaces from the tweet
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :return:
        None if the element is not relevant
        String containing the element cleaned
    """
    element = element.lower()

    # if it is a mention or an url we don't need the element
    if match(r'@\w+', element) or match(r'http.+', element):
        return None

    # remove the '#' from the element
    element = sub('#', '', element)

    # remove all the punctuations in the element
    element = sub('[%s]+' % escape("""~"'([-|`\_^@)]=}/*-+.$£¨*!:/;,? """), '', element)

    # remove all repetition of the same alphabetic character
    element = sub(r'(\w)\1+', r'\1', element)

    # check whether the element is relevant or not
    if element in load_stop_word(language):
        return None
    else:
        return element


def clean_text(text, language):
    """
    Clean the text in the desired language from all undesired elements
    :param text: string to transform in a cleaned list of element
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :return: list of relevant and cleaned element from the text
    """
    list_cleaned_element = list()
    for element in text.split(" "):
        cleaned_element = clean_element(element, language)
        if cleaned_element:
            list_cleaned_element.append(cleaned_element)

    return list_cleaned_element
