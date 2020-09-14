#parallel_query.py
from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread
startTime = datetime.now()

hosts = ['10.10.1.3', '10.10.1.7', '192.168.1.142']
threads = []

def checkparallel(ip):
    device = ConnectHandler(device_type='cisco_ios_telnet', ip=ip, password='cisco', secret = 'cisco')
    output = device.send_command("show ip int brief")
    print ("\nConfiguration for IP: %s is as follow: \n" % (ip))
    print(output)

for host in hosts:
    ip = host
    t = Thread(target=checkparallel, args= (ip,))
    t.start()
    threads.append(t)

#wait for all threads to completed
for t in threads:
    t.join()

print ("\nTotal execution time:")
print(datetime.now() - startTime)