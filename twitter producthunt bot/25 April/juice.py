from selenium import webdriver
import sqlite3, smtplib, time

NUM_BOT_USE = 49
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

## function to get the twitter credentials
def getTwitterCredetials(id):
    c_account.execute('SELECT Username from accounts where id = ' + str(id))
    rows = c_account.fetchone()
    return rows[0]

def getJuice(username):
    driver = webdriver.Firefox()
    url = 'http://hunterlist.co/profile/'+username
    try:
        driver.get(url)
        g = driver.find_elements_by_css_selector('.col-sm-6.col-md-2')
        for i in g:
            if 'Votes' in i.text:
                votes = i.find_element_by_css_selector('.metric_value').text
            elif 'Posts' in i.text:
                posts = i.find_element_by_css_selector('.metric_value').text
            elif 'Maker' in i.text:
                maker = i.find_element_by_css_selector('.metric_value').text
            elif 'Juice' in i.text:
                juice = i.find_element_by_css_selector('.metric_value').text

        #print votes, posts, maker, juice
        msg = 'Username = ' + username + '; votes = ' + votes +\
              '; posts = ' + posts + '; maker = ' + maker + \
              '; juice = ' + juice
        sendMail(msg)
        print msg
    except:
        pass
    driver.close()


for i in range(1, NUM_BOT_USE+1):
    username = getTwitterCredetials(i)
    getJuice(username)
    time.sleep(20)

    
