# http://www.lextek.com/manuals/onix/stopwords1.html : english stop words
# https://www.ranks.nl/stopwords/french : french stop words

from re import escape, match, sub


def clean_end_line(text):
    """
    Remove the ending characters from a string
    :param text: word or text that ends with an ending character
    :return: string containing the same text without ending characters
    """
    return sub(rb'(.*)\1\n|\r|\r\n', rb'\1', text)


def _clean_element(element, stop_words):
    """
    Remove all the undesired stuff from the element including stop words in the correct language
    :param element: string representing an element (between whitespaces) from the tweet
    :param stop_words: list of stop word in the desired language
    :return: None or String
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
    element = sub(rb'[%s]+' % escape("""~"'([-|`\_^@)]=}/*-+.$£¨*!:/;,? """.encode()), rb'', element)

    # remove all repetition (more than twice) of the same alphabetic character
    element = sub(rb'(\w)\1+', rb'\1\1', element)

    # check whether the element is relevant or not
    if element in stop_words:
        return None
    else:
        return element


def clean_text(text, stop_words):
    """
    Clean the text from all undesired elements including the stop words in the desired language
    :param text: string to transform in a cleaned list of element
    :param stop_words: list of stop words in the correct language
    :return: list of relevant and cleaned element from the text
    """
    list_cleaned_element = list()
    for element in text.split(rb" "):
        cleaned_element = _clean_element(element, stop_words)
        if cleaned_element:
            list_cleaned_element.append(cleaned_element)
    return list_cleaned_element
