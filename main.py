#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib
import data
from subprocess import *
import sys

cpu=[]
mem=[]
disk_read=[]
disk_write=[]
io=[]

N=100 # number of samples
 
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
    print 'NO.   CPU   MEMORY   DISK_RD   DISK_WR   I/O'
    matplotlib.rcParams['toolbar'] = 'None'
    #plt.subplot(211)
    plt.figure(figsize=(20,10))
    i=0
    while True:
        i+=1
        plt.ylim(0,100)
        plt.xlim(0,N)
        _cpu=data.cpu(pid,process)
        _mem=data.mem(pid, process)
        _dd_r=data.disk_read(pid)
	_dd_w=data.disk_write(pid)
	_io=data.io(pid)
        print i,'\t',_cpu,'\t',_mem,'\t',_dd_r,'\t',_dd_w,'\t',_io
        cpu.append(_cpu)
        mem.append(_mem)
        disk_read.append(_dd_r)
	disk_write.append(_dd_w)
	io.append(_io)
        plt.grid(True)
        plt.xlabel('TIME IN S')
        plt.ylabel('USAGE IN %')
        plt.title(' - - SYSTEM MONITOR - - ')
        cpu_label='CPU ('+_cpu+'%)'
	mem_label='MEM ('+_mem+'%)'
	disk_read_label='DISK-RD ('+_dd_r+'KB/S)'
	disk_write_label='DISK-WR ('+_dd_w+'KB/S)'
	io_label='IO ('+_io+'%)'
        plt.plot(cpu[-60:-1],'g', label=cpu_label)
        plt.plot(mem[-60:-1],'r', label=mem_label)
        plt.plot(disk_read[-60:-1],'k', label=disk_read_label)
	plt.plot(disk_write[-60:-1],'k', label=disk_write_label)
	plt.plot(io[-60:-1],'b', label=io_label)
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06,0,0.04), ncol=5)
	if len(cpu)>N:
            del cpu[0]
	    del mem[0]
            del disk_read[0]
	    del disk_write[0]
	    del io[0]
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
