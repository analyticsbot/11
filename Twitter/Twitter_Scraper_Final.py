# -*- coding: utf-8 -*-
import sys
import requests
from lxml.html import fromstring
from lxml.etree import ParserError
import time
import re
from urllib import urlencode
from urlparse import urlunparse
import datetime
import helper_data
from random import choice
import csv
from requests.auth import HTTPProxyAuth
from urllib import urlopen
from concurrent import futures
reload(sys)
sys.setdefaultencoding('utf8')

# Ensuring that ProxyMesh works fine:
print "My current IP address: ", urlopen('http://icanhazip.com').read().strip()
AUTH = requests.auth.HTTPProxyAuth('rlr229@cornell.edu', "{7,UC:86A'j&u.h9")
PROXIES = {'http': 'http://us-dc.proxymesh.com:31280'}
resp = requests.get('http://icanhazip.com', proxies=PROXIES, auth=AUTH, headers=choice(helper_data.browsers))
print "My new IP address via ProxyMesh:", resp.content.strip()
# raw_input("Is it okay with IP addresses? Press enter to start process...\n")

get_min_tweet_pattern = re.compile(r'TWEET-(\d+)-\d+', re.IGNORECASE)


def read_csv(fname):
    with open(fname, 'r') as csvfile:
        result = list(csv.reader(csvfile, quotechar=None))
    return result


def construct_url(query, max_position=None):
    params = {
        'f': 'tweets',
        'vertical': 'default',
        'src': 'typd',
        'q': query
    }
    # max_position looks like TWEET-{0}-{1}'  # 0 - oldest tweet, 1 - recent tweet
    if max_position:
        params['max_position'] = max_position

    url_tupple = ('https', 'twitter.com', '/i/search/timeline', '', urlencode(params), '')
    url = urlunparse(url_tupple)
    print url
    return url


def get_html(url, rate_delay):
    time.sleep(rate_delay)
    while True:
        try:
            resp = requests.get(url, proxies=PROXIES, auth=AUTH, headers=choice(helper_data.browsers))
            return resp.json()
        except Exception as e:
            print "Couldn't get response from twitter site. Reconnecting after 10 seconds."
            print e
            time.sleep(10)


def get_initial_max_min_tweet_id(response_html):
    """
    Parses first page with results, gets max_tweet_id and last_tweet_id from that page.
    :param response_html: first page with results
    """
    parsed_body = fromstring(response_html["items_html"])
    tweets = parsed_body.xpath('//li[@data-item-type="tweet"]')
    old_tweet = tweets[-1].xpath('@data-item-id')[0]
    try:
        max_tweet = tweets[0].xpath('.//@data-retweet-id')[0]
    except IndexError:
        max_tweet = tweets[0].xpath('@data-item-id')[0]

    return old_tweet, max_tweet


def get_tweets(response_html):
    output_tweets = []
    parsed_body = fromstring(response_html["items_html"])
    tweets = parsed_body.xpath('//li[@data-item-type="tweet"]')
    print "Tweets in page:", len(tweets)
    for li in tweets:
        tweet = {
            'tweet_id': li.xpath('@data-item-id')[0],
            'text': None,
            'user_id': None,
            'user_screen_name': None,
            'user_name': None,
            'created_at': None,
            'retweets': 0,
            'favorites': 0,
            'location': None,
            'location_text': None
        }

        # Tweet Text
        try:
            text = li.xpath('.//p[@class="TweetTextSize  js-tweet-text tweet-text"]')[0]
            text = text.text_content().strip()
            tweet['text'] = text
        except IndexError:
            pass

        # Tweet User ID, User Screen Name, User Name
        try:
            user_id = li.xpath('.//a/@data-user-id')[0]
            tweet['user_id'] = user_id.strip()
        except IndexError:
            pass
        try:
            user_name = li.xpath('.//@data-screen-name')[0]
            tweet['user_name'] = user_name.strip()
        except IndexError:
            pass
        try:
            user_screen_name = li.xpath('.//@data-name')[0]
            tweet['user_screen_name'] = user_screen_name.strip()
        except IndexError:
            pass

        # Tweet Created At
        try:
            created_date = li.xpath('.//span/@data-time-ms')[0]
            tweet['created_at'] = float(created_date)
        except IndexError:
            pass

        # Tweet Retweets, Tweet Favourites
        try:
            retweets_count = li.xpath('.//span/@data-tweet-stat-count')
            tweet['retweets'] = retweets_count[0]

            favourites_count = retweets_count[1]
            tweet['favorites'] = favourites_count
        except IndexError:
            pass

        # Tweet location
        try:
            twitter_location = li.xpath('.//a/@data-place-id')[0]
            tweet['location'] = twitter_location
        except IndexError:
            pass

        # Tweet Geolocation
        try:
            tweet_geolocation = li.xpath('.//span[contains(@class, "Tweet-geo")]/@title')[0]
            tweet['location_text'] = tweet_geolocation
        except IndexError:
            pass

        output_tweets.append(tweet)
    return output_tweets


