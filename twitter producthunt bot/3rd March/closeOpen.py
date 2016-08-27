import multiprocessing, subprocess, time

def changeIP(aa):
    subprocess.call(aa.split())

while True:
    f = open('closeVPN.txt', 'rb')
    stop = f.read().strip()
    if stop == 'True':
        bb = "sudo killall openvpn"
        print bb
        p2 = multiprocessing.Process(target=changeIP, name="killvpn", args=(bb,))
        p2.start()
        time.sleep(11)
