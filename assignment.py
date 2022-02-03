from os import getcwd
from os.path import join

import tweepy


class TweetCounter:
    def __init__(self, bearer_token: str, all_tweet_query: str, unique_tweet_query: str,
                 all_tweet_file_path: str, unique_tweet_file_path: str,
                 start_time: str, end_time: str):

        self.client                 = tweepy.Client(bearer_token=bearer_token)
        self.total_tweet_query      = all_tweet_query
        self.unique_tweet_query     = unique_tweet_query
        self.total_tweet_file_path  = all_tweet_file_path
        self.unique_tweet_file_path = unique_tweet_file_path
        self.start_time             = start_time
        self.end_time               = end_time

    # fetch tweets in the time period specified
    def get_tweet_data(self, get_unique=False):
        try:
            # open file
            file_path = self.unique_tweet_file_path if get_unique else self.total_tweet_file_path
            tweets_data_file = open(file_path, 'w')

            # get tweets from Twitter's API
            for tweet in tweepy.Paginator(
                    self.client.search_recent_tweets,
                    query=self.unique_tweet_query if get_unique else self.total_tweet_query,
                    tweet_fields=['created_at'],
                    expansions='author_id',
                    start_time=self.start_time,
                    end_time=self.end_time).flatten():

                print(tweet.id, tweet.text)

                # flush to file
                tweets_data_file.write(f'{tweet.id} {tweet.author_id}\n')

            # close file
            tweets_data_file.close()
        except Exception as e:
            print(f'Error = {e.args}')
        return

    # read text file and return content as python list
    @staticmethod
    def _read_text_file(file_path: str):
        """
        :param file_path: Path to file
        :return: Text content
        """
        with open(file_path) as f:
            content = [x.strip() for x in f.readlines()]
        return content

    # read tweets data saved in file and return count
    def get_tweet_count(self, get_unique=False):
        file_path = self.unique_tweet_file_path if get_unique else self.total_tweet_file_path
        try:
            data = self._read_text_file(file_path=file_path)
            if data is not None:
                return len(data)
            return 0
        except Exception as e:
            print(f'Cannot read from path {self.total_tweet_file_path} {e.args}')
        return 0


# file
all_tweets_file_name   = 'all_tweet_data.txt'
unique_tweets_file_name = 'unique_tweet_data.txt'
project_dir = getcwd()  # this will save the file to current working directory

######### NOTE
######### Time period is 12:00 AM Feb 1, 2022 to 12:00 AM Feb 2, 2022 (1 day)
######### Please supply your own bearer token

# initiate counter
tweet_counter = TweetCounter(
    bearer_token='AAAAAAAAAAAAAAAAAAAAAOk9YwEAAAAAwqQ6WY3ylnIGinE9MY6EEn3UQDg%3D0mUgHkMWSusm4OX5cWOlExmuBhy4Ej4P6POs3sRL6Zy5Fd9iPt',
    all_tweet_query='(justin bieber) (music)',
    unique_tweet_query='(justin bieber) (music) -is:retweet',
    all_tweet_file_path=join(project_dir, all_tweets_file_name),
    unique_tweet_file_path=join(project_dir, unique_tweets_file_name),
    start_time='2022-02-01T00:00:00Z',
    end_time='2022-02-02T00:00:00Z'
)

# get all tweets and write to file
tweet_counter.get_tweet_data(get_unique=False)

# get unique tweets and write to file
tweet_counter.get_tweet_data(get_unique=True)

# get all tweets count
total_count = tweet_counter.get_tweet_count(get_unique=False)

# get unique tweets count
unique_count = tweet_counter.get_tweet_count(get_unique=True)

# Upon running this code, you should see counts for the time period selected above
print('\n\n\n')
print(f' TOTAL TWEET COUNT = {total_count}')   # 497
print(f'UNIQUE TWEET COUNT = {unique_count}')  # 166
