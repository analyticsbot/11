import socket
import socks
import httplib
import requests

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket

def newIdentity():
    socks.setdefaultproxy()
    print requests.get('http://my-ip.heroku.com').content
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9051))
    s.send("AUTHENTICATE\r\n")
    response = s.recv(128)
    if response.startswith("250"):
        s.send("SIGNAL NEWNYM\r\n")
    s.close()
    connectTor()
    
def main():
##    print 'connected'
##
##    conn = httplib.HTTPConnection("my-ip.heroku.com")
##    conn.request('GET', '/')
##    response = conn.getresponse()
##    print (response.read())
##    print requests.get('http://my-ip.heroku.com').content
##    
##    connectTor()
##    print 'connected'
##
##    conn = httplib.HTTPConnection("my-ip.heroku.com")
##    conn.request('GET', '/')
##    response = conn.getresponse()
##    print (response.read())
##    print requests.get('http://my-ip.heroku.com').content

    newIdentity()
    print requests.get('http://my-ip.heroku.com').content

main()
