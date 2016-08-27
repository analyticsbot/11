import socket
import socks
import httplib
import requests

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket

def main():
    print 'connected'

    conn = httplib.HTTPConnection("my-ip.heroku.com")
    conn.request('GET', '/')
    response = conn.getresponse()
    print (response.read())
    print requests.get('http://my-ip.heroku.com').content
    
    connectTor()
    print 'connected'

    conn = httplib.HTTPConnection("my-ip.heroku.com")
    conn.request('GET', '/')
    response = conn.getresponse()
    print (response.read())
    print requests.get('http://my-ip.heroku.com').content

main()
