# http://www.lextek.com/manuals/onix/stopwords1.html : english stop words
# https://www.ranks.nl/stopwords/french : french stop words

from re import escape, match, sub

from Ressources.resource import get_path_resource


def clean_end_line(text):
    """
    Remove the ending character from a string
    :param text: word or text that ends with an ending character
    :return: string containing the same text without ending character
    """
    return sub(rb'(.*)\1\n|\r|\r\n', rb'\1', text)


def load_stop_word(language='en'):
    """
    Load all the stop words for the corresponding language
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
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


def clean_element(element, language='en'):
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
    if match(rb'@\w+', element) or match(rb'http.+', element):
        return None

    # remove the '#' from the element
    element = sub(rb'#', rb'', element)

    # remove all the punctuations in the element
    element = sub(rb'[%s]+' % escape("""~"'([-|`\_^@)]=}/*-+.$£¨*!:/;,? """), r'', element)

    # remove all repetition of the same alphabetic character
    element = sub(rb'(\w)\1+', rb'\1', element)

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
    for element in text.split(rb" "):
        cleaned_element = clean_element(element, language)
        if cleaned_element:
            list_cleaned_element.append(cleaned_element)

    return list_cleaned_element
