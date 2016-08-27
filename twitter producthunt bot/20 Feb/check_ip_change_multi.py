import smtplib, requests, os, time, random
from threading import Thread
import subprocess
import multiprocessing

## send an email with updated ip address or errors
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'product.hunt.bot12@gmail.com'
MAIL_PASSWORD = 'producthunt1234'
TO_EMAIL = 'product.hunt.bot12@gmail.com'


dd = {}
def changeIP(aa):
    proc = subprocess.Popen([aa], shell=True)
    dd['proc'] = proc
    time.sleep(4)
    pid = proc.pid
    
    return proc
    
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
        print str(e)
        return False

options = ['London', 'New York', 'Boston', 'Montana', 'Quebec', 'Ontario']
while True:    
    ## change ip to the local
##    aa = "sudo ./hma-vpn-mod_2.sh " + random.choice(options)
##    print aa
##    p = multiprocessing.Process(target=changeIP, name="changeIP", args=(aa,))
##    p.start()
##
##    time.sleep(100)
##    
##
##    cur_ip = requests.get('http://api.ipify.org').content
##     
##    msg = 'Current IP is ' + cur_ip
##    print msg
    sendMail('msg')
    print 'msg'
##    time.sleep(3)
##    print dd['proc'].terminate()
##
##    time.sleep(100)
##    bb = "sudo killall openvpn"
##    p2 = multiprocessing.Process(target=changeIP, name="killvpn", args=(bb,))
##    p2.start()
##
##    time.sleep(20)
##    p.terminate()
##    time.sleep(10)
    
