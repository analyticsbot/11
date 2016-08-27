import smtplib, requests, os, time, random
from threading import Thread
import subprocess
## send an email with updated ip address or errors
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'product.hunt.bot12@gmail.com'
MAIL_PASSWORD = 'producthunt1234'
TO_EMAIL = 'product.hunt.bot12@gmail.com'


def changeIP(aa):
    os.system(aa)
    
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

options = ['London', 'New York', 'Boston', 'Montana', 'Quebec', 'Ontario']
while True:    
    ## change ip to the local
    aa = "sudo ./hma-vpn-mod_2.sh " + random.choice(options)
    print aa
    t = Thread(target = changeIP, args=(aa,))
    t.start()

    time.sleep(20)

    cur_ip = requests.get('https://api.ipify.org').content.strip()
    msg = 'Current IP is ' + cur_ip
    sendMail(msg)
    time.sleep(10)
