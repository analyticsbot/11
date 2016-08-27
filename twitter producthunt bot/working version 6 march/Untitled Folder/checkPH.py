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
driver.get(twitter_login_url)

username, password, email = 'meSamspro', 'iexahgh5Yo', 'ThomeCaroliexah@outlook.com'
username, password, email = 'MeEarnest88', 'Oojoh3cahru', 'WhitehCynthiOojoh@outlook.com'
logging.info("Logging into the twitter account ")
email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
email_elem.send_keys(username)
pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
pwd_elem.send_keys(password)
pwd_elem.submit()

time.sleep(2)
# static variables
LOG_LEVEL = 'INFO' # possible options = INFO, DEBUG, ERROR
twitter_login_url = 'https://twitter.com/login/'
product_hunt_tech = 'https://www.producthunt.com/tech'
product_hunt_games = 'https://www.producthunt.com/games'
product_hunt_books = 'https://www.producthunt.com/books'
product_hunt_home = 'https://www.producthunt.com/'
HANDLE = 'Google Doc Publisher'
product_hunt_url = 'https://t.co/LZWtRWJpxX'
driver.get(product_hunt_url)
driver.get(product_hunt_tech)
## click on the upvote button
voted =[]
upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
options = [i*4 for i in range(0, (len(upvotes)/4)+1)]
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
    time.sleep(5)
except:
    pass

# check if asks for bio. usually the first time
try:
    time.sleep(2)
    headline= driver.find_element_by_id('headline')
    headline.send_keys(bio)
    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.techSolidColor_3JJ0o.solidVariant_2wWrf').click()
except:
    pass
time.sleep(2)
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
                time.sleep(2)
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
    pass
driver.get(product_hunt_tech)
logging.info("Going to url "+ product_hunt_tech)        
count = 0
upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
try:
    for vote in upvotes:
        driver.get(product_hunt_tech)
        time.sleep(2)
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

##driver.get(product_hunt_games)
##time.sleep(15)
##driver.get(product_hunt_books)
##time.sleep(15)
##driver.get(product_hunt_home)
##time.sleep(15)

## logout from producthunt
try:
    driver.find_element_by_css_selector('.placeholderHidden_pb7Bz').click()
    driver.find_element_by_css_selector('li.option_2XMGo:nth-child(6) > a:nth-child(1)').click()
    time.sleep(5)
except:
    pass

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
