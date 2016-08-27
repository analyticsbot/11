import subprocess
import time
argument = '...'
proc = subprocess.Popen(['ls -l'], shell=True)
time.sleep(3) # <-- There's no time.wait, but time.sleep.
pid = proc.pid # <--- access `pid` attribute to get the pid of the child process.
print pid

print proc.terminate()
