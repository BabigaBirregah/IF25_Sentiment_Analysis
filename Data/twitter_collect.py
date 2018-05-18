# https://pypi.org/project/twitter/
# http://socialmedia-class.org/twittertutorial.html

from twitter import OAuth, Twitter, TwitterStream

from Data.credentials import credentials


def connect_method():
    """
    Collect the credentials and create the method to connect to the Twitter object
    :return: OAuth object with the corresponding credentials
    """
    # you should create a credential function, in a separate file not included to git, returning a tuple
    # (ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET = credentials()
    return OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


def search_sample(query):
    """
    Using the Twitter library we collect some tweets regarding the query
    :param query: word to look for with the twitter API and collect some tweets
    :return:
    """
    return [dic['text'] for dic in Twitter(auth=connect_method()).search.tweets(q=query)['statuses']]


def collect_tweet(nb_tweets=1):
    """
    Collect the desired number of tweets using the Twitter library connecting to the Tweeter API live stream
    :param nb_tweets: number of tweets to collect
    :return:
    """
    twitter_stream = TwitterStream(auth=connect_method())

    only_text = list()
    for msg in twitter_stream.statuses.sample():  # infinite loop
        try:
            if msg['text']:
                only_text.append(msg['text'])
                nb_tweets -= 1
        except:
            pass

        if not nb_tweets:  # to stop the loop when reaching the desired amount of tweets
            break

    return only_text
