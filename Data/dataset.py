from secrets import randbelow

from numpy import array

from Classifier.features import characteristic_vector
from Data.clean_data import clean_end_line, clean_text
from Ressources.resource import get_correct_stop_word
from Ressources.resource import get_path_resource

NB_TWEETS_PER_FILE = 789314
NB_TOTAL_POSITIVE_TWEETS = 790185
NB_TOTAL_NEGATIVE_TWEETS = 788442


def clean_line(line):
    """
    The line of the sample is constructed like this :
        Number_line,label_sentiment,Sentiment140,text_tweet
        Number_line,label_sentiment,Kaggle,text_tweet
    We need to extract the label and the text only
    :param line: line extracted from the data set
    :return: tuple containing the label and the text
    """
    try:
        label, text = line.split(b',Sentiment140,')
    except:
        label, text = line.split(b',Kaggle,')
    return label.split(b',')[1], clean_end_line(text)


def _get_lines_file(number_line, file):
    """
    Collect the desired amount of line in the file
    :param number_line: total number of lines to collect from the file
    :param file: file object separated by line
    :return: list of tuple containing the labelled of the text and the text of the tweet
    """
    count_lines, list_tweets = 0, list()
    for line in file:
        count_lines += 1
        list_tweets.append(clean_line(line))
        number_line -= 1
        if not number_line:
            break

    return count_lines, list_tweets


def get_some_sample(number_tweets=12):
    """
    Collect from our data sets the desired amount of tweets
    :param number_tweets: number of tweets to collect
    :return: tuple of actual number of tweets collected and the list of tweets
    """
    # data set csv file : ItemID,Sentiment,SentimentSource,SentimentText
    number_tweets = min(number_tweets, 2 * NB_TWEETS_PER_FILE)
    with open(get_path_resource('Sentiment_analysis_dataset_1.csv'), 'rb') as file_part1:
        number_lines, sample_list = _get_lines_file(number_tweets, file_part1)
        if number_tweets - number_lines:
            with open(get_path_resource('Sentiment_analysis_dataset_2.csv'), 'rb') as file_part2:
                number_lines_2, sample_list_2 = _get_lines_file(number_tweets - number_lines, file_part2)
                if number_tweets - (number_lines + number_lines_2):
                    return NB_TWEETS_PER_FILE * 2, sample_list + sample_list_2
                else:
                    return number_tweets, sample_list + sample_list_2

    return number_tweets, sample_list


def get_positive_tweets(sample_list):
    """
    From a sample list (the list returned by get_some_sample) containing tuples of label and text of a tweet,
    return only the positive tweets
    :param sample_list: list of tuples containing label and text of a tweet
    :return: list of text of tweets from the positive tweets
    """
    return [x[1] for x in sample_list if x[0] == b'1']


def get_negative_tweets(sample_list):
    """
    From a sample list (the list returned by get_some_sample) containing tuples of label and text of a tweet,
    return only the negative tweets
    :param sample_list: list of tuples containing label and text of a tweet
    :return: list of text of tweets from the negative tweets
    """
    return [x[1] for x in sample_list if x[0] == b'0']


def get_positive_negative_tweets(sample_list):
    """
    From a sample list (the list returned by get_some_sample) containing tuples of label and text of a tweet,
    return 2 lists containing the text only
    :param sample_list: list of tuples containing label and text of a tweet
    :return: 2 lists of text, first one containing the negatives, second the positive
    """
    positive, negative = list(), list()
    for tuple in sample_list:
        if tuple[0] == b'1':
            positive.append(tuple[1])
        else:
            negative.append(tuple[1])
    return negative, positive


def get_randomised_sample(number_tweets=12):
    """
    Get some random tweets from the whole data set
    :param number_tweets: Number of tweets to collect up to the total number of tweets
    :return: sample_list containing the line from the data set
    """
    number_tweets = min(number_tweets, 2 * NB_TWEETS_PER_FILE)
    sample_list = list()
    with open(get_path_resource('Sentiment_analysis_dataset_1.csv'), 'rb') as file_part1:
        with open(get_path_resource('Sentiment_analysis_dataset_2.csv'), 'rb') as file_part2:
            global_file = file_part1.readlines() + file_part2.readlines()
            while number_tweets:
                sample_list.append(clean_line(global_file.pop(randbelow(len(global_file)))))
                number_tweets -= 1
    return sample_list


