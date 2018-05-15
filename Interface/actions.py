from Data.twitter_collect import collect_tweet, search_sample


def analyse_text(text, kernel):
    pass


def analyse_file(file_content, kernel):
    pass


def analyse_query(query, kernel):
    twitter_sample = search_sample(query)
    pass


def analyse_tweets(nb_tweets, kernel):
    twitter_sample = collect_tweet(nb_tweets)
    pass


def custom_training(nb_tweet_sample, randomised, kernel):
    pass
