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

input_file_name = 'filename.txt'
num_tweets_post = 3
f = open(input_file_name, 'rb')
data = f.read().split('\n')[:-1]
data = [unidecode(d.strip()) for d in data]
tweet = {}
tweet['data'] = data
min_RT_count = 0
min_fav_count = 0
hashtags = ['#CantGetEnough']
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
    return age<86400

def twitterBOT(api, screen_name, min_RT_count, min_fav_count, hashtags, keywords, num_tweets_post):

    tweets_to_post = tweet['data'][:num_tweets_post]
    tweet['data'] = tweet['data'][num_tweets_post:]
    for status in tweets_to_post:
        try:
            api.update_status(status = unidecode(status))
            print 'Added tweet to timeline', status
        except:
            pass
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    for keyword in keywords:    
    # search for a specific keyword
        firstTime = True
        while True:
            tweets_within_24_hours = []
            if firstTime:
                new_tweets = api.search(q=keyword)
            else:
                new_tweets = api.search(q=keyword, since_id = oldest)
                
            for t in new_tweets:
                if in24Hours(t.created_at):
                    tweets_within_24_hours.append(t)
                    print unidecode(t.text)

            #save most recent tweets
            alltweets.extend(tweets_within_24_hours)

            if len(new_tweets) < 200:
                break
            else:
                firstTime = False
                oldest = new_tweets[-1].id

    for t in alltweets:
        try:
            t.user.follow()
        except:
            pass
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
                try:
                    t.user.unfollow()
                except:
                    pass
        except:
            pass

        if not userExists:
            sql = 'insert into twitter (name, time_followed, following) values ( "' + \
                  unidecode(name) + '", ' +\
                  str(start) + ', 1 );'
            c.execute(sql)
            conn.commit()
        if any(word.lower() in t.text.lower() for word in hashtags):
            if int(t.retweet_count)>= int(min_RT_count):
                print 'int(t.retweet_count)', int(t.retweet_count)
                print 'RTed tweet --- ', unidecode(t.text)
                try:
                    t.retweet()
                except:
                    pass
            if int(t.favorite_count) >= int(min_fav_count):
                print 'int(t.favorite_count)', int(t.favorite_count)
                try:
                    t.favorite()
                except:
                    pass
                print 'Fav-ed tweet --- ', unidecode(t.text)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitterBOT(api, screen_name, min_RT_count, min_fav_count, hashtags, keywords, num_tweets_post)
## scheduler that runs every 24 hours and likes/RTs tweets
sched = BlockingScheduler()
@sched.scheduled_job('interval', hours = 2)
def timed_job():
    twitterBOT(api, screen_name, min_RT_count, min_fav_count, hashtags, keywords, num_tweets_post)
sched.start()