def get_randomised_pos_neg_sample(num_pos=12, num_neg=12):
    """
    Get two lists of negative and positive texts from the labelled tweets in the whole data set up to the number of
    positive and negative tweets contained in the data set
    :param num_pos: number of positive tweets to collect up to the total number of positive tweets in the data set
    :param num_neg: number of negative tweets to collect up to the total number of negative tweets in the data set
    :return: 2 lists containing negative texts and positive texts from the tweets in the data set
    """
    num_pos = min(num_pos, NB_TOTAL_POSITIVE_TWEETS)
    num_neg = min(num_neg, NB_TOTAL_NEGATIVE_TWEETS)
    positives, negatives = list(), list()
    with open(get_path_resource('Sentiment_analysis_dataset_1.csv'), 'rb') as file_part1:
        with open(get_path_resource('Sentiment_analysis_dataset_2.csv'), 'rb') as file_part2:
            global_file = file_part1.readlines() + file_part2.readlines()
            while num_pos or num_neg:
                element = clean_line(global_file.pop(randbelow(len(global_file))))
                if element[0] == b'1' and num_pos:
                    positives.append(element[1])
                    num_pos -= 1
                elif num_neg:
                    negatives.append(element[1])
                    num_neg -= 1
    return negatives, positives


def _count_pos_neg_sample():
    """
    Method to compute the number of positive and negative sample contained in our data set
    :return: None, print the number of negative tweets, positive tweets and total tweets counted
    """
    count_pos, count_neg, number_tweets = 0, 0, 2 * NB_TWEETS_PER_FILE - 1
    with open(get_path_resource('Sentiment_analysis_dataset_1.csv'), 'rb') as file_part1:
        with open(get_path_resource('Sentiment_analysis_dataset_2.csv'), 'rb') as file_part2:
            global_file = file_part1.readlines() + file_part2.readlines()
            while number_tweets:
                number_tweets -= 1
                if global_file.pop().split(b',Sentiment140,')[0].split(b',')[1] == b'1':
                    count_pos += 1
                else:
                    count_neg += 1
    print(count_neg, count_pos, count_neg + count_pos)


def get_characteristic_label_vectors(nb, randomness, pos_equal_neg, Resource, bypass=False, language='en'):
    """
    Collect the desired number of label vectors regarding the parameters given. Provide 2 booleans to get a
    collection randomised or not and equal in number of positive and negative vector, or not.
    :param nb: number of vector to collect
    :param randomness: if the collection should be randomised among all the tweets in the sample
    :param pos_equal_neg: if we want the same amount of positive and negative vectors
    :param Resource: class object containing all the resources (positive words, negative words, positive emoticons,
    negative emoticons, stop words)
    :param bypass: False or True
        False : if we only want non null vector
        True : if we want tweets only, with the corresponding eventually null vector
    :param language: Choose the language from french to english
        'fr' | 'en'
    :return: tuple of array containing the features vectors and labels vectors corresponding
    """
    m_features, m_labels = list(), list()
    nb_pos, nb_neg, nb_tweet = 0, 0, 0
    with open(get_path_resource('Sentiment_analysis_dataset_1.csv'), 'rb') as file_part1:
        with open(get_path_resource('Sentiment_analysis_dataset_2.csv'), 'rb') as file_part2:
            global_file = file_part1.readlines() + file_part2.readlines()
            while nb_tweet < nb:
                if randomness:
                    label, text = clean_line(global_file.pop(randbelow(2 * NB_TWEETS_PER_FILE - nb_tweet)))
                else:
                    label, text = clean_line(global_file.pop())
                feature_vector = characteristic_vector(clean_text(text, get_correct_stop_word(Resource, language)),
                                                       Resource)
                if feature_vector != [0, 0, 0, 0, 0] or bypass:
                    float_label = float(label)
                    if pos_equal_neg:
                        if float_label == 0.0 and nb_neg < nb // 2 or float_label == 1.0 and nb_pos < nb // 2:
                            m_features.append(feature_vector)
                            m_labels.append(float_label)
                            nb_tweet += 1
                            if float(label) == 1.0:
                                nb_pos += 1
                            else:
                                nb_neg += 1
                    else:
                        m_features.append(feature_vector)
                        m_labels.append(float_label)
                        nb_tweet += 1
    return array(m_features), array(m_labels)
