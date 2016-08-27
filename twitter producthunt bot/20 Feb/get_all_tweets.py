import tweepy #https://github.com/tweepy/tweepy
import csv, sqlite3, requests, random, logging, re
from apscheduler.schedulers.blocking import BlockingScheduler

#Twitter API credentials
access_key = "4415348663-5pNNm5YQLmGrBMwWuJ1yObWbaESTIw1fNSPPDA9"
access_secret = "gafJtISvaAdfUWuc9xsSpY2R1rHu5ICbhQEMDmqG8SWT3"
consumer_secret = "1Qhn2zclLLAs82mQPEKeThJbS5CdCyYYsWtVvQi7S4oVCDdFJU"
consumer_key = "6FiPNQ2wpHQSiBB58m31V0l1v"

## initializing the scheduler class
sched = BlockingScheduler()

## function to get the list of proxies
def getProxies():
    proxy = []
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    html = response.content

    templs = re.findall(r'<tr><td>(.*?)</td><td>', html)
    templs2 = re.findall(r'</td><td>[1-99999].*?</td><td>', html)

    for i in range(len(templs)):
        ip = (templs[i] + ":" + templs2[i].replace('</td><td>', ''))
        proxy = 'http://' + ip
        if requests.get('https://api.ipify.org', proxies = {'http':proxy}).content == proxy:
            proxy.append(proxy)
    print('Total proxies downloaded', len(proxy))


def get_all_tweets(screen_name, c, conn):
    proxies_list = getProxies()
    ## delete all records
    c.execute('DELETE * FROM links;')
    conn.commit()

    #Twitter only allows access to a users most recent 3240 tweets with this method
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []	

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #transform the tweepy tweets into a 2D array that will populate the csv	
    outtweets = [tweet.text.encode("utf-8") for tweet in alltweets]

    links = []

    for tweet in outtweets:
            t = tweet.split()
            for i in t:
                    if 'http' in i:
                        try:
                            proxies = {'http': random.choice(proxies_list)}
                            r = requests.get(i, proxies=proxies)
                            if 'x-twitter-response-tags' not in r.headers.keys():
                                    links.append(i)
                                    c.execute("SELECT link from links")
                                    rows = c.fetchone()
                                    if rows == None:
                                        print i
                                        c.execute("INSERT INTO links (link) values(?)", (i, ))
                                        conn.commit()
                        except:
                            pass



if __name__ == '__main__':     
    ## initialize the scheduler option. this is based on the local machine time
    ## runs at midnight 01-44-40
    sched.configure({'misfire_grace_time': 1000})
    @sched.scheduled_job('cron', hour=01, minute=44, second=40)
    def timed_job():
        logging.basicConfig()
        print 'starting the job'
        conn = sqlite3.connect('producthunt_links.db', check_same_thread = False)
        print "[+] Opened database connection successfully"
        c = conn.cursor()

        ## try to create the table if it does not exists
        try:
            c.execute("create table links(link TEXT);")
            conn.commit()
        except:
            pass
        get_all_tweets("ProductHunt", c, conn)

        # close the connection
        c.close()
        conn.close()
        
    sched.start()

	
