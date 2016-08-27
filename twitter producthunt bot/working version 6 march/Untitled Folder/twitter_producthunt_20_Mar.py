from selenium import webdriver
from random import choice
import sqlite3, logging, requests, os,multiprocessing, subprocess
from time import localtime, strftime
import smtplib, random, time
from threading import Thread
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)

## check if the script running on ubuntu
try:
    if os.environ.get('USER') == 'ubuntu':        
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 600))
        display.start()
except:
    pass    

# static variables
LOG_LEVEL = 'INFO' # possible options = INFO, DEBUG, ERROR
driver = webdriver.Firefox()
twitter_login_url = 'https://twitter.com/login/'
product_hunt_tech = 'https://www.producthunt.com/tech'
product_hunt_games = 'https://www.producthunt.com/games'
product_hunt_books = 'https://www.producthunt.com/books'
product_hunt_home = 'https://www.producthunt.com/'
NUM_BOT_USE = 49  ## number of twitter ids to use for upvoting content
NUM_UPVOTES_PRODUCT_HUNT = random.randint(2,3) ## number of upvotes on product hunt
HANDLE = 'Codeology' ## handle or product that has to be always upvoted 
NUM_TRENDS = 6 ## number of trends on twitter the bot should interact
NumTweets = 5
## send an email with updated ip address or errors
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'product.hunt.bot12@gmail.com'
MAIL_PASSWORD = 'producthunt1234'
TO_EMAIL = 'product.hunt.bot12@gmail.com'

