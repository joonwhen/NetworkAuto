from netmiko import ConnectHandler
from datetime import datetime
import netmiko

hosts = ['10.1.1.2', '10.1.1.3']

startTime = datetime.now()

for routers in hosts:
    print("Connecting to Host: "+routers)
    connection = {
        'device_type': 'cisco_ios_telnet',
        'host':   routers,
        'password': 'cisco',
        'secret': 'cisco'
    }         
    
    commands = ["show ip int brief"]
    net_connect = ConnectHandler(**connection)
    if net_connect:
        print("Connected.")
        net_connect.enable()
        for command in commands:
            output = net_connect.send_command(command)
            print(output)
            print(" ")

    else:
        print("Unable to connect to target host.")
    
    print("=============================================================")

endTime = datetime.now()

total_time = endTime - startTime

print("Total time taken was: "+str(total_time))