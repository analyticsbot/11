import tweepy, time, sqlite3
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from text_unidecode import unidecode

## access tokens from twitter
access_token = "746823395220795396-sLrVj7lRe6zoou9TIYMIkvK3xn9Oclr"
access_token_secret = "LuIuSyN9qzX41IoU87x8uBmYzw8IrPFalkVgewbPwNU3M"
consumer_secret = "OHhAWKiO7jmKNs9qYL0ukx6sYC1b9VGEOMYxmIyrbVjrHsHr3d"
consumer_key = "PwiM62T9aCW8e8oIyt5vcdQNg"
screen_name = 'reel_casey'

access_token = "700557896677875713-1g1KoOWEWz7Co6TA3srZCgL5Mv5ZAxw"
access_token_secret = "89qPeMBc6btegSdi9H0QpfOB5gCSSpRD02Hs3KLZhcZBT"
consumer_secret = "8L3E1BYTNT9Qok9KgF5NtewJ7m3Yp4Y1fvUkBWjNMW40Sf9VYo"
consumer_key = "Mw5F8zynR1rfVSyNNLs73Ki5A"
screen_name = 'DeandreaGedding'

min_RT_count = 0
min_fav_count = 0
hashtags = ['Shopping']
keywords = ['#CantGetEnough']

conn = sqlite3.connect('twitterdb.db')
c = conn.cursor()
# Create table
try:
    c.execute('''CREATE TABLE twitter
             (name text, time_followed float, following INT)''')
    conn.commit()
except:
    pass

def in24Hours(d):
    """function to check if the tweet is older than a day/24 hours"""
    age = int(time.time() - (d - datetime(1970,1,1)).total_seconds())
    print age
    return age<200#86400

def twitterBOT(api, screen_name, min_RT_count, min_fav_count, hashtags, keywords):
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    ## store all the tweets made within 24 hours
    tweets_within_24_hours = []

    for keyword in keywords:    
        # search for a specific keyword
        while True:
            try:
                new_tweets = api.search(q=keyword)
                break
            except:
                pass

        
        for t in new_tweets:
            if in24Hours(t.created_at):
                tweets_within_24_hours.append(t)
                print unidecode(t.text)
        
        #save most recent tweets
        alltweets.extend(tweets_within_24_hours)

        ## if there are more tweets within 24 hours
        if len(tweets_within_24_hours) == len(new_tweets):    
            #save the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            continue_ = True
            
            #keep grabbing tweets until there are no tweets left to grab or 24 hour window is crossed
            while (len(new_tweets) > 0) and continue_:                
                    #all subsiquent requests use the max_id param to prevent duplicates
                    while True:
                        try:
                            new_tweets = api.search(q=keyword, since_id  = oldest)
                            break
                        except:
                            pass                    
                    
                    #save most recent tweets
                    alltweets.extend(new_tweets)

                    for t in new_tweets:
                        if in24Hours(t.created_at):
                            tweets_within_24_hours.append(t)
                            print unidecode(t.text)
                        else:
                            continue_ = False
                    
                    #update the id of the oldest tweet less one
                    oldest = alltweets[-1].id - 1
    print len(tweets_within_24_hours), 'len(tweets_within_24_hours)'
    for t in tweets_within_24_hours:
        t.user.follow()
        start = time.time()
        name = t.user.name
        userExists = 0
        try:
            sql1 = 'select name, time_followed, following from twitter where name = "' + str(name) + '"'
            c.execute(sql1)
            rows = fetchone()
            userExists = 1
            time_followed = float(rows[1])
            if start - time_followed > 172800:
                t.user.unfollow()
        except:
            pass

        if not userExists:
            sql = 'insert into twitter (name, time_followed, following) values ( "' + str(name) + '", ' +\
                  str(start) + ', 1 );'
            c.execute(sql)
            conn.commit()
        if any(word.lower() in t.text.lower() for word in hashtags):
            if int(t.retweet_count)> int(min_RT_count):
                print 'int(t.retweet_count)', int(t.retweet_count)
                t.retweet()
            if int(t.favorite_count) > int(min_fav_count):
                print 'int(t.favorite_count)', int(t.favorite_count)
                t.favorite()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitterBOT(api, screen_name, min_RT_count, min_fav_count, hashtags, keywords)
## scheduler that runs every 24 hours and likes/RTs tweets
sched = BlockingScheduler()
@sched.scheduled_job('interval', hours = 2)
def timed_job():
    twitterBOT(api, screen_name, min_RT_count, min_fav_count, hashtags, keywords)
sched.start()