# add filemode="w" to overwrite
logging.basicConfig(filename='twitter.log',level=logging.INFO, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

## function to send an email
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

## function to get the twitter credentials
def getTwitterCredetials(id):
    c_account.execute('SELECT Username, Password, Bio, Location, Email from accounts where id = ' + str(id))
    rows = c_account.fetchone()
    return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"',''), rows[4].replace('"','')

## function to get tweets
def getTweets(c_tweets):
    c_tweets.execute("SELECT * FROM tweets ORDER BY RANDOM() LIMIT 5")
    rows = c_tweets.fetchall()
    return rows

## function to interact with twitter. like, RT, follow, trends
def TwitterAction(driver, username, password, c_tweets, email):
    driver.get(twitter_login_url)
    logging.info("Logging into the twitter account ")
    email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
    email_elem.send_keys(username)
    pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
    pwd_elem.send_keys(password)

    pwd_elem.submit()
    time.sleep(1)
    try:
        if 'Help us keep your account safe' in driver.page_source:
            email_elem = driver.find_element_by_id('challenge_response')
            email_elem.send_keys(email)
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
        trend_elem = driver.find_elements_by_css_selector('.js-nav.trend-name')
        choice(trend_elem).click()
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

    ## tweet some stuff
    tweets = getTweets(c_tweets)
    try:
        for tweet in tweets:
            logging.info("Tweeting  -- " + tweet)
            elem_tweet_box = driver.find_element_by_xpath('//*[@id="tweet-box-home-timeline"]')
            elem_tweet_box.clear()
            elem_tweet_box.send_keys(tweet)
            tweet_click_box = driver.find_element_by_xpath("//*[@id=\"timeline\"]/div[2]/div/form/div[2]/div[2]/button/span[1]/span")
            tweet_click_box.click()
    except Exception,e:
        logging.error("Error tweeting")

    ## follow some random people
    try:
        account_elem = driver.find_element_by_css_selector('.flex-module')
        accounts_to_follow = account_elem.find_elements_by_css_selector('.js-account-summary.account-summary.js-actionable-user')
        for account in accounts_to_follow:
            follow_btn = account.find_element_by_css_selector('.small-follow-btn.follow-btn.btn.small.follow-button.js-recommended-item')
            follow_btn.click()
        logging.info("Followed some random people")
    except Exception,e:
        logging.error("No one to follow")

    logging.info("Twitter Action done for account " +  username)    

## get a random product hunt url to visit the website
def getProductHuntUrl(c_producthunt):
    c_producthunt.execute("SELECT * FROM links ORDER BY RANDOM() LIMIT 1")
    rows = c_producthunt.fetchone()
    return rows[0]

## start product hunt action. Upvote product. Tweet product.
## visit product page
def productHuntAction(driver, username, password, bio, product_hunt_tech, c_producthunt):
    logging.info("Starting Product hunt action for " +  username)
    product_hunt_url = getProductHuntUrl(c_producthunt)
    logging.info("Going to the product hunt url == "+ product_hunt_url)
    driver.get(product_hunt_url)
    time.sleep(random.randint(10,20))
    driver.get(product_hunt_tech)
    logging.info("Going to the product hunt tech url == "+ product_hunt_tech)
    time.sleep(random.randint(15,20))
    ## click on the upvote button
    voted =[]
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    logging.info("Number of upvotes possible on this "+ len(upvotes) + ' titles total : ' +  len(titles))
    options = [i*4 for i in range(0, (len(upvotes)/4)+1)]
    try:
        while True:
            toVote = random.choice(options)
            if titles[toVote/4].text != HANDLE:
                upvotes[toVote].click()
                time.sleep(4)
                voted.append(toVote)
                logging.info("Upvoted the handle == "+ titles[toVote/4].text)
                break
    except:
        logging.info("Did not find handle == "+ HANDLE)
    time.sleep(10)
    ## click on the twitter login button
    try:
        driver.find_element_by_css_selector('.secondaryText_PM80d.inverse_1CN6F.base_3CbW2').click()
        logging.info("Logging in using twitter "+ username)
    except:
        pass
    time.sleep(3)
    ## authorize the twitter application
    try:
        driver.find_element_by_css_selector('.submit.button.selected').click()
        logging.info("Authotizing login using twitter "+ username)
        time.sleep(10)
    except:
        pass

    # check if asks for bio. usually the first time
    try:
        time.sleep(10)
        headline= driver.find_element_by_id('headline')
        headline.send_keys(bio)
        driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.techSolidColor_3JJ0o.solidVariant_2wWrf').click()
        logging.info("Adding a bio to the account "+ username)        
    except:
        pass
    time.sleep(10)
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    try:
        for title in titles:
            if title.text.strip() == HANDLE:
                logging.info("Upvoted the handle == "+ HANDLE)
                upvotes[titles.index(title)*4].click()
                voted.append(titles.index(title)*4)
                title.click()
                time.sleep(2)
                try:
                    tw = driver.find_element_by_id('twitter')
                    tw.click()
                    time.sleep(5)
                    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.twitterSolidColor_G22Bs.solidVariant_2wWrf').click()
                    time.sleep(2)
                    driver.find_element_by_css_selector('.modal--close.v-desktop')
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
    except:
        logging.error("Cant Upvoted the handle == "+ HANDLE)
    time.sleep(10)
    driver.get(product_hunt_tech)
    logging.info("Going to url "+ product_hunt_tech)        
    time.sleep(10)
    count = 0
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    try:
        for vote in upvotes:
            driver.get(product_hunt_tech)
            time.sleep(10)
            titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
            upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
            to_vote = random.choice(options)
            time.sleep(2)
            if to_vote not in voted:
                upvotes[to_vote].click()
                count +=1
                time.sleep(5)
                titles[to_vote/4].click()
                logging.info("upvoted "+ titles[to_vote/4].text) 
                try:
                    tw = driver.find_element_by_id('twitter')
                    time.sleep(5)
                    tw.click()
                    time.sleep(5)
                    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.twitterSolidColor_G22Bs.solidVariant_2wWrf').click()
                    time.sleep(2)
                    driver.find_element_by_css_selector('.modal--close.v-desktop')
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
                driver.get(product_hunt_tech)
                time.sleep(5)
            if count == NUM_UPVOTES_PRODUCT_HUNT:
                break
    except:
        pass

    driver.get(product_hunt_games)
    time.sleep(15)
    driver.get(product_hunt_books)
    time.sleep(15)
    driver.get(product_hunt_home)
    time.sleep(15)
    
    ## logout from producthunt
    driver.find_element_by_css_selector('.placeholderHidden_pb7Bz').click()
    driver.find_element_by_css_selector('li.option_2XMGo:nth-child(6) > a:nth-child(1)').click()
    time.sleep(5)

    logging.info("logged out from product hunt for user name "+ username) 
    

    ## logout from twitter
    try:
        driver.get('https://twitter.com/')
        time.sleep(5)
        driver.find_element_by_css_selector('.btn.js-tooltip.settings.dropdown-toggle.js-dropdown-toggle').click()
        driver.find_element_by_css_selector('#signout-button').click()
        time.sleep(2)
    except:
        pass

    logging.info("logged out from twitter for user name "+ username) 

def changeIP(aa):
    subprocess.call(aa.split())
    
if __name__ == "__main__":
    while True:
        for i in range(1, NUM_BOT_USE+1):
            username, password, bio, location, email = getTwitterCredetials(i)
            print username, password, bio, location, email
            sendMail('working')
            logging.info("Logging to twitter account  :: " +   username)
            logging.info("Changing ip according to location : " +  location)
            ## change ip to the local
            aa = "sudo ./hma-vpn-mod_2.sh " + location
            f = open('location.txt', 'wb')
            f.write(location)
            f.close()
            
            #time.sleep(100)
            logging.info("IP Change successful")
            # send the new ip to email
            cur_ip = requests.get('https://api.ipify.org').content.strip()
            msg = 'Current IP is ' + cur_ip
            logging.info("IP Change successful. New IP is  :: " +  cur_ip + ' for location ' +  location)
            try:
                sendMail(msg)
            except:
                logging.info("Error sending ip change email")
            logging.info("Starting twitter action")
            try:
                TwitterAction(driver, username, password, c_tweets, email)
            except Exception,e:
                msg_twitter = 'Error performing twitter action for account ' + username
                sendMail(msg_twitter)
            #time.sleep(20)
##            try:
##                productHuntAction(driver, username, password, bio, product_hunt_tech, c_producthunt)
##            except:
##                msg_ph = 'Error performing product hunt action for account ' + username
##                sendMail(msg_ph)
##            logging.info("Product hunt action done "+ username)
            time.sleep(20)

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
        #time.sleep(3600*23)


        
            