class TweetsHandler:
    def __init__(self, file_name, max_tweets, query, csv_file):
        self.counter = 0
        self.file_name = file_name
        self.query = query
        self.csv_file = csv_file
        self.max_tweets = max_tweets
        self.csv_file.write(self.query)
        self.csv_file.write("\n\n")

    def save_tweets(self, tweets_list):
            for tweet in tweets_list:
                self.counter += 1

                if tweet['created_at'] is not None:
                    t = datetime.datetime.fromtimestamp((tweet['created_at']/1000))
                    fmt = "%Y-%m-%d %H:%M:%S"
                    self.csv_file.write('{0},{1},"{2}",{3},{4},{5},{6},"{7}"\n'.format(
                        self.counter, tweet['user_id'], tweet['user_name'],
                        tweet['retweets'], tweet['favorites'], tweet['location'], t.strftime(fmt),
                        tweet['text']))

                    print "%i [%s] - %s" % (self.counter, t.strftime(fmt), tweet['text'])

                if self.counter == self.max_tweets:
                    return False
            return True


def search_tweets(file_name, query, max_tweets, rate_delay, error_delay):
    """
    Request string from CSV file must be in comma-separated format:
    for example 'budweiser', "budweiser lang:en since:2016-02-05 until:2016-02-09"
    Where first part 'budweiser' is future output csv file name.
    """
    with open("Massive_Pt3/%s.csv" % file_name, "wb") as csv_file:
        # Some initials
        continue_search = True
        request_url = construct_url(query)
        response_html = get_html(request_url, rate_delay)
        json_without_tweets = 0

        # If we have no results then stop executing
        try:
            old_tweet, max_tweet = get_initial_max_min_tweet_id(response_html)
        except Exception as p:
            tweets_handler = TweetsHandler(file_name, max_tweets, query, csv_file)
            tweets_handler.save_tweets([])
            print "We don't have tweets on response or something goes wrong"
            print "Query is: {0}, URL is: {1}".format(query, request_url)
            print p
            return

        print "Initial Recent Tweet is:", max_tweet
        print "Initial Oldest Tweet is:", old_tweet

        tweets_handler = TweetsHandler(file_name, max_tweets, query, csv_file)

        while continue_search:
            # Get tweets from page
            try:
                tweets = get_tweets(response_html)
            except ParserError:
                print "We have json without tweets. It seems we don't have any tweets anymore or new tweets will be on the next page..."
                print "Query is: {0}, URL is: {1}".format(query, request_url)
                # Trying to obtain new tweets after empty json page
                next_page_position = response_html["min_position"]
                next_page_position = re.search(get_min_tweet_pattern, next_page_position).group(1)
                max_position = 'TWEET-{0}-{1}'.format(next_page_position, max_tweet)
                next_page_url = construct_url(query, max_position)
                response_html = get_html(next_page_url, rate_delay)
                json_without_tweets += 1
                if json_without_tweets >= 100000:
                    break
                continue

            # Save tweets
            continue_search = tweets_handler.save_tweets(tweets)

            max_position = 'TWEET-{0}-{1}'.format(old_tweet, max_tweet)
            next_page_url = construct_url(query, max_position)
            response_html = get_html(next_page_url, rate_delay)

            # Lets find next_page_position - it is a next page in pagination
            next_page_position = response_html["min_position"]
            next_page_position = re.search(get_min_tweet_pattern, next_page_position).group(1)

            # This logic can be realized only after deep research of json responses from twitter about positions
            if old_tweet != next_page_position:
                old_tweet = next_page_position
                print
                continue
            else:
                print "We reached end of pages, or tweets on site"
                break


def main():
    """
    Launches main process with multithreading handler.
    Parameters possible to change: rate_delay, error_delay, max_tweets, searches(list of keywords to search),
    num_of_threads(number of simultaneous threads)
    """
    searches = read_csv('Test.csv')
    max_tweets = 100000000
    rate_delay = 0
    error_delay = 10
    num_of_threads = 5

    with futures.ProcessPoolExecutor(max_workers=num_of_threads) as pool:
        for csv_row in searches:
            # csv_row[0] - file_name to be saved as csv output;
            # csv_row[1] - query string for searching tweets
            pool.submit(search_tweets, csv_row[0], csv_row[1], max_tweets, rate_delay, error_delay)


def w_o_mp_main():
    """
    Launches main process without multithreading handler.
    Parameters possible to change: rate_delay, error_delay, max_tweets, searches(list of keywords to search),
    num_of_threads(number of simultaneous threads)
    Usually using for debugging
    """
    searches = read_csv('Test.csv')
    max_tweets = 100000000
    rate_delay = 0
    error_delay = 10

    for csv_row in searches:
        # csv_row[0] - file_name to be saved as csv output;
        # csv_row[1] - query string for searching tweets
        search_tweets(csv_row[0], csv_row[1], max_tweets, rate_delay, error_delay)


if __name__ == '__main__':
    main()
    # w_o_mp_main()


    # Debug
    # search_tweets('budweiser', "budweiser lang:en since:2016-02-05 until:2016-02-09", 100, 0, 10)
    # search_tweets('uzynagash', 'Uzynagash', 100, 0, 10)
