from secrets import randbelow

from Data.clean_data import clean_end_line
from Ressources.resource import get_path_resource

number_tweets_each_file = 789314
total_positive_tweets = 790185
total_negative_tweets = 788442


def clean_line(line):
    """
    The line of the sample is constructed like this :
        Number_line,label_sentiment,Sentiment140,text_tweet
    We need to extract the label and the text only
    :param line: line extracted from the data set
    :return: tuple containing the label and the text
    """
    try:
        label, text = line.split(b',Sentiment140,')
    except:
        label, text = line.split(b',Kaggle,')
    return (label.split(b',')[1], clean_end_line(text))


def get_lines_file(number_line, file):
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
    # TODO: maybe use csv library to read and treat the file
    number_tweets = min(number_tweets, 2 * number_tweets_each_file)
    with open(get_path_resource('Sentiment_analysis_dataset_1.csv'), 'rb') as file_part1:
        number_lines, sample_list = get_lines_file(number_tweets, file_part1)
        if number_tweets - number_lines:
            with open(get_path_resource('Sentiment_analysis_dataset_2.csv'), 'rb') as file_part2:
                number_lines_2, sample_list_2 = get_lines_file(number_tweets - number_lines, file_part2)
                if number_tweets - (number_lines + number_lines_2):
                    return number_tweets_each_file * 2, sample_list + sample_list_2
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
    number_tweets = min(number_tweets, 2 * number_tweets_each_file)
    sample_list = list()
    with open(get_path_resource('Sentiment_analysis_dataset_1.csv'), 'rb') as file_part1:
        with open(get_path_resource('Sentiment_analysis_dataset_2.csv'), 'rb') as file_part2:
            global_file = file_part1.readlines() + file_part2.readlines()
            while number_tweets:
                sample_list.append(global_file.pop(randbelow(len(global_file))))
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
    num_pos = min(num_pos, total_positive_tweets)
    num_neg = min(num_neg, total_negative_tweets)
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


def count_pos_neg_sample():
    """
    Method to compute the number of positive and negative sample contained in our data set
    :return: None, print the number of negative tweets, positive tweets and total tweets counted
    """
    count_pos, count_neg, number_tweets = 0, 0, 2 * number_tweets_each_file - 1
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
