from selenium import webdriver
from random import choice
import sqlite3, logging, requests, os,multiprocessing, subprocess
from time import localtime, strftime
import smtplib, random, time
from threading import Thread
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)
driver = webdriver.Firefox()
twitter_login_url = 'https://twitter.com/login/'

NUM_BOT_USE = 1 ## number of twitter ids to use for upvoting content
NUM_UPVOTES_PRODUCT_HUNT = random.randint(2,3) ## number of upvotes on product hunt
HANDLE = 'Codeology' ## handle or product that has to be always upvoted 
NUM_TRENDS = 1 ## number of trends on twitter the bot should interact
NumTweets = 5
username, password, email = 'meSamspro', 'iexahgh5Yo', 'ThomeCaroliexah@outlook.com'
#username, password, email = 'MeEarnest88', 'Oojoh3cahru', 'WhitehCynthiOojoh@outlook.com'
driver.get(twitter_login_url)
logging.info("Logging into the twitter account ")
email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
email_elem.send_keys(username)
pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
pwd_elem.send_keys(password)

pwd_elem.submit()

try:
    if 'Help us keep your account safe' in driver.page_source and 'phone' not in driver.page_source:
        email_elem = driver.find_element_by_id('challenge_response')
        email_elem.send_keys(email)
        email_elem.submit()
except:
    pass

try:
    if 'phone' in driver.page_source:
        email_elem = driver.find_element_by_id('challenge_response')
        email_elem.send_keys('9164001460')
        email_elem.submit()
except:
    pass
    
time.sleep(2)
logging.info("Successfully logged into the twitter account ")
trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item')
logging.info("Number of trends to play with :: " + str(NUM_TRENDS))
num_trends = 0
while True:
    num_trends +=1
    if num_trends>NUM_TRENDS:
        break
    time.sleep(5)
    try:
        trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item.context-trend-item')
            
    except:
        try:
            trend_elem = driver.find_elements_by_css_selector('.js-nav.trend-name')
        except:
            pass
    choice(trend_elem).find_element_by_tag_name('a').click()
    time.sleep(5)
    numTweets = 0
    g = driver.find_elements_by_css_selector('.js-tweet-text-container')
    for i in g:
        i.click()
        try:
            time.sleep(1)
            a = driver.find_element_by_css_selector('.permalink-inner.permalink-tweet-container')
            b = a.find_element_by_css_selector('.ProfileTweet-actionButton.js-actionButton.js-actionRetweet')
            b.click()
            driver.find_element_by_css_selector('.btn.primary-btn.retweet-action').click()
            a.find_element_by_css_selector('.button-text.follow-text').click()
            numTweets +=1
        except:
            pass
        f = driver.find_element_by_css_selector('#permalink-overlay')
        f.click()
        time.sleep(1)
        if numTweets>NumTweets:
            break
    
## go to homepage
try:
    driver.find_element_by_css_selector('#global-nav-home').find_element_by_tag_name('a').click()
    logging.info("Moving to homepage to do the next action")
except:
    driver.get('https://twitter.com/')

time.sleep(1)

## tweet some stuff
tweets = ['Gotta go', 'SVG Star Wars Land Speeder - https://t.co/rxVatdUzU0 via @awebdesignnews',\
          '@PythonEcuador @tin_nqn_ @patovala @manuelmax  https://t.co/meJWRqQBqF',\
          'RT @pycoders: himawaripy - Put near-realtime picture of Earth as your desktop background https://t.co/20TRp7kimH #python']
try:
    for tweet in tweets:
        time.sleep(1)
        elem_tweet_box = driver.find_element_by_xpath('//*[@id="tweet-box-home-timeline"]')
        elem_tweet_box.clear()
        time.sleep(1)
        elem_tweet_box.send_keys(tweet)
        tweet_click_box = driver.find_element_by_xpath("//*[@id=\"timeline\"]/div[2]/div/form/div[2]/div[2]/button/span[1]/span")
        tweet_click_box.click()
        time.sleep(1)
except Exception,e:
    pass
## follow some random people
try:
    account_elem = driver.find_element_by_css_selector('.flex-module')
    accounts_to_follow = account_elem.find_elements_by_css_selector('.js-account-summary.account-summary.js-actionable-user')
    for account in accounts_to_follow:
        follow_btn = account.find_element_by_css_selector('.small-follow-btn.follow-btn.btn.small.follow-button.js-recommended-item')
        follow_btn.click()
except Exception,e:
    pass
time.sleep(2)
try:
    driver.find_element_by_id('user-dropdown-toggle').click()
    driver.find_element_by_id('signout-button').click()
except:
    pass
