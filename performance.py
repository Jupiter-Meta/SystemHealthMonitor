#!/usr/bin/python3
import subprocess,datetime,pymysql
import serial,re,operator,math
from functools import reduce

conn = pymysql.connect(database="BC",user="admin",password="admin",host="localhost")
cur=conn.cursor()

port=serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=.1)
testarr=[]

cmnd='m11'
port.write(cmnd.encode())
port.write(str.encode("\r"))
rcv =port.read(90)
rcv=rcv.decode()
rcv=rcv.replace('L1','')
l=list(rcv)
g=list(map(lambda v: float(v) if '.' in v else int(v),re.findall(r'\d+(?:\.\d+)?',rcv)))
m11_data=g[1]

cmnd='m15'
port.write(cmnd.encode())
port.write(str.encode("\r"))
rcv =port.read(90)
rcv=rcv.decode()
rcv=rcv.replace('L1','')
l=list(rcv)
g=list(map(lambda v: float(v) if '.' in v else int(v),re.findall(r'\d+(?:\.\d+)?',rcv)))
m15_data=g[1]

cmnd='m16'
port.write(cmnd.encode())
port.write(str.encode("\r"))
rcv =port.read(90)
rcv=rcv.decode()
rcv=rcv.replace('L1','')
l=list(rcv)
g=list(map(lambda v: float(v) if '.' in v else int(v),re.findall(r'\d+(?:\.\d+)?',rcv)))
m16_data=g[1]

print("Real Power")
realpower=m15_data*m16_data*m11_data
print(realpower)

print("Temperature")
# try:
#   temp=subprocess.check_output("vcgencmd measure_temp | awk 'NR==1 {print $1}'", shell=True)
#   temp=float(temp[5:9])
# except:
temp=int(subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True))
temp=temp/1000  
print(temp)

print("Available-RAM")
RAM=int(subprocess.check_output("free | awk 'NR==2 {print $7}'",shell=True))
RAM=RAM/1024
print(RAM)

print("CPU usage in %")
CPU=float(subprocess.check_output("top -n1 | awk '/Cpu\(s\):/ {print $2}'",shell=True))
print(CPU)

print("Disk Usage in %")
try:
  disk=subprocess.check_output("df -h --total | awk 'NR==11 {print $5}'",shell=True)
  print(disk)
  disk=float(disk[:2])
  print(disk)
except:
  disk=0

data={'temp':temp,'CPU':CPU,'RAM':RAM,'disk':disk,'realpower':realpower}
cur.execute("INSERT INTO performance (temp,RAM,CPU,disk,realpower) VALUES (%(temp)s,%(RAM)s,%(CPU)s,%(disk)s,%(realpower)s);",data)
conn.commit()
conn.close()
