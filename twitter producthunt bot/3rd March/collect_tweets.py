#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sqlite3, datetime
from unidecode import unidecode
import csv, sqlite3, requests, random, logging, re
from apscheduler.schedulers.blocking import BlockingScheduler

#Twitter API credentials
access_token = "4415348663-5pNNm5YQLmGrBMwWuJ1yObWbaESTIw1fNSPPDA9"
access_token_secret = "gafJtISvaAdfUWuc9xsSpY2R1rHu5ICbhQEMDmqG8SWT3"
consumer_secret = "1Qhn2zclLLAs82mQPEKeThJbS5CdCyYYsWtVvQi7S4oVCDdFJU"
consumer_key = "6FiPNQ2wpHQSiBB58m31V0l1v"

conn = sqlite3.connect('botdb.db', check_same_thread = False)
print "[+] Opened database connection successfully"
c = conn.cursor()

## initializing the scheduler class
sched = BlockingScheduler()

## try to create the table if it does not exists
try:
    c.execute("create table tweets(tweet TEXT);")
    conn.commit()
except:
    pass

class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0
        now = datetime.datetime.now()
        if datetime.time(now.hour, now.minute, now.second) == datetime.time(01, 49, 32):
            self.num_tweets = 0
        
    
    def on_status(self, status):
        # Print the tweet
        tweet = status.text
        
        if self.num_tweets < 500:
            c.execute("INSERT INTO tweets (tweet) values(?)", (unidecode(tweet), ))
            conn.commit()
            return True
        else:
            return False

    def on_error(self, status_code):
        #print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        return True


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby', 'Get Investors', 'producthunt', 'influential people', 'next big thing', 'addicting app'])
