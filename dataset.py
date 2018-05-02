from os import getcwd

number_tweets_each_file = 789314


# TODO: clean the lines to get only the text and the labelled (positive/negative feeling) from the file
def clean_lines(line):
    pass


def get_lines_file(number_line, file):
    """
    Collect the desired amount of line in the file
    :param number_line: <= total number of lines in the file
    :param file: file object separated by line
    :return: list of tuple containing the labelled of the text and the text of the tweet
    """
    count_lines, list_tweets = 0, list()
    for line in file:
        count_lines += 1
        list_tweets.append(clean_lines(line))
        number_line -= 1
        if not number_line:
            break

    return count_lines, list_tweets


def get_some_sample(number_tweets):
    """
    Collect from our data sets the desired amount of tweets
    :param number_tweets: number of tweets to collect
    :return: tuple of actual number of tweets collected and the list of tweets
    """
    # data set csv file : ItemID,Sentiment,SentimentSource,SentimentText
    # TODO: maybe use csv library to read and treat the file
    with open(getcwd() + "/Ressources/Sentiment_analysis_dataset_1.csv", 'rb') as file_part1:
        number_lines, sample_list = get_lines_file(number_tweets, file_part1)
        if number_tweets - number_lines:
            with open(getcwd() + "/Ressources/Sentiment_analysis_dataset_2.csv", 'rb') as file_part2:
                number_lines_2, sample_list_2 = get_lines_file(number_tweets - number_lines, file_part2)
                if number_tweets - (number_lines + number_lines_2):
                    return number_tweets_each_file * 2, sample_list + sample_list_2
                else:
                    return number_tweets, sample_list + sample_list_2

        return number_tweets, sample_list
