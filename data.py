#     Author: Alessandro Zanni,
#     URL: https://github.com/AleDanish

import psutil
import time
import subprocess
import re

folder="metrics/"
cpu_file="cpu_perc.csv"
memory_file="memory_perc.csv"
io_file="io_perc.csv"
disk_write_file="disk_write.csv"
disk_read_file="disk_read.csv"

def cpu(pid, ps_name):
    '''This method returns the current CPU usage in %'''
    cmd="top -p "+pid.strip()+" -b -n 1 | grep -w "+ps_name+" | awk '{print $9}'"
    output=subprocess.check_output(["sh", "-c", cmd])
    print repr( output)
    value = re.sub(',', '.', output.strip())
    print repr(value)
    writefile(cpu_file, value, "a")
    return "%4.2f" %float(value)

def cpu_sys(pid):
    '''This method returns the current CPU usage by the system'''
    a=psutil.Process(int(pid)).cpu_times().system
    return "%4.2f" %a

def cpu_user(pid):
    '''This method returns the current CPU usage by the user'''
    a=psutil.Process(int(pid)).cpu_times().user
    return "%4.2f" %a

def mem(pid, ps_name):
    '''This method returns the current RAM usage in %'''
    #a=psutil.virtual_memory().total
    cmd="top -p "+pid.strip()+" -b -n 1 | grep -w "+ps_name+" | awk '{print $10}'"
    output=subprocess.check_output(["sh", "-c", cmd])
    value = re.sub(',', '.', output.strip())
    writefile(memory_file, value, "a")
    return "%4.2f" %float(value)

def dsk():
    '''This method returns the current DISK usage'''
    a=psutil.disk_partitions()
    b=[]
    x=0
    y=0
    for i in range (0,len(a)):
        b.append(a[i][1])
        x+=psutil.disk_usage(b[i])[0]
        y+=psutil.disk_usage(b[i])[1]
        z=float(y)/float(x)*100
    return "%2.2f" %z

def disk_write(pid):
    '''This method returns the current DISK WRITE speed in KB'''
    cmd="iotop -p "+pid.strip()+" -n 1 -k | awk '{print $8}'"
    output=subprocess.check_output(["sudo", "sh", "-c", cmd])
    value=formatResult(output)
    writefile(disk_write_file, value, "a")
    return "%4.2f" %float(value)

def disk_read(pid):
    '''This method returns the current DISK READ speed in KB'''
    cmd="iotop -p "+pid.strip()+" -n 1 -k | awk '{print $4}'"
    output=subprocess.check_output(["sudo", "sh", "-c", cmd])
    value=formatResult(output)
    writefile(disk_read_file, value, "a")
    return "%4.2f" %float(value)

def io(pid):
    '''This method returns the current I/O usage in %'''
    cmd="iotop -p "+pid.strip()+" -n 1 | awk '{print $10}'"
    output=subprocess.check_output(["sudo", "sh", "-c", cmd])
    value=formatResult(output)
    writefile(io_file, value, "a")
    return "%4.2f" %float(value)

def writefile(file_name, data, options):
    with open(folder+file_name, options) as myfile:
        myfile.write(str(data)+";")

def formatResult(output):
    [out1,out2]=output.split('.')
    i=0 # num digit
    if type(out1[-2:])!=int:
        i=1
    elif type(out1[-3:])!=int:
        i=2
    else:
        i=3
    return out1[-i:]+'.'+out2[:2]

