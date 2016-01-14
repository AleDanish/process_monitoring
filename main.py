#     Author: Alessandro Zanni,
#     URL: https://github.com/AleDanish

import matplotlib.pyplot as plt
import matplotlib
import data
from subprocess import *
import sys

cpu=[]
mem=[]
disk=[]
io=[]

N=60 # number of samples
 
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
    print 'NO.    CPU    MEMORY    DISK    I/O'
    matplotlib.rcParams['toolbar'] = 'None'
    plt.figure(figsize=(20,10))
    i=0
    while True:
        i+=1
        plt.ylim(0,100)
        plt.xlim(0,N)
        _cpu=data.cpu(pid,process)
        _mem=data.mem(pid, process)
        _disk=data.disk()
	_io=data.io()
        print i,'\t',_cpu,'\t',_mem,'\t',_disk,'\t',_io
        cpu.append(_cpu)
        mem.append(_mem)
        #disk.append(_disk)
	#io.append(_io)
        plt.grid(True)
        plt.xlabel('TIME IN S')
        plt.ylabel('USAGE IN %')
        plt.title(' - - SYSTEM MONITOR - - ')
        cpu_label='CPU ('+_cpu+'%)'
	mem_label='MEM ('+_mem+'%)'
	disk_label='DISK ('+_disk+'KB/S)'
	io_label='IO ('+_io+'KB/S)'
        plt.plot(cpu[-60:-1],'g', label=cpu_label)
        plt.plot(mem[-60:-1],'r', label=mem_label)
	plt.plot(disk[-60:-1],'k', label=disk_label)
	plt.plot(io[-60:-1],'b', label=io_label)
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06,0,0.04), ncol=5)
	if len(cpu)>N:
            del cpu[0]
	    del mem[0]
	    #del disk[0]
	    #del io[0]
        plt.draw()
        matplotlib.interactive(True)
	plt.show()
        plt.clf()

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
