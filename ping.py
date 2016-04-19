import subprocess
import shlex

cmd1 = "ping -n 1 -w 1 192.168.1."



for i in range(1,100):
    cmd = cmd1 + str(i)
    args = shlex.split(cmd)
    print args
    try:
        subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print cmd + " server is up!"
    except subprocess.CalledProcessError:
        print "Failed to get ping."