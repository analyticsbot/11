from selenium import webdriver
from random import choice
import sqlite3, logging
from time import localtime, strftime
import smtplib, random, time
 
LOG_LEVEL = 'INFO' # possible options = INFO, DEBUG, ERROR
driver = webdriver.Firefox()
twitter_login_url = 'https://twitter.com/login/'
product_hunt_tech = 'https://www.producthunt.com/tech'
product_hunt_games = 'https://www.producthunt.com/games'
product_hunt_books = 'https://www.producthunt.com/books'
product_hunt_home = 'https://www.producthunt.com/'
NUM_BOT_USE = 2
NUM_UPVOTES_PRODUCT_HUNT = 3
HANDLE = 'Codeology'
NUM_TRENDS = 2

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'product.hunt.bot12@gmail.com'
MAIL_PASSWORD = 'producthunt1234'
TO_EMAIL = 'product.hunt.bot12@gmail.com'

# add filemode="w" to overwrite
if LOG_LEVEL == 'INFO':
    logging.basicConfig(filename='twitter.log',level=logging.INFO, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
elif LOG_LEVEL == 'ERROR':
    logging.basicConfig(filename='twitter.log',level=logging.ERROR, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
elif LOG_LEVEL == 'DEBUG':
    logging.basicConfig(filename='twitter.log',level=logging.DEBUG, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def sendMail(msg):
    try:
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)     
        server.sendmail(MAIL_USERNAME, TO_EMAIL, msg)
        server.quit()
        logging.info("Email sent :: " +  msg)
        return True
    except Exception,e:
        logging.debug("Error in sending email  :: " +  str(e))
        return False
    
""" CONNECT TO ALL THE REQUIRED DBS"""
## connect to account db
try:
    conn_account = sqlite3.connect('accounts.db', check_same_thread = False)
    c_account = conn_account.cursor()
    print "[+] Opened accounts database connection successfully"
    logging.debug("Opened accounts database connection successfully")
except:
    print "[+] Error in opening accounts database connection"
    logging.debug("Error in opening accounts database connection")
#id, Gender, Name, Username, Password, Location ,Email, Recovery_Mail, Bio

## connect to product hunt links
try:
    conn_producthunt = sqlite3.connect('producthunt_links.db', check_same_thread = False)
    c_producthunt = conn_producthunt.cursor()
    print "[+] Opened product hunt database connection successfully"
    logging.debug("Opened product hunt database connection successfully")
except:
    print "[+] Error in opening product hunt database connection"
    logging.debug("Error in opening product hunt database connection")

## connect to tweets db
try:
    conn_tweets = sqlite3.connect('tweets.db', check_same_thread = False)
    c_tweets = conn_tweets.cursor()
    print "[+] Opened tweets database connection successfully"
    logging.debug("Opened tweets database connection successfully")
except:
    print "[+] Error in opening tweets database connection"
    logging.debug("Error in opening tweets database connection")

""" CONNECTED TO ALL THE REQUIRED DBS"""

def getTwitterCredetials(id):
    c_account.execute('SELECT Username, Password, Bio, Location from accounts where id = ' + str(id))
    rows = c_account.fetchone()
    return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"','')

username = 'SamathaLennertz'
password = 'iOP1839ylee'

def getTweets(c_tweets):
    c_tweets.execute("SELECT * FROM tweets ORDER BY RANDOM() LIMIT 5")
    rows = c_tweets.fetchall()
    return rows

def TwitterAction(driver, username, password, c_tweets):
    driver.get(twitter_login_url)

    email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
    email_elem.send_keys(username)
    pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
    pwd_elem.send_keys(password)

    pwd_elem.submit()
    time.sleep(2)
    trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item')
    
    num_trends = 0
    while True:
        num_trends +=1
        if num_trends>NUM_TRENDS:
            break
        time.sleep(5)
        trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item')
        choice(trend_elem).find_element_by_tag_name('a').click()
        time.sleep(10)

        ## follow some handles
        try:
            accounts = driver.find_elements_by_css_selector('.button-text.follow-text')
            for account in accounts:
                try:
                    account.click()
                except Exception,e:
                    print str(e)
        except Exception,e:
            print str(e)

        tweets = driver.find_elements_by_css_selector('.js-stream-item.stream-item.stream-item.expanding-stream-item')
        numTweets = 1
        while True:    
            tweet = choice(tweets)
            try:
                footer = tweet.find_element_by_css_selector('.stream-item-footer')
                rt = footer.find_element_by_css_selector('.ProfileTweet-actionButton.js-actionButton.js-actionRetweet')
                time.sleep(5)
                rt.click()
                time.sleep(5)
                driver.find_element_by_css_selector('.btn.primary-btn.retweet-action').click()
                time.sleep(2)
                numTweets +=1
            except Exception,e:
                print str(e)
                try:
                    driver.find_element_by_css_selector('.Icon.Icon--close.Icon--medium.dismiss').click()
                except Exception,e:
                    print str(e)
            if numTweets>5:
                break

    ## go to homepage
    try:
        driver.find_element_by_css_selector('#global-nav-home').find_element_by_tag_name('a').click()
    except:
        driver.get('https://twitter.com/')

    ## tweet some stuff
    tweets = getTweets(c_tweets)
    try:
        for tweet in tweets:
            print tweet
            elem_tweet_box = driver.find_element_by_xpath('//*[@id="tweet-box-home-timeline"]')
            elem_tweet_box.clear()
            elem_tweet_box.send_keys(tweet)
            tweet_click_box = driver.find_element_by_xpath("//*[@id=\"timeline\"]/div[2]/div/form/div[2]/div[2]/button/span[1]/span")
            tweet_click_box.click()
    except Exception,e:
        print str(e)  

    ## follow some random people
    try:
        account_elem = driver.find_element_by_css_selector('.flex-module')
        accounts_to_follow = account_elem.find_elements_by_css_selector('.js-account-summary.account-summary.js-actionable-user')
        for account in accounts_to_follow:
            follow_btn = account.find_element_by_css_selector('.small-follow-btn.follow-btn.btn.small.follow-button.js-recommended-item')
            follow_btn.click()
    except Exception,e:
        print str(e)

def getProductHuntUrl(c_producthunt):
    c_producthunt.execute("SELECT * FROM links ORDER BY RANDOM() LIMIT 1")
    rows = c_producthunt.fetchone()
    return rows[0]

def productHuntAction(driver, username, password, bio, product_hunt_tech, c_producthunt):    
    product_hunt_url = getProductHuntUrl(c_producthunt)
    driver.get(product_hunt_url)
    time.sleep(20)
    driver.get(product_hunt_tech)
    time.sleep(20)
    ## click on the upvote button
    voted =[]
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    options = [i for i in range(0, len(upvotes)/4)]
    try:
        while True:
            toVote = random.choice(options)
            if titles[toVote/4].text != HANDLE:
                upvotes[toVote].click()
                time.sleep(4)
                voted.append(toVote)
                break
    except:
        pass
    time.sleep(10)
    ## click on the twitter login button
    try:
        driver.find_element_by_css_selector('.secondaryText_PM80d.inverse_1CN6F.base_3CbW2').click()
    except:
        pass
    time.sleep(3)
    ## authorize the twitter application
    try:
        driver.find_element_by_css_selector('.submit.button.selected').click()
        time.sleep(10)
    except:
        pass

    # check if asks for bio. usually the first time
    try:
        time.sleep(10)
        headline= driver.find_element_by_id('headline')
        headline.send_keys(bio)
        driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.techSolidColor_3JJ0o.solidVariant_2wWrf').click()
    except:
        pass
    time.sleep(10)
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    for title in titles:
        if title.text.strip() == HANDLE:
            upvotes[titles.index(title)*4].click()
            voted.append(titles.index(title)*4)
            title.click()
            time.sleep(2)
            try:
                tw = driver.find_element_by_id('twitter')
                tw.click()

                p=driver.current_window_handle
                h=driver.window_handles
                h.remove(p)
                driver.switch_to_window(h.pop())
                driver.find_element_by_css_selector('.button.selected.submit').click()
                driver.close()
                driver.switch_to_window(p)
                time.sleep(2)
            except:
                pass
    time.sleep(10)
    driver.execute_script("window.history.go(-1)")
            
    time.sleep(10)
    count = 0
    for vote in upvotes:
        titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
        to_vote = random.choice(options)
        if to_vote not in voted:
            upvotes[to_vote].click()
            count +=1
            time.sleep(5)
            titles[to_vote/4].click()
            try:
                tw = driver.find_element_by_id('twitter')
                time.sleep(5)
                tw.click()
                time.sleep(2)
                p=driver.current_window_handle
                h=driver.window_handles
                h.remove(p)
                driver.switch_to_window(h.pop())
                driver.find_element_by_css_selector('.button.selected.submit').click()
                driver.close()
                driver.switch_to_window(p)
            except:
                pass
            driver.execute_script("window.history.go(-1)")
            time.sleep(2)
        if count == NUM_UPVOTES_PRODUCT_HUNT:
            break

    
if __name__ == "__main__":
    for i in range(1, NUM_BOT_USE+1):
        username, password, bio, location = getTwitterCredetials(i)
        ## change ip to the local
        # os.system("""start cmd /c scrapy crawl EarthPorn""")
        TwitterAction(driver, username, password, c_tweets)
        time.sleep(5)
        productHuntAction(driver, username, password, bio, product_hunt_tech, c_producthunt)
    

