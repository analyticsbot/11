from selenium import webdriver
import logging, os, multiprocessing, subprocess, random, time
from time import localtime, strftime
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)

from helper import *
from helper import *
from phbot import productHuntAction
from twitterbot import TwitterAction

startDisplay()
driver = webdriver.Firefox()
logging.basicConfig(filename='twitter.log',level=logging.INFO, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    for i in range(1, NUM_BOT_USE+1):
        conn, c = connect()
        username, password, bio, location = getTwitterCredetials(i, c)
        print username, password, bio, location
        aa = "sudo ./hma-vpn-mod_2.sh " + location
        p = multiprocessing.Process(target=changeIPLocation, name="changeIP", args=(aa,))
        p.start()
        
        time.sleep(10)
        logging.info("IP Change successful")
        # send the new ip to email
        cur_ip = requests.get('https://api.ipify.org').content.strip()
        msg = 'Current IP is ' + cur_ip
        logging.info("IP Change successful. New IP is  :: " +  cur_ip + ' for location ' +  location)
##        try:
##            sendMail(msg)
##        except:
##            logging.info("Error sending ip change email")
##        logging.info("Starting twitter action")
##        try:
##            TwitterAction(driver, username, password, c_tweets)
##        except Exception,e:
##            msg_twitter = 'Error performing twitter action for account ' + username
##            sendMail(msg_twitter)
##        time.sleep(20)
##        try:
##            productHuntAction(driver, username, password, bio, product_hunt_tech, c_producthunt)
##        except:
##            msg_ph = 'Error performing product hunt action for account ' + username
##            sendMail(msg_ph)
##        logging.info("Product hunt action done "+ username)
##        time.sleep(20)

        bb = "sudo killall openvpn"
        p2 = multiprocessing.Process(target=closeVPN, name="killvpn", args=(bb,))
        p2.start()
