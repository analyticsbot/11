import smtplib
import subprocess, random
from pyvirtualdisplay import Display
import sqlite3
from random import choice

# static variables
LOG_LEVEL = 'INFO' # possible options = INFO, DEBUG, ERROR
twitter_login_url = 'https://twitter.com/login/'
product_hunt_tech = 'https://www.producthunt.com/tech'
product_hunt_games = 'https://www.producthunt.com/games'
product_hunt_books = 'https://www.producthunt.com/books'
product_hunt_home = 'https://www.producthunt.com/'
NUM_BOT_USE = 2 ## number of twitter ids to use for upvoting content
NUM_UPVOTES_PRODUCT_HUNT = random.randint(2,3) ## number of upvotes on product hunt
HANDLE = 'Codeology' ## handle or product that has to be always upvoted 
NUM_TRENDS = 2 ## number of trends on twitter the bot should interact

## send an email with updated ip address or errors
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'product.hunt.bot12@gmail.com'
MAIL_PASSWORD = 'producthunt1234'
TO_EMAIL = 'product.hunt.bot12@gmail.com'

def connect():
    conn = sqlite3.connect('botdb.db', check_same_thread = False)
    c = conn.cursor()
    print "[+] Opened database successfully"

    return conn, c


## check if the script running on ubuntu
def startDisplay():
    try:
        if os.environ.get('USER') == 'ravi':
            display = Display(visible=0, size=(800, 600))
            display.start()
    except:
        pass

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

def getTwitterCredetials(id, c_account):
    c_account.execute('SELECT Username, Password, Bio, Location from accounts where id = ' + str(id))
    rows = c_account.fetchone()
    return rows[0], rows[1], rows[2].strip().replace('"',''), rows[3].replace('"','')

## function to get tweets
def getTweets(c_tweets):
    c_tweets.execute("SELECT * FROM tweets ORDER BY RANDOM() LIMIT 5")
    rows = c_tweets.fetchall()
    return rows

## get a random product hunt url to visit the website
def getProductHuntUrl(c_producthunt):
    c_producthunt.execute("SELECT * FROM links ORDER BY RANDOM() LIMIT 1")
    rows = c_producthunt.fetchone()
    return rows[0]

def changeIPLocation(location):
    command = "sudo ./hma-vpn-mod_2.sh " + location
    command = command.split()
    output = subprocess.call(command)
    return output

def closeVPN():
    command = "sudo killall openvpn".split()
    output = subprocess.call(command)
    return output

def disconnect():
    c.close()
    conn.close()
