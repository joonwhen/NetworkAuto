from netmiko import ConnectHandler
from threading import Thread
import mysql.connector as sql
import re

# Establish Connection to MySQL Database 
network_db = sql.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "network"
)

# Prompting User Input / Main Menu
def user_input():
    print("Configure by: ")
    print("1. Device Name")
    print("2. IP Address")
    user_selection = input()

    if(user_selection == '1'):
        Device_Selection()
    if(user_selection == '2'):
        IP_Selection()

def obtain_ip(raw_ip):
    y = str(raw_ip)
    x = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", y)
    return x.group()

# Device Selection
def Device_Selection():
    print("Enter Hardware Name: ")
    Hardware_Name = input()
    db_selector = network_db.cursor()
    db_selector.execute("SELECT IP_Address FROM network_hardware WHERE Hardware_Name = Hardware_Name")
    db_result = db_selector.fetchone() # .fetchall()
    address = obtain_ip(db_result)
    device_config(address)

# IP Selection
def IP_Selection():
    print("Enter IP Address: ")
    IP_Address = input()
    device_config(IP_Address)

# Configuration
def device_config(IP_Address):
    
    # Infornation Needed to Connect to Device
    # Improve on this to extract such information from SQL
    connection = {
        'device_type': 'cisco_ios_telnet',
        'host':   IP_Address,
        'password': 'cisco',
        'secret': 'cisco'
    }     
    print("Connecting to: " + IP_Address)
    net_connect = ConnectHandler(**connection)

    if(net_connect):
        net_connect.enable()
        print("Connected to " + IP_Address)
        while True:
            print("Enter Command: ")
            command = input()
            print("")
            if(command == 'x'):
                break
            else:
                output = net_connect.send_command_timing(
                    command_string=command,
                    strip_prompt=False,
                    strip_command=True
                )
                if "Delete filename" in output:
                    output += net_connect.send_command_timing(
                        command_string="\n",
                        strip_prompt=False,
                        strip_command=False
                    )
                if "confirm" in output:
                    output += net_connect.send_command_timing(
                        command_string="y",
                        strip_prompt=False,

                        strip_command=False
                    )
                print(output)
                
    else:
        print("Connection Failed")




# Initialisation    
user_input()