import pandas as pd
import tweepy
import time
import json
api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
api_key_secret ="xxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret ="xxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
bearer_token = r"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# Getting authentication done through our developer created app
client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)
class Tweets_Listener(tweepy.StreamingClient):
    def on_connect(self):
        print("connected successfully")
    stop_time=time.time()+60
    tweets=[]
    def on_tweet(self,tweet):
        if tweet.referenced_tweets==None:
            self.tweets.append(tweet.text)
            #print(type(tweet.text))
            time.sleep(0.5)
        if(time.time()>self.stop_time):
            #Just want to stop retrieving the tweets after 60seconds 
            self.disconnect()
            print("One minute completed")
#### creating object for our designed class
stream_tweets_extractor = Tweets_Listener(bearer_token=bearer_token)
keywords=["cricket"] #If we want, we can add more keywords
for rule in stream_tweets_extractor.get_rules()[0]:
    stream_tweets_extractor.delete_rules(rule.id)
for keyword in keywords:
    #adding a rule, to extract only the tweets that contains keyword politics
    stream_tweets_extractor.add_rules(tweepy.StreamRule(keyword)) 
#Here we make sure to discard the referenced tweets. re-tweets
stream_tweets_extractor.filter(tweet_fields=["referenced_tweets"])
print("The number of tweets obtained in one minute time duration:",
      len(stream_tweets_extractor.tweets))
#creating a DataFrame with list of tweets obtained from real-time twitter streams
df_tweets = pd.DataFrame(stream_tweets_extractor.tweets,columns=["Tweets obtained in 60 seconds/ one minute"])
#Creating and storing the retrieved data in a json file.
df_tweets.to_json("D:\Michigan_State_University_Works\CSE_482\Exercises\exercise-2\msu.json")
## Retrieving data from json file, cross-checking the data which we stored in "msu.json" file
df_tweets = pd.read_json("D:\Michigan_State_University_Works\CSE_482\Exercises\exercise-2\msu.json")
#Just checking one tweet, whether cricket keywords exists or not!!! Yes it is there
df_tweets.iloc[0,0]

