from tweepy import StreamListener
from tweepy import OAuthHandler, Stream
from tweepy import API, Cursor
import twitter_credentials
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from textblob import TextBlob
import re,json



class Authenticator:

    def authenticate(self):
        authenticated = OAuthHandler(
            twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        authenticated.set_access_token(
            twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECTRET)
        return authenticated

class TwitterClient:
    def __init__(self,twitter_user=None):
        self.authorizer = Authenticator().authenticate()
        self.client = API(self.authorizer)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.client

    def get_user_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.client.user_timeline,id= self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_home_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.client.home_timeline,id= self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

class TwitterListener(StreamListener):
    """
    A listener class to listen to tweets
    """

    def on_data(self, data):
        print ('getting tweets...')
        json_data = json.loads(data)
        print (json_data['text'])
        return True

    def on_error(self, status):
        raise Exception('Something went wrong. Error code: '+str(status))


class TweetAnalyzer:

    def clean_tweet(self,tweet):
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split()) 
    
    def analyze_sentiments(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'
    
    def tweets_to_dataframe(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['Tweets'])
        df['Created_at'] = np.array([tweet.created_at for tweet in tweets])
        df['Source'] = np.array([tweet.source for tweet in tweets])
        df['User'] = np.array([tweet.user.screen_name for tweet in tweets])
        df['Retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['Liked_count'] = np.array([tweet.favorite_count for tweet in tweets])
        df['Sentiments'] = np.array([self.analyze_sentiments(tweet.text) for tweet in tweets])
        df.set_index('Created_at',inplace=True)
        
        return df

if __name__ == '__main__':
    listener = TwitterListener()
    auth = Authenticator().authenticate()
    hashtag_list = ['#modi']
    stream = Stream(auth, listener)
    stream.filter(track=hashtag_list,async=True)
    # print ('starting next')
    # stream.filter(track=['#python'],async=True)
    # streamer = TwitterStreamer()
    
    # streamer.stream_tweets(hashtag_list)
    # twitter_client = TwitterClient()
    # api = twitter_client.get_twitter_client_api()
    # tweets = api.user_timeline(screen_name='pycon',count=100)
    # df = TweetAnalyzer().tweets_to_dataframe(tweets)
    # neutral_tweets = df['Tweets'].where(df['Sentiments']=='Neutral')
    # print (neutral_tweets)
    # likes = pd.Series(data=df['Liked_count'],index=df.index)
    # retweets = pd.Series(data=df['Retweets'],index=df.index)
    # likes.plot(figsize=(10,5),label='likes',legend=True)
    # retweets.plot(figsize=(10,5),label='likes',legend=True)
    # plt.show()
    