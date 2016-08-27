from selenium import webdriver
import sqlite3, smtplib, time

twitter_login_url = 'https://twitter.com/login/'
NUM_BOT_USE = 49 ## number of twitter ids to use for upvoting content

## connect to account db
try:
    conn_account = sqlite3.connect('accounts.db', check_same_thread = False)
    c_account = conn_account.cursor()
    print "[+] Opened accounts database connection successfully"
except:
    print "[+] Error in opening accounts database connection"
#id, Gender, Name, Username, Password, Location ,Email, Recovery_Mail, Bio

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

## function to get the twitter credentials
def getTwitterCredetials(id):
    c_account.execute('SELECT Username, Password, Bio, Location, Email, Phone from accounts where id = ' + str(id))
    rows = c_account.fetchone()
    try:
        return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"',''), rows[4].replace('"',''), rows[5].replace('"','')
    except:
        return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"',''), rows[4].replace('"',''), rows[5]

##global driver
##driver = webdriver.Firefox()
## function to interact with twitter. like, RT, follow, trends
def KloutAction(username, password, twitter_login_url, email, phone):
    driver = webdriver.Firefox()
    driver.get(twitter_login_url)
    email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
    email_elem.send_keys(username)
    pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
    pwd_elem.send_keys(password)

    pwd_elem.submit()
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


    driver.get('https://klout.com/home')
    driver.find_element_by_css_selector('.tw-connect.button').click()
    try:
        driver.find_element_by_css_selector('#allow').click()
    except:
        pass
    try:
        driver.find_element_by_css_selector('#last-name').send_keys('Roger')
    except:
        pass
    try:
        driver.find_element_by_css_selector('#email').send_keys(email)
    except:
        pass
    try:
        driver.find_element_by_css_selector('#register-klout').click()
    except:
        pass
    
    try:
        driver.find_element_by_css_selector('#main').click()
        driver.find_element_by_css_selector('#main').click()
    except:
        pass
    try:
        driver.find_element_by_css_selector('.close.close-modal').click()
    except:
        pass
    try:
        driver.find_element_by_css_selector('.close.close-modal').click()
    except:
        pass
    score = driver.find_element_by_css_selector('.score').text
    driver.close()
    return score
    

if __name__ == "__main__":
    while True:
        for i in range(1, NUM_BOT_USE+1):
            username, password, bio, location, email, phone = getTwitterCredetials(i)
            print username, password, bio, location, email , phone
            try:
                score = KloutAction(username, password, twitter_login_url, email, phone)
                msg = 'Klout Score::' + username+'='+str(score)
                print msg
                sendMail(msg)
            except Exception,e:
                print str(e)
                msg_twitter = 'Error performing klout action for account ' + username
                sendMail(msg_twitter)
