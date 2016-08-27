from selenium import webdriver
from random import choice
import sqlite3, logging, requests, os,multiprocessing, subprocess
from time import localtime, strftime
import smtplib, random, time
from threading import Thread
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)


twitter_login_url = 'https://twitter.com/login/'

NUM_BOT_USE = 49 ## number of twitter ids to use for upvoting content
NUM_TRENDS = 5 ## number of trends on twitter the bot should interact
NumTweets = 20
## send an email with updated ip address or errors
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'product.hunt.bot12@gmail.com'
MAIL_PASSWORD = 'producthunt1234'
TO_EMAIL = 'product.hunt.bot12@gmail.com'

## function to send an email
def sendMail(msg):
    try:
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)     
        server.sendmail(MAIL_USERNAME, TO_EMAIL, msg)
        server.quit()
        return True
    except Exception,e:
        return False

## connect to account db
try:
    conn_account = sqlite3.connect('accounts.db', check_same_thread = False)
    c_account = conn_account.cursor()
    print "[+] Opened accounts database connection successfully"
except:
    print "[+] Error in opening accounts database connection"
#id, Gender, Name, Username, Password, Location ,Email, Recovery_Mail, Bio

## connect to tweets db
try:
    conn_tweets = sqlite3.connect('tweets.db', check_same_thread = False)
    c_tweets = conn_tweets.cursor()
    print "[+] Opened tweets database connection successfully"
except:
    print "[+] Error in opening tweets database connection"

## function to get the twitter credentials
def getTwitterCredetials(id):
    c_account.execute('SELECT Username, Password, Bio, Location, Email, Phone from accounts where id = ' + str(id))
    rows = c_account.fetchone()
    try:
        return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"',''), rows[4].replace('"',''), rows[5].replace('"','')
    except:
        return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"',''), rows[4].replace('"',''), rows[5]

## function to get tweets
def getTweets(c_tweets):
    c_tweets.execute("SELECT * FROM tweets ORDER BY RANDOM() LIMIT 5")
    rows = c_tweets.fetchall()
    return rows

## function to interact with twitter. like, RT, follow, trends
def TwitterAction(username, password, c_tweets, NUM_TRENDS, NumTweets, twitter_login_url, email, phone):
    driver = webdriver.Firefox()
    driver.get(twitter_login_url)
    email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
    email_elem.send_keys(username)
    pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
    pwd_elem.send_keys(password)

    pwd_elem.submit()
    time.sleep(random.randint(2,5))
    

    ## unlock account if blocked
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
            email_elem.send_keys(phone)
            email_elem.submit()
    except:
        pass

    num_tweets_acc = driver.find_elements_by_css_selector('.ProfileCardStats-statValue')[0].text
    num_acc_following = driver.find_elements_by_css_selector('.ProfileCardStats-statValue')[1].text
    num_acc_followers = driver.find_elements_by_css_selector('.ProfileCardStats-statValue')[2].text
    update = '#Tweets=' + str(num_tweets_acc) + ', #Following=' + str(num_acc_following) + ', #Followers=' + str(num_acc_followers)
    sendMail(update)
    #trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item')
    num_trends = 0

    time.sleep(random.randint(2,5))
    num_trends = 0
    while True:
        num_trends +=1
        if num_trends>NUM_TRENDS:
            break
        time.sleep(random.randint(4,8))
        try:
            while True:
                trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item.context-trend-item')
                if len(trend_elem)>0:
                    break
                
        except:
            try:
                trend_elem = driver.find_elements_by_css_selector('.js-nav.trend-name')
            except:
                pass
        time.sleep(random.randint(5,8))
        #choice(trend_elem).find_element_by_tag_name('a').click()
        link= choice(trend_elem).find_element_by_tag_name('a').get_attribute('href')
        driver.get(link)
        time.sleep(random.randint(5,8))
        numTweets = 0
        while True:
            g = driver.find_elements_by_css_selector('.js-tweet-text-container')
            if len(g)>0:
                break
        for i in g:
            
            try:
                i.click()
                time.sleep(1)
                a = driver.find_element_by_css_selector('.permalink-inner.permalink-tweet-container')
                b = a.find_element_by_css_selector('.ProfileTweet-actionButton.js-actionButton.js-actionRetweet')
                b.click()
                time.sleep(2)
                driver.find_element_by_css_selector('.btn.primary-btn.retweet-action').click()
                time.sleep(2)
                a.find_element_by_css_selector('.button-text.follow-text').click()
                numTweets +=1
                try:
                    f = driver.find_element_by_css_selector('#permalink-overlay')
                    f.click()
                except:
                    pass
                try:
                    driver.find_element_by_css_selector('.PermalinkProfile-dismiss').click()
                except:
                    pass
                time.sleep(random.randint(2,5))
            except:
                pass
            
            time.sleep(random.randint(2,5))
            if numTweets>NumTweets:
                break
        
    ## go to homepage
    try:
        driver.find_element_by_css_selector('#global-nav-home').find_element_by_tag_name('a').click()
        logging.info("Moving to homepage to do the next action")
    except:
        driver.get('https://twitter.com/')

    time.sleep(random.randint(2,5))

    ## tweet some stuff
    tweets = getTweets(c_tweets)
    
    try:
        for tweet in tweets:
            time.sleep(random.randint(2,5))
            elem_tweet_box = driver.find_element_by_xpath('//*[@id="tweet-box-home-timeline"]')
            elem_tweet_box.clear()
            time.sleep(random.randint(2,5))
            elem_tweet_box.send_keys(tweet)
            tweet_click_box = driver.find_element_by_xpath("//*[@id=\"timeline\"]/div[2]/div/form/div[2]/div[2]/button/span[1]/span")
            tweet_click_box.click()
            time.sleep(random.randint(2,5))
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
    time.sleep(random.randint(2,5))
    try:
        driver.find_element_by_id('user-dropdown-toggle').click()
        driver.find_element_by_id('signout-button').click()
        driver.close()
    except:
        pass
    time.sleep(random.randint(2,5))
    try:
        driver.close()
    except:
        pass
    time.sleep(random.randint(2,5))
  
if __name__ == "__main__":
    while True:
        #for i in range(1, NUM_BOT_USE+1):
        for i in range(NUM_BOT_USE, 0, -1):            
            username, password, bio, location, email, phone = getTwitterCredetials(i)
            print username, password, bio, location, email , phone
            sendMail('working')
            ## change ip to the local
            aa = "sudo ./hma-vpn-mod_2.sh " + location
            f = open('location.txt', 'wb')
            f.write(location)
            f.close()
            
##            # send the new ip to email
##            cur_ip = requests.get('https://api.ipify.org').content.strip()
##            msg = 'Current IP is ' + cur_ip
##            try:
##                sendMail(msg)
##            except:
##                pass
            try:
                TwitterAction(username, password, c_tweets, NUM_TRENDS, NumTweets, twitter_login_url, email, phone)
            except Exception,e:
                print str(e)
                msg_twitter = 'Error performing twitter action for account ' + username
                sendMail(msg_twitter)
            time.sleep(200)

            bb = "sudo killall openvpn"
            f = open('closeVPN.txt', 'wb')
            f.write('True')
            f.close()

            time.sleep(10)
            bb = "sudo killall openvpn"
            f = open('closeVPN.txt', 'wb')
            f.write('False')
            f.close()
            print 'done'
        time.sleep(3600*23)




















