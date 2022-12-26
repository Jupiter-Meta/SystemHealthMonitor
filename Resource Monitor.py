#!/usr/bin/python3
import subprocess,datetime
import serial,re,operator,math
from functools import reduce

try:
  temp=subprocess.check_output("vcgencmd measure_temp | awk 'NR==1 {print $1}'", shell=True)
  temp=float(temp[5:9])
except:
  temp=int(subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True))
  temp=temp/1000  



RAM=int(subprocess.check_output("free | awk 'NR==2 {print $7}'",shell=True))
RAM=RAM/1024



CPU=float(subprocess.check_output("top -n1 | awk '/Cpu\(s\):/ {print $2}'",shell=True))


print("Disk Usage in %")
try:
  disk=subprocess.check_output("df -h --total | awk 'NR==9 {print $5}'",shell=True)
  disk=float(disk[:2])
except:
  disk=0

data={'temp':temp,'CPU':CPU,'RAM':RAM,'disk':disk}
print(data)