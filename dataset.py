number_tweets_each_file = 789314


def get_line_file(number_line, file):
    count_lines, list_tweets = 0, list()
    for line in file:
        count_lines += 1
        list_tweets.append(line)
        number_line -= 1
        if not number_line:
            break
    return count_lines, list_tweets


def get_some_sample(number_tweets):
    with open("./Ressources/Sentiment_analysis_dataset_1.csv", 'rb') as file_part1:
        number_lines, sample_list = get_line_file(number_tweets, file_part1)
        if number_tweets - number_lines:
            with open("./Ressources/Sentiment_analysis_dataset_2.csv", 'rb') as file_part2:
                number_lines_2, sample_list_2 = get_line_file(number_tweets - number_lines, file_part2)
                if number_tweets - (number_lines + number_lines_2):
                    return number_tweets_each_file * 2, sample_list + sample_list_2
                return number_tweets, sample_list + sample_list_2
        return number_tweets, sample_list
