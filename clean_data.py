# http://www.lextek.com/manuals/onix/stopwords1.html : english stop words
# https://www.ranks.nl/stopwords/french : french stop words
# http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip : labelled tweets data set
# https://www.w3.org/community/sentiment/wiki/Datasets : emoticon Lexicon dictionary among others
# https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107 : english positive and negative words

import re


def load_stop_word(language='fr'):
    if language == 'fr':
        with open('../stop_word_fr.txt', 'r') as file_stop_word:
            stop_word = file_stop_word.readlines()
        return stop_word
    elif language == 'en':
        with open('../stop_word_en.txt', 'r') as file_stop_word:
            stop_word = file_stop_word.readlines()
        return stop_word


def load_positive_word(language='en'):
    if language == 'fr':
        with open('../positive_word_fr.txt', 'r') as file_positive_word:
            positive_word = file_positive_word.readlines()
        return positive_word
    if language == 'en':
        with open('../positive_word_en.txt', 'r') as file_positive_word:
            positive_word = file_positive_word.readlines()
        return positive_word


def load_emoticons_scores():
    emoticon_dict = dict()
    with open('../EmoticonSentimentLexicon.txt') as emoticons_file:
        for key, value in emoticons_file.readline().split('sep'):
            emoticon_dict[key] = value
    return emoticon_dict


def clean_element(element, language='fr'):
    element = element.lower()
    if re.match(r'#\w+', element):
        element = re.sub('#', '', element)
    elif re.match(r'@\w+', element) or re.match(r'http.+', element):
        return None
    elif re.match('[%s]+' % re.escape("""~"'([-|`\_^@)]=}/*-+.$£¨*!:/;,? """), element):
        element = re.sub('[%s]+' % re.escape("""~"'([-|`\_^@)]=}/*-+.$£¨*!:/;,? """), '', element)
    element = re.sub(r'(\w)\1+', r'\1', element)
    if element in load_stop_word(language):
        return None
    else:
        return element


def clean_text(text, language):
    list_cleaned_element = list()
    for element in text.split(" "):
        cleaned_element = clean_element(element, language)
        if cleaned_element:
            list_cleaned_element.append(cleaned_element)
