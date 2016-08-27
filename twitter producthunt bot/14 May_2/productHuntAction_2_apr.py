from selenium import webdriver
from random import choice
import sqlite3, logging, requests, os,multiprocessing, subprocess
from time import localtime, strftime
import smtplib, random, time, random
from threading import Thread
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)

product_hunt_tech = 'https://www.producthunt.com/tech'
product_hunt_games = 'https://www.producthunt.com/games'
product_hunt_books = 'https://www.producthunt.com/books'
product_hunt_home = 'https://www.producthunt.com/'
twitter_login_url =  'https://twitter.com/login/'
NUM_BOT_USE = 49 ## number of twitter ids to use for upvoting content
NUM_UPVOTES_PRODUCT_HUNT = random.randint(2,3) ## number of upvotes on product hunt
HANDLE = 'Codeology' ## handle or product that has to be always upvoted 

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

## connect to product hunt links
try:
    conn_producthunt = sqlite3.connect('producthunt_links_2.db', check_same_thread = False)
    c_producthunt = conn_producthunt.cursor()
    print "[+] Opened product hunt database connection successfully"
except:
    print "[+] Error in opening product hunt database connection"

## function to get the twitter credentials
def getTwitterCredetials(id):
    c_account.execute('SELECT Username, Password, Bio, Location, Email, Phone from accounts where id = ' + str(id))
    rows = c_account.fetchone()
    try:
        return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"',''), rows[4].replace('"',''), rows[5].replace('"','')
    except:
        return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"',''), rows[4].replace('"',''), rows[5]

## get a random product hunt url to visit the website
def getProductHuntUrl(c_producthunt):
    c_producthunt.execute("SELECT * FROM links ORDER BY RANDOM() LIMIT 1")
    rows = c_producthunt.fetchone()
    return rows[0]

## start product hunt action. Upvote product. Tweet product.
## visit product page
def productHuntAction(username, password, bio, product_hunt_tech, c_producthunt,twitter_login_url, email, phone):
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
    time.sleep(2)
    product_hunt_url = getProductHuntUrl(c_producthunt)
    driver.get(product_hunt_url)
    #time.sleep(random.randint(10,20))
    driver.get(product_hunt_tech)
    #time.sleep(random.randint(15,20))
    ## click on the upvote button
    time.sleep(10)
    voted =[]
    time.sleep(10)
    while True:
        try:
            upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
        except:
            upvotes = []
        if len(upvotes)>0:
            break
    print 2
    while True:
        try:
            titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
        except:
            titles = []
        if len(titles)>0:
            break
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
    time.sleep(3)
    try:
        driver.find_element_by_css_selector('.secondaryText_PM80d.inverse_1CN6F.base_3CbW2').click()
    except Exception,e:
        #print str(e)
        pass

    try:
        while True:
            
            driver.find_element_by_css_selector('.twitterButton_2X0Lx.loginButton_1keGm').click()
            if 'product hunt' in driver.title().lower():
                break
    except:
        pass
    time.sleep(3)
    ## authorize the twitter application
    try:
        driver.find_element_by_css_selector('.submit.button.selected').click()
        #time.sleep(10)
    except Exception,e:
        pass
    time.sleep(3)
    # check if asks for bio. usually the first time
    try:
        #time.sleep(10)
        headline= driver.find_element_by_id('headline')
        headline.send_keys(bio)
        try:
            driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.techSolidColor_3JJ0o.solidVariant_2wWrf').click()
        except:
            try:
                driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.orangeSolidColor_B-2gO.solidVariant_2wWrf').click()
            except:
                pass
    except Exception,e:
        #print str(e)
        pass

    time.sleep(2)
    try:
        topics = driver.find_elements_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.simpleVariant_1Nl54')
        for topic in topics:
            topic.click()
        driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.orangeSolidColor_B-2gO.solidVariant_2wWrf').click()
    except:
        pass
            
    time.sleep(10)
    while True:
        try:
            upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
        except:
            upvotes = []
        if len(upvotes)>0:
            break
    while True:
        try:
            titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
        except:
            titles = []
        if len(titles)>0:
            break
    try:
        for title in titles:
            if title.text.strip() == HANDLE:
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
                    time.sleep(2)
                except Exception,e:
                    print str(e)
    except Exception,e:
        print str(e)
    time.sleep(10)
    driver.get(product_hunt_tech)
    time.sleep(10)
    count = 0
    while True:
        try:
            upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
        except:
            upvotes = []
        if len(upvotes)>0:
            break
    while True:
        try:
            titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
        except:
            titles = []
        if len(titles)>0:
            break
    try:
        for vote in upvotes:
            driver.get(product_hunt_tech)
            time.sleep(10)
            while True:
                try:
                    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
                except:
                    upvotes = []
                if len(upvotes)>0:
                    break
            while True:
                try:
                    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
                except:
                    titles = []
                if len(titles)>0:
                    break
            to_vote = random.choice(options)
            time.sleep(4)
            if to_vote not in voted:
                upvotes[to_vote].click()
                count +=1
                time.sleep(5)
                titles[to_vote/4].click()
                try:
                    time.sleep(5)
                    tw = driver.find_element_by_id('twitter')
                    time.sleep(5)
                    tw.click()
                    time.sleep(5)
                    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.twitterSolidColor_G22Bs.solidVariant_2wWrf').click()
                    time.sleep(2)
                    driver.find_element_by_css_selector('.modal--close.v-desktop')
                    time.sleep(2)
                except Exception,e:
                    print str(e)
                driver.get(product_hunt_tech)
                time.sleep(5)
            if count == NUM_UPVOTES_PRODUCT_HUNT:
                break
    except Exception,e:
        print str(e)

    driver.get(product_hunt_games)
    time.sleep(5)
    driver.get(product_hunt_books)
    time.sleep(5)
    driver.get(product_hunt_home)
    time.sleep(5)
    
    ## logout from producthunt
    try:
        driver.find_element_by_css_selector('.placeholderHidden_pb7Bz').click()
        driver.find_element_by_css_selector('li.option_2XMGo:nth-child(6) > a:nth-child(1)').click()
    except:
        pass
    time.sleep(5)    

    ## logout from twitter
    try:
        driver.get('https://twitter.com/')
        time.sleep(5)
        driver.find_element_by_css_selector('.btn.js-tooltip.settings.dropdown-toggle.js-dropdown-toggle').click()
        driver.find_element_by_css_selector('#signout-button').click()
        time.sleep(2)
    except:
        pass
    while True:
        try:
            driver.close()
            break
        except:
            pass


if __name__ == "__main__":
    while True:
        for i in range(1, NUM_BOT_USE+1):
            username, password, bio, location, email, phone = getTwitterCredetials(i)
            print username, password, bio, location, email , phone
            sendMail('working')
            ## change ip to the local
            aa = "sudo ./hma-vpn-mod_2.sh " + location
            f = open('location.txt', 'wb')
            f.write(location)
            f.close()
            
            try:
                productHuntAction(username, password, bio, product_hunt_tech, c_producthunt,twitter_login_url, email, phone)
            except Exception, e:
                print str(e)
                msg_ph = 'Error performing product hunt action for account ' + username
                sendMail(msg_ph)
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
