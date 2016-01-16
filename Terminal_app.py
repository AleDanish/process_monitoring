#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import data
from subprocess import *
import sys

def main():
    if len(sys.argv) <= 1:
	print "Specify a process to monitor"
	sys.exit(1)
    process=sys.argv[1]
    pid=get_pid(process)
    if pid == "":
	print "No PID found"
	sys.exit(1)
    print "Process: %s"%process
    print "Pid: %s"%pid
    while True:
        _cpu=data.cpu(pid,process)
        _mem=data.mem(pid, process)
        _disk=data.disk()
	_io=data.io()
        print 'CPU (',_cpu,'%) - MEM (',_mem,'%) - DISK (',_disk,'KB/S) - IO (',_io,'KB/S)'

def get_pid(name):
        pipe=Popen("pgrep -u %s"%name, shell=True, stdout=PIPE).stdout
	pid=pipe.read()
	try:
	   int(pid)
	except ValueError:
	   pipe = Popen("pgrep %s"%name, shell=True, stdout=PIPE).stdout
	   pid=pipe.read()
        return pid
 
main()
