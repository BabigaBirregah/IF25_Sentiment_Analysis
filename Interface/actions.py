from Data.twitter_collect import collect_tweet, search_sample


def analyse_text(text, language, kernel, sample_used):
    pass


def analyse_file(file_content, language, kernel, sample_used):
    pass


def analyse_query(query, language, kernel, sample_used):
    twitter_sample = search_sample(query)
    pass


def analyse_tweets(nb_tweets, language, kernel, sample_used):
    twitter_sample = collect_tweet(nb_tweets)
    pass


def custom_training(nb_tweet_sample, randomised, equal_pos_neg, language, kernel):
    pass
