import multiprocessing, subprocess, time


def changeIP(aa):
    subprocess.call(aa.split())

while True:
    f = open('location.txt', 'rb')
    location = f.read().strip()
    f.close()
    aa = "sudo ./hma-vpn-mod_2.sh " + location
    p = multiprocessing.Process(target=changeIP, name="changeIP", args=(aa,))
    p.start()
    time.sleep(900)
    p.terminate()
    
